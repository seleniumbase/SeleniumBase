import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from random import randint, seed
from seleniumbase import SB
sys.argv.append("-n")  # Tell SeleniumBase to do thread-locking as needed


def launch_driver(url):
    seed(len(threading.enumerate()))  # Random seed for browser placement
    with SB() as sb:
        sb.set_window_rect(randint(4, 720), randint(8, 410), 700, 500)
        sb.open(url=url)
        if sb.is_element_visible("h1"):
            sb.highlight("h1", loops=9)
        else:
            sb.sleep(2.2)


if __name__ == "__main__":
    urls = ['https://seleniumbase.io/demo_page' for i in range(4)]
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        for url in urls:
            executor.submit(launch_driver, url)
