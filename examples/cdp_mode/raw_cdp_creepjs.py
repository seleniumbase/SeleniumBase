from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://abrahamjuliot.github.io/creepjs/")
sb.sleep(4)  # Wait for everything to load
pdf_path = "./downloaded_files/creepjs.pdf"
sb.save_as_pdf(pdf_path)
print(f"* PDF saved to: {pdf_path}")
