"""Running tests with pure "python" instead of directly calling "pytest".
To run, use: "python pure_python.py".
Two examples: pytest.main() and subprocess.call()."""
import pytest
import subprocess

pytest.main(["test_mfa_login.py", "--chrome", "-v"])
subprocess.call(["pytest", "test_mfa_login.py", "--chrome", "-v"])
