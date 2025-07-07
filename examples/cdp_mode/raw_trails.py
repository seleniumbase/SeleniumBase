from seleniumbase import SB

with SB(uc=True, ad_block=True, test=True) as sb:
    url = "https://www.alltrails.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.click_if_visible("button.osano-cm-close")
    sb.sleep(0.5)
    search_box = 'input[data-testid="homepage-search-box"]'
    search_term = "Thundering Brook Falls"
    sb.type(search_box, search_term + " Trail")
    sb.sleep(1.5)
    sb.click('a span:contains("%s")' % search_term)
    sb.sleep(3.5)
    sb.cdp.click('button:contains("more")')
    sb.sleep(0.7)
    sb.click_if_visible('button[data-testid="modal-close"]')
    sb.sleep(0.7)
    print("Description: (%s)\n" % sb.get_text("h1"))
    print(sb.get_text('div[class*="Description_expanded"]'))
    sb.scroll_to_bottom()
    sb.sleep(1.7)
    sb.click_if_visible('button[data-testid="modal-close"]')
    sb.sleep(1.7)
    summary = '[class*="ReviewSummary_summary"] span'
    print("\nReview Summary:\n\n%s" % sb.get_text(summary))
    reviews = sb.select_all('p[class*="styles_reviewText"]')
    print("\nReviews:")
    for review in reviews:
        print("\n" + review.text)
    folder = "images_exported"
    file_name = "thundering_brook_falls.png"
    sb.save_screenshot(file_name, folder, selector="body")
    print('\n"./%s/%s" was saved!' % (folder, file_name))
