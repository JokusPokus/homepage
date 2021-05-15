import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NimTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome("tests/UI/chromedriver.exe")

    def tearDown(self) -> None:
        self.driver.quit()

    def test_nim_link_on_landing_page_is_displayed(self):
        self.driver.get(self.live_server_url)
        nim_container = self.driver.find_element_by_id("nimAI-container")
        self.assertEqual(nim_container.find_element_by_tag_name("h2").text, "Beat my Nim AI!")

    def test_landing_page_link_leads_to_nim_page(self):
        self.driver.get(self.live_server_url)
        nim_container = self.driver.find_element_by_id("nimAI-container")
        nim_container.click()
        self.assertEqual(self.driver.find_element_by_id("welcome").text, "Welcome to the game!")

    def test_rules_are_toggled_on_button_click(self):
        self.driver.get(self.live_server_url + "/showcase/nimAI/")
        rules = self.driver.find_element_by_id("rules__text")
        self.assertFalse(rules.is_displayed())

        rules_button = self.driver.find_element_by_id("rules__btn")
        rules_button.click()
        self.assertTrue(rules.is_displayed())

        rules_button.click()
        self.assertFalse(rules.is_displayed())

    def test_accepting_challenge_leads_to_training_screen(self):
        self.driver.get(self.live_server_url + "/showcase/nimAI/")
        challenge_accepted_button = self.driver.find_element_by_id("challenge-accepted")
        challenge_accepted_button.click()

        self.assertEqual(self.driver.find_element_by_id("message-display").text, "Let the AI learn the game!")

    def test_input_slider_with_difficulty_label(self):
        self.driver.get(self.live_server_url + "/showcase/nimAI/train/")
        slider = self.driver.find_element_by_class_name("train-slider")
        difficulty = self.driver.find_element_by_class_name("level")
        diff_display = self.driver.find_element_by_id("value-display")

        self.assertEqual(diff_display.text, "1")
        self.assertEqual(difficulty.text, "EASY PEASY")

        for _ in range(20):
            slider.send_keys(Keys.RIGHT)

        self.assertEqual(diff_display.text, "21")
        self.assertEqual(difficulty.text, "A LIL' CHALLENGE")

        for _ in range(279):
            slider.send_keys(Keys.RIGHT)

        self.assertEqual(diff_display.text, "10000")
        self.assertEqual(difficulty.text, "PREPARE TO CRY")
