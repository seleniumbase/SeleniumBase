import asyncio
import mycdp
import time
from seleniumbase import cdp_driver
from seleniumbase import decorators


async def main():
    url = "https://gitlab.com/users/sign_in"
    driver = await cdp_driver.start_async()
    await driver.main_tab.send(
        mycdp.emulation.set_device_metrics_override(
            width=412, height=732, device_scale_factor=3, mobile=True
        )
    )
    page = await driver.get(url, lang="en")
    time.sleep(3)
    try:
        element = await page.select('[style*="grid"] div div', timeout=1)
        await element.mouse_click_with_offset_async(32, 28)
    except Exception:
        pass  # Maybe CAPTCHA was already bypassed
    element = await page.select('label[for="user_login"]')
    await element.flash_async(duration=1.5, color="44EE44")
    time.sleep(1)
    element = await page.select('[data-testid="sign-in-button"]')
    await element.flash_async(duration=2, color="44EE44")
    time.sleep(2)

if __name__ == "__main__":
    # Call an async function with awaited methods
    loop = asyncio.new_event_loop()
    with decorators.print_runtime("raw_mobile_async.py"):
        loop.run_until_complete(main())
