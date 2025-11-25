from seleniumbase import config as sb_config


def end_reused_class_session_as_needed():
    if (
        getattr(sb_config, "reuse_class_session", None)
        and getattr(sb_config, "shared_driver", None)
    ):
        if (
            hasattr(sb_config.shared_driver, "service")
            and sb_config.shared_driver.service.process
        ):
            try:
                sb_config.shared_driver.quit()
            except Exception:
                sb_config.shared_driver = None
