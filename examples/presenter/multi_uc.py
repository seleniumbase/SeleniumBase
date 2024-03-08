"""Part of the UC presentation"""
import pytest
from random import randint
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "-n3")


@pytest.mark.parametrize("", [[]] * 3)
def test_multi_threaded(sb):
    url = "https://gitlab.com/users/sign_in"
    sb.driver.uc_open_with_reconnect(url, 3)
    sb.set_window_rect(randint(0, 755), randint(38, 403), 700, 500)
    try:
        sb.assert_text("Username", '[for="user_login"]', timeout=3)
        sb.post_message("SeleniumBase wasn't detected", duration=4)
        sb._print("\n Success! Website did not detect Selenium! ")
    except Exception:
        sb.driver.uc_open_with_reconnect(url, 3)
        try:
            sb.assert_text("Username", '[for="user_login"]', timeout=3)
            sb.post_message("SeleniumBase wasn't detected", duration=4)
            sb._print("\n Success! Website did not detect Selenium! ")
        except Exception:
            sb.fail('Selenium was detected! Try using: "pytest --uc"')
