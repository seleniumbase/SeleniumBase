"""CDP.network.ResponseReceived with CDP.network.ResourceType.XHR."""
import ast
import asyncio
import colorama
import mycdp
import sys
import time
from seleniumbase.undetected import cdp_driver

xhr_requests = []
last_xhr_request = None
c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
cr = colorama.Style.RESET_ALL
if "linux" in sys.platform:
    c1 = c2 = cr = ""


def listenXHR(page):
    async def handler(evt):
        # Get AJAX requests
        if evt.type_ is mycdp.network.ResourceType.XHR:
            xhr_requests.append([evt.response.url, evt.request_id])
            global last_xhr_request
            last_xhr_request = time.time()
    page.add_handler(mycdp.network.ResponseReceived, handler)


async def receiveXHR(page, requests):
    responses = []
    retries = 0
    max_retries = 5
    # Wait at least 2 seconds after last XHR request for more
    while True:
        if last_xhr_request is None or retries > max_retries:
            break
        if time.time() - last_xhr_request <= 2:
            retries = retries + 1
            time.sleep(2)
            continue
        else:
            break
    await page
    # Loop through gathered requests and get response body
    for request in requests:
        try:
            res = await page.send(mycdp.network.get_response_body(request[1]))
            if res is None:
                continue
            responses.append({
                "url": request[0],
                "body": res[0],
                "is_base64": res[1],
            })
        except Exception as e:
            print("Error getting response:", e)
    return responses


async def crawl():
    driver = await cdp_driver.cdp_util.start_async()
    tab = await driver.get("about:blank")
    listenXHR(tab)

    # Change url to something that makes ajax requests
    tab = await driver.get("https://resttesttest.com/")
    time.sleep(1)
    # Click AJAX button on https://resttesttest.com/
    element = await tab.select("button#submitajax")
    await element.click_async()
    time.sleep(2)

    xhr_responses = await receiveXHR(tab, xhr_requests)
    for response in xhr_responses:
        print(c1 + "*** ==> XHR Request URL <== ***" + cr)
        print(f'{response["url"]}')
        is_base64 = response["is_base64"]
        b64_data = "Base64 encoded data"
        try:
            headers = ast.literal_eval(response["body"])["headers"]
            print(c2 + "*** ==> XHR Response Headers <== ***" + cr)
            print(headers if not is_base64 else b64_data)
        except Exception:
            response_body = response["body"]
            print(c2 + "*** ==> XHR Response Body <== ***" + cr)
            print(response_body if not is_base64 else b64_data)


if __name__ == "__main__":
    print("================= Starting =================")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(crawl())
