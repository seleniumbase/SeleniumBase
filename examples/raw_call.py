"""Calling tests with "python" instead of directly using "pytest".
To run, use: "python raw_call.py".
Two examples: pytest.main() and subprocess.call()."""
import pytest
import subprocess

pytest.main(["test_mfa_login.py", "--chrome", "-v"])
subprocess.call(["pytest", "test_mfa_login.py", "--chrome", "-v"])
