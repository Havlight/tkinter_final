from playwright.sync_api import sync_playwright, Page
from attr import dataclass


@dataclass
class Business:
    """holds business data"""

    name: str = ''
    address: str = ''
    category: str = ''
    opening_hours: dict = {}
    phone_number: str = ''
    reviews_count: str = ''
    rating: str = ''
    status: str = ''
    latitude: float = None
    longitude: float = None

    def __str__(self):
        return "name:" + self.name + "\naddress:" + self.address + "\ncate:" + self.category + "\nopening:" \
               + str(self.opening_hours) + "\nphone:" + self.phone_number + "\nreviews_count:" + self.reviews_count \
               + "\nrating:" + self.rating + "\nlatitude:" + str(self.latitude) + " longitude:" + str(self.longitude)


def parse_schedule(schedule_str):
    try:
        # 去掉结尾的点号和多余的空格
        schedule_str = schedule_str.strip().strip('。')

        # 按照分号拆分每一天的时间段
        days = schedule_str.split(';')

        # 创建一个空字典来存储结果
        schedule_dict = {}

        # 处理每一天的时间段
        for day in days:
            # 按照逗号拆分每个部分
            parts = day.split('、')
            day_name = parts[0].strip()  # 获取星期几

            # 获取时间段
            times = []
            for time_range in parts[1:]:
                # 按照 ' 到 ' 拆分时间段，并去掉多余的空格
                if '休息' in time_range:
                    times.extend(["休息"])
                else:
                    start, end = [t.strip() for t in time_range.split('到')]
                    times.extend([start, end])

            # 将时间段列表添加到字典中
            schedule_dict[day_name] = times

        return schedule_dict
    except Exception as e:
        print(e)
        return {}


def single_search(page: Page):
    # xpath
    Title = '//div/h1[contains(@class, "DUwDvf lfPIob")]'
    Rating = '//div[contains(@class, "F7nice")]/span[1]'
    Review_nums = '//div[contains(@class, "F7nice")]/span[last()]'
    Category = '//div[contains(@class, "fontBodyMedium")]//button[contains(@class, "DkEaL ")]'
    # get attribute aria-label
    Phone_Number = '//button[contains(@aria-label,"電話號碼") and @class="CsEnBe"]'
    Address = '//button[contains(@aria-label,"地址: ")]'
    Opening_Hours = '//div[contains(@aria-label, "隱藏本週營業時間")]'
    status_xpath = '//div[@data-hide-tooltip-on-mouse-move and @role]//span[contains(text(),"已打烊")]'
    # not used
    Photos = '//div[contains(@class, "RZ66Rb FgCUCc")]/button[contains(@class,"aoRNLd kn2E5e NMjTrf lvtCsd ")]/img'

    # cteate instance
    bs = Business()
    if page.locator(Title).count() > 0:
        bs.name = page.locator(Title).inner_text()
    if page.locator(Rating).count() > 0:
        bs.rating = page.locator(Rating).inner_text()
    if page.locator(Review_nums).count() > 0:
        bs.reviews_count = page.locator(Review_nums).inner_text()
    if page.locator(Category).count() > 0:
        bs.category = page.locator(Category).inner_text()
    if page.locator(status_xpath).count() > 0:
        bs.status = "已打烊"
    else:
        bs.status = "營業中"
    if page.locator(Address).count() > 0:
        bs.address = page.locator(Address).get_attribute('aria-label')
    if page.locator(Phone_Number).count() > 0:
        bs.phone_number = page.locator(Phone_Number).get_attribute('aria-label')
    if page.locator(Opening_Hours).count() > 0:
        bs.opening_hours = parse_schedule(
            page.locator(Opening_Hours).get_attribute('aria-label').replace('隱藏本週營業時間', ''))

    bs.latitude, bs.longitude = extract_coordinates_from_url(page.url)

    return [bs]


def multiple_search(page: Page, total):
    # iterate all results
    # scraped the same number of listings in the previous iteration
    previously_counted = 0
    while True:
        page.mouse.wheel(0, 10000)
        page.wait_for_timeout(3000)

        if (
                page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()
                >= total
        ):
            listings = page.locator(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            ).all()[:total]
            listings = [listing.locator("xpath=..") for listing in listings]
            print(f"Total Scraped: {len(listings)}")
            break
        else:
            # logic to break from loop to not run infinitely
            # in case arrived at all available listings
            if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    == previously_counted
            ):
                listings = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).all()
                print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                break
            else:
                previously_counted = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()
                print(
                    f"Currently Scraped: ",
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count(),
                )
    # all the search entry
    results = []

    for listing in listings:
        listing.click()
        page.wait_for_timeout(2000)

        # print(listing.inner_text())
        # for scrolling the right sidebar
        page.hover('//div/h1[contains(@class, "DUwDvf lfPIob")]')
        page.mouse.wheel(0, 500)

        # xpath
        Title = '//div/h1[contains(@class, "DUwDvf lfPIob")]'
        Rating = '//div[contains(@class, "F7nice")]/span[1]'
        Review_nums = '//div[contains(@class, "F7nice")]/span[last()]'
        Category = '//div[contains(@class, "fontBodyMedium")]//button[contains(@class, "DkEaL ")]'
        # get attribute aria-label
        Phone_Number = '//button[contains(@aria-label,"電話號碼") and @class="CsEnBe"]'
        Address = '//button[contains(@aria-label,"地址: ")]'
        Opening_Hours = '//div[contains(@aria-label, "隱藏本週營業時間")]'
        status_xpath = '//div[@data-hide-tooltip-on-mouse-move and @role]//span[contains(text(),"已打烊")]'
        # not used
        Photos = '//div[contains(@class, "RZ66Rb FgCUCc")]/button[contains(@class,"aoRNLd kn2E5e NMjTrf lvtCsd ")]/img'

        # cteate instance
        bs = Business()
        if page.locator(Title).count() > 0:
            bs.name = page.locator(Title).inner_text()
        if page.locator(Rating).count() > 0:
            bs.rating = page.locator(Rating).inner_text()
        if page.locator(Review_nums).count() > 0:
            bs.reviews_count = page.locator(Review_nums).inner_text()
        if page.locator(Category).count() > 0:
            bs.category = page.locator(Category).inner_text()
        if page.locator(status_xpath).count() > 0:
            bs.status = "已打烊"
        else:
            bs.status = "營業中"
        if page.locator(Address).count() > 0:
            bs.address = page.locator(Address).get_attribute('aria-label')
        if page.locator(Phone_Number).count() > 0:
            bs.phone_number = page.locator(Phone_Number).get_attribute('aria-label')
        if page.locator(Opening_Hours).count() > 0:
            bs.opening_hours = parse_schedule(
                page.locator(Opening_Hours).get_attribute('aria-label').replace('隱藏本週營業時間', ''))

        bs.latitude, bs.longitude = extract_coordinates_from_url(page.url)

        results.append(bs)
    return results


def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    """helper function to extract coordinates from url"""

    coordinates = url.split('/@')[-1].split('/')[0]
    # return latitude, longitude
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])
