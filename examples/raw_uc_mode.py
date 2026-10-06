"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.goto("https://gitlab.com/users/sign_in")
    sb.solve_captcha()
    sb.highlight('h1:contains("GitLab")')
    sb.highlight('button:contains("Sign in")')
