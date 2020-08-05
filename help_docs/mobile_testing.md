<p align="center"><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/README.md"><img src="https://cdn2.hubspot.net/hubfs/100006/images/SeleniumBaseText_F.png" alt="SeleniumBase" title="SeleniumBase" width="290" /></a></p>

<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Mobile Testing</h2>

Use ``--mobile`` to run SeleniumBase tests using Chrome's mobile device emulator with default values for Device Metrics and User-Agent.

<b>Here's an example mobile test:</b>

[SeleniumBase/examples/test_skype_site.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_skype_site.py)

```bash
pytest test_skype_site.py --mobile
```
[<img src="https://cdn2.hubspot.net/hubfs/100006/images/skype_mobile_test_2.gif" title="SeleniumBase Mobile Testing">](https://cdn2.hubspot.net/hubfs/100006/images/skype_mobile_test_2.gif)

To configure Device Metrics, use:
```bash
--metrics="CSS_Width,CSS_Height,Pixel_Ratio"
```

To configure the User-Agent, use:
```bash
--agent="USER-AGENT-STRING"
```

To find real values for Device Metrics, see:
* [Device Metrics List](https://gist.github.com/sidferreira/3f5fad525e99b395d8bd882ee0fd9d00)

To find real User-Agent strings, see:
* [User Agent Strings List](https://developers.whatismybrowser.com/useragents/explore/)

--------

Here's another example of running a mobile test ([SeleniumBase/examples/test_swag_labs.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py)), which demonstrates using ``--metrics`` and ``--agent`` with ``--mobile``:

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

<p align="center"><div align="center"><a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20📓📖📚-11BBDD.svg" alt="SeleniumBase.io Docs" />
</a> <a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase.io Docs" /></a></div></p>
