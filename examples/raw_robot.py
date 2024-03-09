from seleniumbase import SB

with SB(enable_3d_apis=True, test=True) as sb:
    sb.open("threejs.org/examples/#webgl_animation_skinning_morph")
    sb.switch_to_frame("iframe#viewer")
    sb.set_text_content("#info p", "Hi, I'm Michael Mintz")
    sb.add_css_style("#info p{zoom: 2.54}")
    sb.sleep(0.8)
    sb.click('button:contains("Wave")')
    sb.highlight("#info p")
    sb.select_option_by_text("select", "Idle")
    sb.click('button:contains("ThumbsUp")')
    sb.set_text_content("#info p", "I created SeleniumBase")
    sb.highlight("#info p")
    sb.sleep(0.8)
    sb.click('button:contains("Jump")')
    sb.sleep(1.5)
