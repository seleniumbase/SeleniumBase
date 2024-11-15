<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) CDP Mode 🐙

🐙 <b translate="no">SeleniumBase</b> <b translate="no">CDP Mode</b> (Chrome Devtools Protocol Mode) is a special mode inside of <b><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/uc_mode.md" translate="no"><span translate="no">SeleniumBase UC Mode</span></a></b> that lets bots appear human while controlling the browser with the <b translate="no">CDP-Driver</b>. Although regular <span translate="no">UC Mode</span> can't perform <span translate="no">WebDriver</span> actions while the <code>driver</code> is disconnected from the browser, the <span translate="no">CDP-Driver</span> can still perform actions while maintaining its cover. (For Python 3.11 or newer!)

👤 <b translate="no">UC Mode</b> avoids bot-detection by first disconnecting WebDriver from the browser at strategic times, calling special <code>PyAutoGUI</code> methods to bypass CAPTCHAs (as needed), and finally reconnecting the <code>driver</code> afterwards so that WebDriver actions can be performed again. Although this approach works for bypassing simple CAPTCHAs, more flexibility is needed for bypassing bot-detection on websites with advanced protection. (That's where <b translate="no">CDP Mode</b> comes in.)

🐙 <b translate="no">CDP Mode</b> is based on <a href="https://github.com/HyperionGray/python-chrome-devtools-protocol" translate="no">python-cdp</a>, <a href="https://github.com/HyperionGray/trio-chrome-devtools-protocol" translate="no">trio-cdp</a>, and <a href="https://github.com/ultrafunkamsterdam/nodriver" translate="no">nodriver</a>. <code>trio-cdp</code> is an early implementation of <code>python-cdp</code>, and <code>nodriver</code> is a modern implementation of <code>python-cdp</code>. (Refactored Python-CDP code is imported from <a href="https://github.com/mdmintz/MyCDP" translate="no">MyCDP</a>.)

🐙 <b translate="no">CDP Mode</b> includes multiple updates to the above, such as:

* Sync methods. (Using `async`/`await` is not necessary!)
* The ability to use WebDriver and CDP-Driver together.
* Backwards compatibility for existing UC Mode scripts.
* More configuration options when launching browsers.
* More methods. (And bug-fixes for existing methods.)
* Faster response time for support. (Eg. [Discord Chat](https://discord.gg/EdhQTn3EyE))

--------

### 🐙 <b translate="no">CDP Mode</b> usage:

* **`sb.activate_cdp_mode(url)`**

> (Call that from a **UC Mode** script)

That disconnects WebDriver from Chrome (which prevents detection), and gives you access to `sb.cdp` methods (which don't trigger anti-bot checks).

### 🐙 Here are some common `sb.cdp` methods:

* `sb.cdp.click(selector)`
* `sb.cdp.click_if_visible(selector)`
* `sb.cdp.type(selector, text)`
* `sb.cdp.press_keys(selector, text)`
* `sb.cdp.select_all(selector)`
* `sb.cdp.get_text(selector)`

When `type()` is too fast, use the slower `press_keys()` to avoid detection. You can also use `sb.sleep(seconds)` to slow things down.

To use WebDriver methods again, call:

* **`sb.reconnect()`** or **`sb.connect()`**

(Note that reconnecting allows anti-bots to detect you, so only reconnect if it is safe to do so.)

To disconnect again, call:

* **`sb.disconnect()`**

While disconnected, if you accidentally call a WebDriver method, then SeleniumBase will attempt to use the CDP Mode version of that method (if available). For example, if you accidentally call `sb.click(selector)` instead of `sb.cdp.click(selector)`, then your WebDriver call will automatically be redirected to the CDP Mode version. Not all WebDriver methods have a matching CDP Mode method. In that scenario, calling a WebDriver method while disconnected could raise an error, or make WebDriver automatically reconnect first.

To find out if WebDriver is connected or disconnected, call:

* **`sb.is_connected()`**

--------

### 🐙 <b translate="no">CDP Mode</b> examples:

> [SeleniumBase/examples/cdp_mode](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode)

### 🔖 Example 1: (Pokemon site using Incapsula/Imperva protection with invisible reCAPTCHA)

> [SeleniumBase/examples/cdp_mode/raw_pokemon.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_pokemon.py)

<div></div>
<details>
<summary> ▶️ (<b>Click to expand code preview</b>)</summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.pokemon.com/us"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible("button#onetrust-reject-all-handler")
    sb.sleep(1.2)
    sb.cdp.click('a[href="https://www.pokemon.com/us/pokedex/"]')
    sb.sleep(1.2)
    sb.cdp.click('b:contains("Show Advanced Search")')
    sb.sleep(1.2)
    sb.cdp.click('span[data-type="type"][data-value="electric"]')
    sb.sleep(0.5)
    sb.scroll_into_view("a#advSearch")
    sb.sleep(0.5)
    sb.cdp.click("a#advSearch")
    sb.sleep(1.2)
    sb.cdp.click('img[src*="img/pokedex/detail/025.png"]')
    sb.cdp.assert_text("Pikachu", 'div[class*="title"]')
    sb.cdp.assert_element('img[alt="Pikachu"]')
    sb.cdp.scroll_into_view("div.pokemon-ability-info")
    sb.sleep(1.2)
    sb.cdp.flash('div[class*="title"]')
    sb.cdp.flash('img[alt="Pikachu"]')
    sb.cdp.flash("div.pokemon-ability-info")
    name = sb.cdp.get_text("label.styled-select")
    info = sb.cdp.get_text("div.version-descriptions p.active")
    print("*** %s: ***\n* %s" % (name, info))
    sb.sleep(2)
    sb.cdp.highlight_overlay("div.pokemon-ability-info")
    sb.sleep(2)
    sb.cdp.click('a[href="https://www.pokemon.com/us/play-pokemon/"]')
    sb.cdp.click('h3:contains("Find an Event")')
    location = "Concord, MA, USA"
    sb.cdp.type('input[data-testid="location-search"]', location)
    sb.sleep(1)
    sb.cdp.click("div.autocomplete-dropdown-container div.suggestion-item")
    sb.cdp.click('img[alt="search-icon"]')
    sb.sleep(2)
    events = sb.cdp.select_all('div[data-testid="event-name"]')
    print("*** Pokemon events near %s: ***" % location)
    for event in events:
        print("* " + event.text)
    sb.sleep(2)
```

</details>

### 🔖 Example 2: (Hyatt site using Kasada protection)

> [SeleniumBase/examples/cdp_mode/raw_hyatt.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_hyatt.py)

<div></div>
<details>
<summary> ▶️ (<b>Click to expand code preview</b>)</summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.hyatt.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.cdp.click_if_visible('button[aria-label="Close"]')
    sb.sleep(1)
    sb.cdp.click('span:contains("Explore")')
    sb.sleep(1)
    sb.cdp.click('a:contains("Hotels & Resorts")')
    sb.sleep(3)
    location = "Anaheim, CA, USA"
    sb.cdp.press_keys("input#searchbox", location)
    sb.sleep(1)
    sb.cdp.click("div#suggestion-list ul li a")
    sb.sleep(1)
    sb.cdp.click('div.hotel-card-footer button')
    sb.sleep(1)
    sb.cdp.click('button[data-locator="find-hotels"]')
    sb.sleep(5)
    hotel_names = sb.cdp.select_all(
        'div[data-booking-status="BOOKABLE"] [class*="HotelCard_header"]'
    )
    hotel_prices = sb.cdp.select_all(
        'div[data-booking-status="BOOKABLE"] div.rate'
    )
    sb.assert_true(len(hotel_names) == len(hotel_prices))
    print("Hyatt Hotels in %s:" % location)
    print("(" + sb.cdp.get_text("ul.b-color_text-white") + ")")
    if len(hotel_names) == 0:
        print("No availability over the selected dates!")
    for i, hotel in enumerate(hotel_names):
        print("* %s: %s => %s" % (i + 1, hotel.text, hotel_prices[i].text))
```

</details>

### 🔖 Example 3: (BestWestern site using DataDome protection)

* [SeleniumBase/examples/cdp_mode/raw_bestwestern.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_bestwestern.py)

<div></div>
<details>
<summary> ▶️ (<b>Click to expand code preview</b>)</summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.bestwestern.com/en_US.html"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible("div.onetrust-close-btn-handler")
    sb.sleep(1)
    sb.cdp.click("input#destination-input")
    sb.sleep(2)
    location = "Palm Springs, CA, USA"
    sb.cdp.press_keys("input#destination-input", location)
    sb.sleep(1)
    sb.cdp.click("ul#google-suggestions li")
    sb.sleep(1)
    sb.cdp.click("button#btn-modify-stay-update")
    sb.sleep(4)
    sb.cdp.click("label#available-label")
    sb.sleep(2.5)
    print("Best Western Hotels in %s:" % location)
    summary_details = sb.cdp.get_text("#summary-details-column")
    dates = summary_details.split("ROOM")[0].split("DATES")[-1].strip()
    print("(Dates: %s)" % dates)
    flip_cards = sb.cdp.select_all(".flipCard")
    for i, flip_card in enumerate(flip_cards):
        hotel = flip_card.query_selector(".hotelName")
        price = flip_card.query_selector(".priceSection")
        if hotel and price:
            print("* %s: %s => %s" % (
                i + 1, hotel.text.strip(), price.text.strip())
            )
```

</details>

### 🔖 Example 4: (Walmart site using Akamai protection with PerimeterX)

* [SeleniumBase/examples/cdp_mode/raw_walmart.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_walmart.py)

<div></div>
<details>
<summary> ▶️ (<b>Click to expand code preview</b>)</summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.walmart.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.mouse_click('input[aria-label="Search"]')
    sb.sleep(1.2)
    search = "Settlers of Catan Board Game"
    required_text = "Catan"
    sb.cdp.press_keys('input[aria-label="Search"]', search + "\n")
    sb.sleep(3.8)
    print('*** Walmart Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    items = sb.cdp.find_elements('div[data-testid="list-view"]')
    for item in items:
        if required_text in item.text:
            description = item.querySelector(
                '[data-automation-id="product-price"] + span'
            )
            if description and description.text not in unique_item_text:
                unique_item_text.append(description.text)
                print("* " + description.text)
                price = item.querySelector(
                    '[data-automation-id="product-price"]'
                )
                if price:
                    price_text = price.text
                    price_text = price_text.split("current price Now ")[-1]
                    price_text = price_text.split("current price ")[-1]
                    price_text = price_text.split(" ")[0]
                    print("  (" + price_text + ")")
```

</details>

### 🔖 Example 5: (Nike site using Shape Security)

* [SeleniumBase/examples/cdp_mode/raw_nike.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_nike.py)

<div></div>
<details>
<summary> ▶️ (<b>Click to expand code preview</b>)</summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.nike.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.gui_click_element('div[data-testid="user-tools-container"]')
    sb.sleep(1.5)
    search = "Nike Air Force 1"
    sb.cdp.press_keys('input[type="search"]', search)
    sb.sleep(4)
    elements = sb.cdp.select_all('ul[data-testid*="products"] figure .details')
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
    sb.sleep(2)
```

</details>

(<b>Note:</b> Extra <code translate="no">sb.sleep()</code> calls have been added to prevent bot-detection because some sites will flag you as a bot if you perform actions too quickly.)

(<b>Note:</b> Some sites may IP-block you for 36 hours or more if they catch you using regular <span translate="no">Selenium WebDriver</span>. Be extra careful when creating and/or modifying automation scripts that run on them.)

--------

### 🐙 CDP Mode API / Methods

(Some method args have been left out for simplicity. Eg: <code translate="no">timeout</code>)

```python
sb.cdp.get(url)
sb.cdp.open(url)
sb.cdp.reload(ignore_cache=True, script_to_evaluate_on_load=None)
sb.cdp.refresh()
sb.cdp.get_event_loop()
sb.cdp.add_handler(event, handler)
sb.cdp.find_element(selector)
sb.cdp.find(selector)
sb.cdp.locator(selector)
sb.cdp.find_all(selector)
sb.cdp.find_elements_by_text(text, tag_name=None)
sb.cdp.select(selector)
sb.cdp.select_all(selector)
sb.cdp.find_elements(selector)
sb.cdp.find_visible_elements(selector)
sb.cdp.click_nth_element(selector, number)
sb.cdp.click_nth_visible_element(selector, number)
sb.cdp.click_link(link_text)
sb.cdp.tile_windows(windows=None, max_columns=0)
sb.cdp.get_all_cookies(*args, **kwargs)
sb.cdp.set_all_cookies(*args, **kwargs)
sb.cdp.save_cookies(*args, **kwargs)
sb.cdp.load_cookies(*args, **kwargs)
sb.cdp.clear_cookies(*args, **kwargs)
sb.cdp.sleep(seconds)
sb.cdp.bring_active_window_to_front()
sb.cdp.bring_to_front()
sb.cdp.get_active_element()
sb.cdp.get_active_element_css()
sb.cdp.click(selector)
sb.cdp.click_active_element()
sb.cdp.click_if_visible(selector)
sb.cdp.click_visible_elements(selector, limit=0)
sb.cdp.mouse_click(selector)
sb.cdp.nested_click(parent_selector, selector)
sb.cdp.get_nested_element(parent_selector, selector)
sb.cdp.select_option_by_text(dropdown_selector, option)
sb.cdp.flash(selector, duration=1, color="44CC88", pause=0)
sb.cdp.highlight(selector)
sb.cdp.focus(selector)
sb.cdp.highlight_overlay(selector)
sb.cdp.remove_element(selector)
sb.cdp.remove_from_dom(selector)
sb.cdp.remove_elements(selector)
sb.cdp.send_keys(selector, text)
sb.cdp.press_keys(selector, text)
sb.cdp.type(selector, text)
sb.cdp.set_value(selector, text)
sb.cdp.evaluate(expression)
sb.cdp.js_dumps(obj_name)
sb.cdp.maximize()
sb.cdp.minimize()
sb.cdp.medimize()
sb.cdp.set_window_rect()
sb.cdp.reset_window_size()
sb.cdp.get_window()
sb.cdp.get_text(selector)
sb.cdp.get_title()
sb.cdp.get_current_url()
sb.cdp.get_origin()
sb.cdp.get_page_source()
sb.cdp.get_user_agent()
sb.cdp.get_cookie_string()
sb.cdp.get_locale_code()
sb.cdp.get_screen_rect()
sb.cdp.get_window_rect()
sb.cdp.get_window_size()
sb.cdp.get_window_position()
sb.cdp.get_element_rect(selector)
sb.cdp.get_element_size(selector)
sb.cdp.get_element_position(selector)
sb.cdp.get_gui_element_rect(selector)
sb.cdp.get_gui_element_center(selector)
sb.cdp.get_document()
sb.cdp.get_flattened_document()
sb.cdp.get_element_attributes(selector)
sb.cdp.get_element_attribute(selector, attribute)
sb.cdp.get_element_html(selector)
sb.cdp.set_locale(locale)
sb.cdp.set_attributes(selector, attribute, value)
sb.cdp.gui_press_key(key)
sb.cdp.gui_press_keys(keys)
sb.cdp.gui_write(text)
sb.cdp.gui_click_x_y(x, y)
sb.cdp.gui_click_element(selector)
sb.cdp.gui_drag_drop_points(x1, y1, x2, y2)
sb.cdp.gui_drag_and_drop(drag_selector, drop_selector)
sb.cdp.gui_hover_x_y(x, y)
sb.cdp.gui_hover_element(selector)
sb.cdp.gui_hover_and_click(hover_selector, click_selector)
sb.cdp.internalize_links()
sb.cdp.is_checked(selector)
sb.cdp.is_selected(selector)
sb.cdp.check_if_unchecked(selector)
sb.cdp.select_if_unselected(selector)
sb.cdp.uncheck_if_checked(selector)
sb.cdp.unselect_if_selected(selector)
sb.cdp.is_element_present(selector)
sb.cdp.is_element_visible(selector)
sb.cdp.assert_element_present(selector)
sb.cdp.assert_element_absent(selector)
sb.cdp.assert_element(selector)
sb.cdp.assert_element_visible(selector)
sb.cdp.assert_element_not_visible(selector)
sb.cdp.assert_title(title)
sb.cdp.assert_text(text, selector="html")
sb.cdp.assert_exact_text(text, selector="html")
sb.cdp.scroll_into_view(selector)
sb.cdp.scroll_to_y(y)
sb.cdp.scroll_to_top()
sb.cdp.scroll_to_bottom()
sb.cdp.scroll_up(amount=25)
sb.cdp.scroll_down(amount=25)
sb.cdp.save_screenshot(name, folder=None, selector=None)
```

--------

### 🐙 CDP Mode WebElement API / Methods

```python
element.clear_input()
element.click()
element.flash(duration=0.5, color="EE4488")
element.focus()
element.highlight_overlay()
element.mouse_click()
element.mouse_drag(destination)
element.mouse_move()
element.query_selector(selector)
element.querySelector(selector)
element.query_selector_all(selector)
element.querySelectorAll(selector)
element.remove_from_dom()
element.save_screenshot(*args, **kwargs)
element.save_to_dom()
element.scroll_into_view()
element.select_option()
element.send_file(*file_paths)
element.send_keys(text)
element.set_text(value)
element.type(text)
element.get_position()
element.get_html()
element.get_js_attributes()
```

--------

<img src="https://seleniumbase.github.io/cdn/img/sb_text_f.png" alt="SeleniumBase" title="SeleniumBase" align="center" width="335">

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_gs.png" alt="SeleniumBase" title="SeleniumBase" width="335" /></a></div>
