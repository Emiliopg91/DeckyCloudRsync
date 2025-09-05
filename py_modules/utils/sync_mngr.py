# pylint: disable=missing-module-docstring, line-too-long, broad-exception-caught, too-few-public-methods

import asyncio
import os
import time

import decky  # pylint: disable=import-error

from plugin_logger import PluginLogger
from utils.constants import Constants
from utils.fs_sync import FsSync
from utils.rsync import RSync


class SyncManager:
    """Manager for syncronization"""

    @staticmethod
    async def synchronize(winner_remote: bool):
        """Perform synchronization"""
        asyncio.create_task(SyncManager._async_sync(winner_remote))

    @staticmethod
    async def _async_sync(winner_remote: bool):
        PluginLogger.log("INFO", "=== STARTING SYNC ===")

        if not os.path.exists(Constants.local_dir):
            os.makedirs(Constants.local_dir)
        if not os.path.exists(Constants.remote_dir):
            os.makedirs(Constants.remote_dir)
        if not os.path.exists(Constants.merge_dir):
            os.makedirs(Constants.merge_dir)

        start_time = time.time()
        await decky.emit("syncStarted")
        ok = True
        try:
            RSync.sync_from_remote()
            FsSync.copyToLocal()
            RSync.bisync(winner_remote)
            RSync.sync_to_remote()
            FsSync.copyFromLocal()
        except Exception as e:
            ok = False
            PluginLogger.log("ERROR", f"Error on sync: {e}")

        elapsed = (time.time() - start_time) * 1000
        await decky.emit("syncEnded", ok, elapsed)

        PluginLogger.log("INFO", "=== FINISHING SYNC ===")
