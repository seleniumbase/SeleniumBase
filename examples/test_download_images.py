import os
from seleniumbase import BaseCase


class DownloadImages(BaseCase):
    def test_download_images_directly(self):
        self.open("seleniumbase.io/examples/ReadMe/")
        img_elements_with_src = self.find_elements("img[src]")
        unique_src_values = []
        for img in img_elements_with_src:
            src = img.get_attribute("src")
            if src not in unique_src_values:
                unique_src_values.append(src)
        print()
        for src in unique_src_values:
            if src.split(".")[-1] not in ["png", "jpg", "jpeg"]:
                continue
            self.download_file(src)  # Goes to downloaded_files/
            filename = src.split("/")[-1]
            self.assert_downloaded_file(filename)
            folder = "downloaded_files"
            file_path = os.path.join(folder, filename)
            self._print(file_path)

    def test_download_images_via_screenshot(self):
        self.open("seleniumbase.io/error_page/")
        img_elements_with_src = self.find_elements("img[src]")
        unique_src_values = []
        for img in img_elements_with_src:
            src = img.get_attribute("src")
            if src not in unique_src_values:
                unique_src_values.append(src)
        print()
        count = 0
        for src in unique_src_values:
            self.open(src)
            image = self.find_element("img")
            if src.startswith("data:") or ";base64" in src:
                # Special Cases: SVGs, etc. Convert to PNG.
                count += 1
                filename = "svg_image_%s.png" % count
            else:
                filename = src.split("/")[-1]
            folder = "downloaded_files"
            file_path = os.path.join(folder, filename)
            image.screenshot(file_path)
            self.assert_downloaded_file(filename)
            self._print(file_path)
