import mycdp
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
tab = sb.get_active_tab()
loop = sb.get_event_loop()
loop.run_until_complete(
    tab.send(
        mycdp.emulation.set_device_metrics_override(
            width=412, height=732, device_scale_factor=3, mobile=True
        )
    )
)
url = "https://gitlab.com/users/sign_in"
sb.open(url)
sb.sleep(2)
sb.solve_captcha()
# (The rest is for testing and demo purposes)
sb.assert_text("Username", '[for="user_login"]', timeout=3)
sb.assert_element('label[for="user_login"]')
sb.highlight('button:contains("Sign in")')
sb.highlight('h1:contains("GitLab")')
