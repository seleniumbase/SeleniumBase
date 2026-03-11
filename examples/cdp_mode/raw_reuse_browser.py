"""Test connecting to an existing browser."""
from seleniumbase import sb_cdp

sb1 = sb_cdp.Chrome("https://example.com")
port = sb1.get_rd_port()
sb2 = sb_cdp.Chrome(host="127.0.0.1", port=port)
print("The remote-debugging port: %s" % port)
assert sb1.get_rd_port() == sb2.get_rd_port()
assert sb1.get_current_url() == sb2.get_current_url()
