from seleniumbase import SB

with SB(uc=True) as sb:
    sb.goto("https://pixelscan.dev/")
    score = sb.get_numeric_text("span.text-5xl")
    print(f"Clean Score (higher is better): {score}")
    if sb.headed:
        sb.sleep(2)  # Slow down for the live demo
