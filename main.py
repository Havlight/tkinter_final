from attr import dataclass
from playwright.sync_api import sync_playwright, Page
from utils import *

search_for = '蕭記爌肉飯'
total = 50
sort_index = 2

def perform_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale='zh-tw')
        page = context.new_page()

        page.goto('https://www.google.com/maps/')
        page.wait_for_timeout(5000)

        # enter search entry
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        results = []
        # for scrolling
        # check if single or multiple results
        try:
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')
            results = multiple_search(page, total)
        except Exception as e:
            results = single_search(page)
        return results


def get_comments():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale='zh-tw')
        page = context.new_page()

        page.goto('https://www.google.com/maps/')
        page.wait_for_timeout(5000)

        # enter search entry
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        results = []
        # comment button xpath
        cmt_btn_xpath = '//button[contains(@aria-label,"評論") and @role="tab"]'
        cmt_xpaths = '//div[contains(@class,"MyEned")]'
        sorting_btn_xpath = '//button[contains(@aria-label,"排序評論") and contains(@data-value,"排序")]'
        sortingway_xpath = f'//div[contains(@id,"action-menu")]/div[contains(@data-index,"{sort_index}")]'
        # click comment btn
        page.locator(cmt_btn_xpath).click()
        # select sorting way
        # page.locator(sorting_btn_xpath).click()
        # page.locator(sortingway_xpath).click()
        # hover comment for scrolling
        page.locator(cmt_xpaths).nth(0).hover()

        # iterate all results
        # scraped the same number of listings in the previous iteration
        previously_counted = 0
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

            if (
                    page.locator(
                        cmt_xpaths
                    ).count()
                    >= total
            ):
                listings = page.locator(
                    cmt_xpaths
                ).all()[:total]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Scraped: {len(listings)}")
                break
            else:
                # logic to break from loop to not run infinitely
                # in case arrived at all available listings
                if (
                        page.locator(
                            cmt_xpaths
                        ).count()
                        == previously_counted
                ):
                    listings = page.locator(
                        cmt_xpaths
                    ).all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = page.locator(
                        cmt_xpaths
                    ).count()
                    print(
                        f"Currently Scraped: ",
                        page.locator(
                            cmt_xpaths
                        ).count(),
                    )

        for i in listings:
            results.append(i.inner_text())

        return results


print(get_comments())

