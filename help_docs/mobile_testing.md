[<img src="https://cdn2.hubspot.net/hubfs/100006/images/SeleniumBaseText_F.png" title="SeleniumBase" align="center" height="40">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Mobile Testing

Use ``--mobile`` to run your SeleniumBase tests using Chrome's (or Edge's) mobile device emulator with default values for device metrics (CSS Width, CSS Height, Pixel-Ratio) and user agent.

To configure the mobile device metrics, use ``--metrics="CSS_Width,CSS_Height,Pixel_Ratio"``. To configure the user agent, use ``--agent="USER-AGENT-STRING"``.

To find real values for device metrics, [see this GitHub Gist](https://gist.github.com/sidferreira/3f5fad525e99b395d8bd882ee0fd9d00). For a list of available user agent strings, [check out this page](https://developers.whatismybrowser.com/useragents/explore/).

--------

Here's an example of running a mobile test (See https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_skype_site.py):

```bash
pytest test_skype_site.py --mobile --browser=edge
```
[<img src="https://cdn2.hubspot.net/hubfs/100006/images/skype_mobile_test_2.gif" title="SeleniumBase Mobile Testing">](https://cdn2.hubspot.net/hubfs/100006/images/skype_mobile_test_2.gif)

--------

Here's another example of running a mobile test (https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py), which demonstrates using ``--metrics`` and ``--agent`` with ``--mobile``:

```bash
# Run tests using Chrome's mobile device emulator (default settings)
pytest test_swag_labs.py --mobile

# Run mobile tests specifying CSS Width, CSS Height, and Pixel-Ratio
pytest test_swag_labs.py --mobile --metrics="411,731,3"

# Run mobile tests specifying the user agent
pytest test_swag_labs.py --mobile --agent="Mozilla/5.0 (Linux; Android 9; Pixel 3 XL)"
```
[<img src="https://cdn2.hubspot.net/hubfs/100006/images/swag_mobile.gif" title="SeleniumBase Mobile Testing">](https://cdn2.hubspot.net/hubfs/100006/images/swag_mobile.gif)

--------

If you're new to SeleniumBase, read https://github.com/seleniumbase/SeleniumBase to help you get started.