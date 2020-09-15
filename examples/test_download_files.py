from seleniumbase import BaseCase


class DownloadTests(BaseCase):

    def test_download_files(self):
        self.open("https://pypi.org/project/seleniumbase/#files")
        pkg_header = self.get_text("h1.package-header__name")
        pkg_name = pkg_header.replace(" ", "-")
        whl_file = pkg_name + "-py2.py3-none-any.whl"
        self.click('div#files a[href$="%s"]' % whl_file)
        self.assert_downloaded_file(whl_file)
        tar_gz_file = pkg_name + ".tar.gz"
        self.click('div#files a[href$="%s"]' % tar_gz_file)
        self.assert_downloaded_file(tar_gz_file)
