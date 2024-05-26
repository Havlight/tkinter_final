from attr import dataclass
from playwright.sync_api import sync_playwright, Page
from utils import *
import geocoder
import time
search_for = '品蔚手做麵'
total = 3
#sort_index = 2


def perform_search(search_for, total):
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
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]', timeout=2000)
            results = multiple_search(page, total)
        except Exception as e:
            results = single_search(page)
        return results


def get_comments(search_for, total):
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
        #sortingway_xpath = f'//div[contains(@id,"action-menu")]/div[contains(@data-index,"{sort_index}")]'
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


def get_distance(search_for, total):
    with sync_playwright() as p:
        ip = geocoder.ip("me")
        # "C:\Program Files\Google\Chrome\Application\chrome.exe"
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale='zh-tw', geolocation={"longitude": ip.latlng[1], "latitude": ip.latlng[0]},
                                      permissions=["geolocation"])
        page = context.new_page()

        page.goto('https://www.google.com/maps/')
        page.wait_for_timeout(5000)

        # enter search entry
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        path_btn_xpath = '//button[contains(@data-value,"規劃路線")]'
        path_start_input_xpath = '//input[contains(@class,"tactile-searchbox-input") and contains(@aria-label,"起點")]'
        # top_row_xpath = '//div[contains(@class,"MJtgzc")]/div[contains(@role,"radiogroup")]'
        # times_xpath = '//img[@data-tooltip and @data-tooltip]/following-sibling::*[1]'
        travel_boxes = '//div[@data-travel_mode]'
        page.locator(path_btn_xpath).click()
        page.wait_for_timeout(2000)

        page.locator(path_start_input_xpath).fill("你的位置")
        path_detail_xpath = '//button[contains(@class, "TIQqpf") and contains(@class, "fontTitleSmall") and contains(@aria-labelledby, "section-directions-trip-details-msg-0")]'
        page.locator(path_detail_xpath).click()
        return

#print(perform_search(search_for, total))
#print(get_comments(search_for, total))

#print(get_distance(search_for, total))
