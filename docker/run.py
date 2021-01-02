import os
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print("  func {}() takes {:.2f}s".format(method.__name__, (te - ts)))
        return result
    return timed


class Milan_Pics():
    def __init__(self):
        self.IF_DEBUG = True
        self.MORE = 2

        # define selectors will be used
        self.SELECTOR_LOAD_MORE = "button[class*='LoadMoreButton__StyledLoadButton']"
        self.SELECTOR_CATEGORIES = "a[class^='NewsItemSections__NewsItemLinkContainer']"
        self.SELECTOR_RIGHT_BUTTON = "div[class*='GalleryCarousel__ControlRight']>button"
        self.SELECTOR_IMG = "li[class*='GalleryCarousel__Slide']>span>img"

        if self.IF_DEBUG:
            print("initializing chromedriver")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.wait_right_button = WebDriverWait(self.driver, 3)
        self.driver.get("https://www.acmilan.com/en/news/photogallery/latest")
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.SELECTOR_LOAD_MORE)))

    @timeit
    def load_more(self):
        for i in range(self.MORE):
            load_more_button = self.driver.find_element_by_css_selector(
                self.SELECTOR_LOAD_MORE)
            load_more_button.location_once_scrolled_into_view

            load_more_button.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.SELECTOR_LOAD_MORE), "LOADING..."))
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.SELECTOR_LOAD_MORE), "LOAD MORE"))

    @ timeit
    def run(self):
        self.load_more()

        categories = self.driver.find_elements_by_css_selector(self.SELECTOR_CATEGORIES)
        res = {i.text.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\n"})
                                : i.get_attribute('href') for i in categories}

        for key in res.keys():
            if self.IF_DEBUG:
                print("  \nget_sub() --> total {} categories, current: {}".format(len(res), key))

            self.driver.get(res[key])
            self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.SELECTOR_RIGHT_BUTTON)))
            self.category_pic_links(key)

        self.driver.close()

    @ timeit
    def category_pic_links(self, folder_name):
        right_button = self.driver.find_element_by_css_selector(self.SELECTOR_RIGHT_BUTTON)
        while True:
            try:
                right_button.click()
                self.wait_right_button.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, self.SELECTOR_RIGHT_BUTTON)))
            except TimeoutException:
                break

        links = self.driver.find_elements_by_css_selector(self.SELECTOR_IMG)
        d_links = [i.get_attribute("src").replace("&auto=format", "") for i in links]

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            self._download(folder_name, d_links)
            if self.IF_DEBUG:
                print("  _download() --> save files to {}".format(folder_name))

    def _download(self, folder_name, links):
        for link in links:
            file_name = link.split("/")[-1]
            r = requests.get(link, allow_redirects=True)
            with open("./{}/{}".format(folder_name, file_name), 'wb') as f:
                f.write(r.content)


if __name__ == '__main__':
    m = Milan_Pics()
    m.run()
