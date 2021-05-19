import os
import sys

# Remove "" and current working directory from the first entry
# of sys.path (if present) to avoid using the current directory
# in SeleniumBase commands when invoked as "python -m seleniumbase <command>"
if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

if __package__ == "":
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

if __name__ == "__main__":
    import warnings
    from seleniumbase.console_scripts.run import main

    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, module=".*packaging\\.version"
    )
    main()
    sys.exit()
