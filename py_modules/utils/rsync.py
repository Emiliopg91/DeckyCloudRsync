import os
import subprocess
import shutil
import threading

import decky  # pylint: disable=import-error

from plugin_config import PluginConfig
from plugin_logger import PluginLogger
from utils.constants import Constants


class RSync:
    @staticmethod
    def __rsync_diff_map(source, target):
        """
        Devuelve un diccionario {ruta_relativa: ("add"|"modify"|"delete", "file"|"dir")}
        """
        cmd = ["rsync", "-avn", "--delete", source, target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"rsync error: {result.stderr.strip()}")

        changes = {}
        for line in result.stdout.splitlines()[1:-2]:
            line = line.strip()
            if line.startswith("deleting "):
                path = line[len("deleting ") :].strip()
                if not path.startswith("./"):
                    path = "./" + path
                tipo = "dir" if path.endswith("/") else "file"
                changes[path] = ("-", tipo)
            # ignoramos línea "sending incremental file list" y resumen al final
            elif line:
                # es archivo o directorio a añadir o modificar
                # detectamos si es dir si termina en /
                if not line.startswith("./"):
                    line = "./" + line
                tipo = "dir" if line.endswith("/") else "file"
                changes[line] = (
                    "+" if not os.path.exists(os.path.join(target, line)) else "m",
                    tipo,
                )

        return changes

    @staticmethod
    def __apply_change(dst_path, src_path, change):
        action, tipo = change
        if action in ("+", "m"):
            if tipo == "dir":
                os.makedirs(dst_path, exist_ok=True)
                stat_info = os.stat(src_path)
                atime = stat_info.st_atime  # tiempo de último acceso
                mtime = stat_info.st_mtime  # tiempo de última modificación
                os.utime(dst_path, (atime, mtime))
            else:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
        elif action == "-":
            if os.path.isdir(dst_path) and not os.path.islink(dst_path):
                shutil.rmtree(dst_path, ignore_errors=True)
            elif os.path.exists(dst_path):
                os.remove(dst_path)

    @staticmethod
    def bisync(winner_remote):
        """Perform bisync"""
        PluginLogger.log(
            "INFO", f"Getting updates from remote - {Constants.remote_dir}"
        )
        changes_remote = RSync.__rsync_diff_map(
            Constants.remote_dir + "/", Constants.merge_dir + "/"
        )
        for f in sorted(changes_remote.keys(), key=lambda p: (p.count("/"), p)):
            PluginLogger.log("INFO", f"  ({changes_remote[f][0]}){f}")

        PluginLogger.log("INFO", f"Getting updates from local - {Constants.local_dir}")
        changes_local = RSync.__rsync_diff_map(
            Constants.local_dir + "/", Constants.merge_dir + "/"
        )
        for f in sorted(changes_local.keys(), key=lambda p: (p.count("/"), p)):
            PluginLogger.log("INFO", f"  ({changes_local[f][0]}){f}")

        # 1️⃣ Procesar directorios primero para evitar errores al copiar archivos
        all_changes = set(changes_remote.keys()) | set(changes_local.keys())
        dirs_first = sorted(all_changes, key=lambda p: (0 if p.endswith("/") else 1, p))

        if dirs_first:
            PluginLogger.log("INFO", "Applying changes...")
            for path in dirs_first:
                action_remote = changes_remote.get(path)
                action_local = changes_local.get(path)

                src_remote = os.path.join(Constants.remote_dir, path.rstrip("/"))
                src_local = os.path.join(Constants.local_dir, path.rstrip("/"))
                dst_path = os.path.join(Constants.merge_dir, path.rstrip("/"))

                # Cambio solo en dir1
                if action_remote and not action_local:
                    RSync.__apply_change(dst_path, src_remote, action_remote)

                # Cambio solo en dir2
                elif action_local and not action_remote:
                    RSync.__apply_change(dst_path, src_local, action_local)

                # Conflicto
                elif action_remote and action_local:
                    winner_str = "remote" if winner_remote else "local"
                    PluginLogger.log(
                        "INFO",
                        f"  Conflict on {path}, winner {winner_str}",
                    )
                    if winner_remote:
                        RSync.__apply_change(dst_path, src_remote, action_remote)
                    else:
                        RSync.__apply_change(dst_path, src_local, action_local)

            cmd = [
                "rsync",
                "-azv",
                "--delete",
                Constants.merge_dir + "/",
                Constants.remote_dir + "/",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                raise RuntimeError(f"rsync error: {result.stderr.strip()}")

            cmd = [
                "rsync",
                "-azv",
                "--delete",
                Constants.merge_dir + "/",
                Constants.local_dir + "/",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                raise RuntimeError(f"rsync error: {result.stderr.strip()}")
        else:
            PluginLogger.log("INFO", "No changes detected")

    @staticmethod
    def sync_from_remote():
        """Sync remote to local remote folder"""
        user = PluginConfig.get_config_item("settings.remote.user")
        host = PluginConfig.get_config_item("settings.remote.host")
        folder = PluginConfig.get_config_item("settings.remote.directory")
        port = PluginConfig.get_config_item("settings.remote.port")
        password = PluginConfig.get_config_item("settings.remote.password")

        src = f"{user}@{host}:{folder}"
        dst = Constants.remote_dir

        RSync.__sync_with_remote(src, dst, port, password)

    @staticmethod
    def sync_to_remote():
        """Sync local remote folder to remote"""
        user = PluginConfig.get_config_item("settings.remote.user")
        host = PluginConfig.get_config_item("settings.remote.host")
        folder = PluginConfig.get_config_item("settings.remote.directory")
        port = PluginConfig.get_config_item("settings.remote.port")
        password = PluginConfig.get_config_item("settings.remote.password")

        src = Constants.remote_dir
        dst = f"{user}@{host}:{folder}"

        RSync.__sync_with_remote(src, dst, port, password)

    @staticmethod
    def __sync_with_remote(src: str, dst: str, port: int, password: str):
        if not src.endswith("/"):
            src = src + "/"
        if not dst.endswith("/"):
            dst = dst + "/"

        cmd = [
            "sshpass",
            "-p",
            password,
            "rsync",
            "-azv",
            "-e",
            f"ssh -p {port}",
            "--delete",
            src,
            dst,
        ]
        PluginLogger.log("INFO", f"Downloading files from {src} to {dst}")
        cmd_str = " ".join(cmd)
        PluginLogger.log("INFO", f"Running command {cmd_str}")
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
        )

        stdout_thread = threading.Thread(
            target=RSync.__stream_logger, args=(process.stdout, "INFO")
        )
        stderr_thread = threading.Thread(
            target=RSync.__stream_logger, args=(process.stderr, "ERROR")
        )

        # Iniciar threads
        stdout_thread.start()
        stderr_thread.start()

        # Esperar a que termine el proceso
        return_code = process.wait()

        # Esperar a que terminen los threads
        stdout_thread.join()
        stderr_thread.join()

        if return_code != 0:
            raise subprocess.CalledProcessError(
                return_code,
                " ".join(cmd).replace(password, "****"),
                output="",
                stderr="",
            )

    @staticmethod
    def __stream_logger(stream, level):
        for line in iter(stream.readline, ""):
            PluginLogger.log(level, f"  {line.strip()}")
        stream.close()
