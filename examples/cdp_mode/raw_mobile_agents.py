from seleniumbase import SB

agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
agent += " (KHTML, like Gecko) Mobile Safari/537.36"

sites = ["facebook", "twitter", "linkedin", "youtube", "firefox", "amazon"]
sites += ["chatgpt", "gmail", "perplexity", "snapchat", "tiktok", "roblox"]
urls = [f"https://www.{site}.com" for site in sites]

for url in urls:
    with SB(uc=True, test=True, mobile=True) as sb:
        sb.set_window_position(20, 54)
        sb.activate_cdp_mode()
        sb.open(url)
        sb.sleep(2)
        sb.get_new_driver()
        sb.set_window_position(550, 54)
        sb.activate_cdp_mode(agent=agent)
        sb.open(url)
        sb.sleep(8)
