from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from selenium.webdriver.support.ui import Select, WebDriverWait

import unittest
from src.pageobjects.basePage import BasePage
import sys
import os
import urllib


class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')
        print browser
        attrs = vars(DesiredCapabilities)
        print ', '.join("%s: %s" % item for item in attrs.items())

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def test_example(self):
        page = BasePage(self.driver)
        page.open()
        self.assertEqual(urllib.unquote(self.driver.title).decode('utf8'), "Google")

    def tearDown(self):
        self.driver.quit()