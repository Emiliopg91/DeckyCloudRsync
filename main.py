# pylint: disable=missing-module-docstring, line-too-long, broad-exception-caught, too-few-public-methods

import decky  # pylint: disable=import-error

from plugin_config import PluginConfig
from plugin_update import PluginUpdate
from plugin_logger import PluginLogger
from utils.processes import Processes
from utils.cryptography import Cryptography
from utils.fs_sync import FsSync
from utils.logs import LogManager
from utils.constants import Constants
from utils.sync_mngr import SyncManager


class Plugin:
    """Plugin main class"""

    # Lifecycle
    async def _main(self):
        PluginLogger.configure_logger()
        decky.logger.info("Running " + decky.DECKY_PLUGIN_NAME)
        Cryptography.initialize()
        PluginConfig.initialize({"settings.remote.password"})

    async def _unload(self):
        decky.logger.info("Unloading " + decky.DECKY_PLUGIN_NAME)

    async def _migration(self):
        decky.logger.info("Migrating plugin configuration")
        PluginConfig.migrate()

    # Configuration

    async def get_config(self):
        """Get plugin config"""
        return PluginConfig.get_config()

    async def set_config(self, key: str, value):
        """Set config entry"""
        PluginConfig.set_config(key, value)

    async def delete_config(self, key: str):
        """Delete config entry"""
        PluginConfig.delete_config(key)

    # Logger
    async def log(self, level: str, msg: str) -> int:
        """Log line to file"""
        return PluginLogger.log(level, msg)

    # FileSystem sync
    async def copy_to_local(self, directory: str) -> int:
        """Copy files from remote to local locally"""
        return FsSync.copyFolderToLocal(directory)

    # SyncManager
    async def sync(self, winner_remote: bool):
        """Peform sync"""
        await SyncManager.synchronize(winner_remote)

    # Processes
    async def send_signal(self, pid: int, s: str):
        """Send signal to process and its children"""
        return Processes.send_signal(pid, s)

    # Logs

    async def get_last_sync_log(self) -> str:
        """Get last sync log"""
        return LogManager.get_last_sync_log()

    async def get_plugin_log(self) -> str:
        """Get plugin log"""
        return LogManager.get_plugin_log()

    async def get_config_url(self) -> str:
        """Get rclone config url"""
        return LogManager.get_config_url()

    # Misc
    async def get_home_dir(self) -> str:
        """Get home dir"""
        return decky.HOME

    async def get_remote_dir(self) -> str:
        """Get remote dir"""
        return Constants.remote_dir

    async def encrypt(self, plain: str) -> str:
        """Encrypt string"""
        return Cryptography.encrypt_string(plain)

    async def decrypt(self, crypted: str) -> str:
        """Encrypt string"""
        return Cryptography.decrypt_string(crypted)

    # Plugin update
    async def ota_update(self, sudo_pwd=None):
        """Peform OTA update"""
        try:
            return PluginUpdate.ota_update(sudo_pwd)
        except Exception as e:
            decky.logger.error(e)
            return False
