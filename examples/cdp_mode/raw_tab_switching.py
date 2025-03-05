from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    sb.open("data:text/html,<h1>Page A</h1>")
    sb.assert_text("Page A")
    sb.open_new_tab()
    sb.open("data:text/html,<h1>Page B</h1>")
    sb.assert_text("Page B")
    sb.switch_to_tab(0)
    sb.assert_text("Page A")
    sb.assert_text_not_visible("Page B")
    sb.switch_to_tab(1)
    sb.assert_text("Page B")
    sb.assert_text_not_visible("Page A")
