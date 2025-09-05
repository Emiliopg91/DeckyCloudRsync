# pylint: disable=missing-module-docstring

import decky  # pylint: disable=import-error


class Constants:  # pylint: disable=too-few-public-methods
    """Constants class"""

    plugin_settings = decky.DECKY_PLUGIN_SETTINGS_DIR + "/plugin.json"

    # Common remote directory
    remote_dir = decky.DECKY_PLUGIN_RUNTIME_DIR + "/remote"
    local_dir = decky.DECKY_PLUGIN_RUNTIME_DIR + "/local"
    merge_dir = decky.DECKY_PLUGIN_RUNTIME_DIR + "/merge"
