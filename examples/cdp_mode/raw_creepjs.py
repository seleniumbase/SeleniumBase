from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://abrahamjuliot.github.io/creepjs/")
    sb.sleep(4)  # Wait for everything to load
    pdf_path = "./downloaded_files/creepjs.pdf"
    sb.save_as_pdf(pdf_path)
    print(f"* PDF saved to: {pdf_path}")
