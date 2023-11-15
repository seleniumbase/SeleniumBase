"""Part of the UC presentation"""
import pytest
from random import randint
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "-n3")


@pytest.mark.parametrize("", [[]] * 3)
def test_multi_threaded(sb):
    sb.driver.uc_open_with_tab("https://nowsecure.nl/#relax")
    sb.set_window_rect(randint(0, 755), randint(38, 403), 700, 500)
    try:
        sb.assert_text("OH YEAH, you passed!", "h1", timeout=4)
        sb.post_message("Selenium wasn't detected!", duration=4)
        sb._print("\n Success! Website did not detect Selenium! ")
    except Exception:
        sb.driver.uc_open_with_tab("https://nowsecure.nl/#relax")
        try:
            sb.assert_text("OH YEAH, you passed!", "h1", timeout=4)
            sb.post_message("Selenium wasn't detected!", duration=4)
            sb._print("\n Success! Website did not detect Selenium! ")
        except Exception:
            sb.fail('Selenium was detected! Try using: "pytest --uc"')
