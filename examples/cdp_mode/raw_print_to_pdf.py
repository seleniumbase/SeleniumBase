from seleniumbase import SB

with SB(uc=True, test=True, pls="none") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://seleniumbase.io")
    sb.assert_title("SeleniumBase Docs")
    file_path = "downloaded_files/sb.pdf"
    sb.print_to_pdf(file_path)
    sb.assert_downloaded_file("sb.pdf")
    sb.assert_pdf_text(file_path, "SeleniumBase")
