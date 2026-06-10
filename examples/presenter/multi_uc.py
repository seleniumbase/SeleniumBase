"""Part of the UC presentation. (Upgraded for CDP Mode.)"""
import pytest
from random import randint
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "-n3")


@pytest.mark.parametrize("", [[]] * 3)
def test_multi_threaded(sb):
    sb.activate_cdp_mode()  # If not UC Mode, then 2nd browser
    sb.set_window_rect(randint(4, 680), randint(8, 380), 840, 520)
    sb.goto("https://gitlab.com/users/sign_in")
    sb.sleep(2)
    sb.solve_captcha()
    sb.assert_text("Username", '[for="user_login"]', timeout=3)
    sb.post_message("SeleniumBase wasn't detected", duration=4)
    sb._print("\n Success: SeleniumBase wasn't detected! ")
