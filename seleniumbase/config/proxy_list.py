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
* https://www.us-proxy.org/
"""

PROXY_LIST = {
    "example1": "158.69.138.8:1080",  # (Example) - set your own proxy here
    "proxy1": None,
    "proxy2": None,
    "proxy3": None,
    "proxy4": None,
    "proxy5": None,
}
