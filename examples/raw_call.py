"""Can run with "python" instead of using "pytest" directly.
Usage: "python raw_call.py".
Two examples: pytest.main() and subprocess.call()."""
import pytest
import subprocess

pytest.main(["test_coffee_cart.py", "--chrome", "-v"])
subprocess.call(["pytest", "test_mfa_login.py", "--chrome", "-v"])
