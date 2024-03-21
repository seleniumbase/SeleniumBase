"""
Proxy Server "Phone Book".

Simplify running browser tests through a proxy server
by adding your frequently-used proxies here.

Now you can do something like this on the command line:
"pytest SOME_TEST.py --proxy=proxy1"

Format of PROXY_LIST server entries:
* "ip_address:port"  OR  "username:password@ip_address:port"
* "server:port"  OR  "username:password@server:port"
(Do NOT include the http:// or https:// in your proxy string!)

Example proxies in PROXY_LIST below are not guaranteed to be active or secure.
If you don't already have a proxy server to connect to,
you can try finding one from one of following sites:
* https://www.sslproxies.org/
* https://bit.ly/36GtZa1
* https://www.us-proxy.org/
* https://hidemy.name/en/proxy-list/
* http://free-proxy.cz/en/proxylist/country/all/https/ping/all
"""

PROXY_LIST = {
    "example1": "35.185.196.38:3128",  # (Example) - set your own proxy here
    "example2": "129.80.134.71:3128",  # (Example)
    "example3": "socks5://184.178.172.5:15303",  # (Example)
    "proxy1": None,
    "proxy2": None,
    "proxy3": None,
    "proxy4": None,
    "proxy5": None,
}
