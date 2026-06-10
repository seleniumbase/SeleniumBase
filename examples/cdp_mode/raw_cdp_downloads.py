import math
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()

""" Part 1: Using sb.download_file(file_url) """

sb.goto("about:blank")
words_file = "wordle_words.txt"
words_link = (
    "https://seleniumbase.github.io/cdn/txt/%s" % words_file
)
sb.download_file(words_link)
sb.assert_downloaded_file(words_file)
words_path = sb.get_path_of_downloaded_file(words_file)
with open(words_path, "r") as f:
    words_data = f.read()
print("%s | Download = %s bytes." % (words_file, len(words_data)))
sb.assert_true(len(words_data) > 100)  # Verify file not empty
text = '"oasis","carom","cubit"'
sb.assert_in(text, words_data)  # Verify file has expected data

""" Part 2: Using click-initiated downloads """

sb.goto("https://pypi.org/project/sbvirtualdisplay/#files")
sb.assert_element("span#pip-command")
sb.assert_text("Download files", "div#files h2.page-title")
sb.assert_text("Download files", "a#files-tab")
pkg_header = sb.get_text("h1.package-header__name").strip()
pkg_name = pkg_header.replace(" ", "-")
whl_file = pkg_name + "-py3-none-any.whl"
tar_gz_file = pkg_name + ".tar.gz"

# Click the links to download the files into: "./downloaded_files/"
whl_selector = 'div#files a[href$="%s"]' % whl_file
tar_selector = 'div#files a[href$="%s"]' % tar_gz_file
sb.click(whl_selector)  # Download the "whl" file
sb.sleep(0.1)
sb.click(tar_selector)  # Download the "tar" file

# Verify that the downloaded files appear in the [Downloads Folder]
# (This only guarantees that the exact file name is in the folder.)
# (This does not guarantee that the downloaded files are complete.)
# (Later, we'll check that the files were downloaded successfully.)
sb.assert_downloaded_file(whl_file)
sb.assert_downloaded_file(tar_gz_file)

sb.sleep(1)  # Add more time to make sure downloads have completed

# Get the actual size of the downloaded files (in bytes)
whl_path = sb.get_path_of_downloaded_file(whl_file)
with open(whl_path, "rb") as f:
    whl_file_bytes = len(f.read())
print("%s | Download = %s bytes." % (whl_file, whl_file_bytes))
tar_gz_path = sb.get_path_of_downloaded_file(tar_gz_file)
with open(tar_gz_path, "rb") as f:
    tar_gz_file_bytes = len(f.read())
print("%s | Download = %s bytes." % (tar_gz_file, tar_gz_file_bytes))

# Check to make sure the downloaded files are not empty or too small
sb.assert_true(whl_file_bytes > 5000)
sb.assert_true(tar_gz_file_bytes > 5000)

# Get file sizes in kB to compare actual values with displayed values
whl_file_kb = whl_file_bytes / 1000.0
whl_line_fi = sb.get_text('a[href$=".whl"]').strip()
whl_line = sb.get_text('div.file:contains("%s")' % whl_line_fi)
whl_display_kb = float(whl_line.split("(")[1].split(" ")[0])
tar_gz_file_kb = tar_gz_file_bytes / 1000.0
tar_gz_line_fi = sb.get_text('a[href$=".tar.gz"]').strip()
tar_gz_line = sb.get_text('div.file:contains("%s")' % tar_gz_line_fi)
tar_gz_display_kb = float(tar_gz_line.split("(")[1].split(" ")[0])

# Verify downloaded files are the correct size (account for rounding)
sb.assert_true(
    abs(math.floor(whl_file_kb) - math.floor(whl_display_kb)) < 2
)
sb.assert_true(
    abs(math.floor(tar_gz_file_kb) - math.floor(tar_gz_display_kb)) < 2
)

# Finally quit the browser
sb.quit()
