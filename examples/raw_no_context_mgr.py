"""SB() without the context manager `with` block."""
from seleniumbase import SB

sb_context = SB()
sb = sb_context.__enter__()
sb.open("data:text/html,<h1>Test Page</h1>")
sb.highlight("h1", loops=8)
sb_context.__exit__(None, None, None)

"""Same example using `with`:
from seleniumbase import SB

with SB() as sb:
    sb.open("data:text/html,<h1>Test Page</h1>")
    sb.highlight("h1", loops=8)
"""
