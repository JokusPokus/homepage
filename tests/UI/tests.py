from django.test import LiveServerTestCase
from django.core.management import call_command
from selenium import webdriver


class NimTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome("tests/UI/chromedriver.exe")

    def tearDown(self) -> None:
        self.driver.close()

    def test_landing_page_link_is_displayed(self):
        self.driver.get('http://127.0.0.1:8000/')
        nim_container = self.driver.find_element_by_id("nimAI-container")
        self.assertEqual(nim_container.find_element_by_tag_name("h2").text, "Beat my Nim AI!")

