import sys
from seleniumbase import config as sb_config

is_windows = False
if sys.platform in ["win32", "win64", "x64"]:
    is_windows = True


def end_reused_class_session_as_needed():
    if (
        hasattr(sb_config, "reuse_class_session")
        and sb_config.reuse_class_session
        and hasattr(sb_config, "shared_driver")
        and sb_config.shared_driver
    ):
        if (
            not is_windows
            or (
                hasattr(sb_config.shared_driver, "service")
                and sb_config.shared_driver.service.process
            )
        ):
            try:
                sb_config.shared_driver.quit()
            except Exception:
                sb_config.shared_driver = None
