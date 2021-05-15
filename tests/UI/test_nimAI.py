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
        # WHEN user goes to landing page
        self.driver.get(self.live_server_url)

        # THEN NimAI info container is displayed
        nim_container = self.driver.find_element_by_id("nimAI-container")
        self.assertEqual(nim_container.find_element_by_tag_name("h2").text, "Beat my Nim AI!")

    def test_landing_page_link_leads_to_nim_page(self):
        # GIVEN the NimAI info container on the landing page
        self.driver.get(self.live_server_url)
        nim_container = self.driver.find_element_by_id("nimAI-container")

        # WHEN a user clicks on the container
        nim_container.click()

        # THEN the NimAI index is displayed
        self.assertEqual(self.driver.find_element_by_id("welcome").text, "Welcome to the game!")

    def test_rules_are_toggled_on_button_click(self):
        # GIVEN the NimAI landing page containing the rules button
        self.driver.get(self.live_server_url + "/showcase/nimAI/")
        rules = self.driver.find_element_by_id("rules__text")
        self.assertFalse(rules.is_displayed())

        rules_button = self.driver.find_element_by_id("rules__btn")

        # WHEN the rules button is clicked
        rules_button.click()

        # THEN the rules are shown
        self.assertTrue(rules.is_displayed())

        # WHEN the button is clicked again
        rules_button.click()

        # THEN the rules are hidden
        self.assertFalse(rules.is_displayed())

    def test_accepting_challenge_leads_to_training_screen(self):
        # GIVEN the NimAI landing page with a "Challenge Accepted" button
        self.driver.get(self.live_server_url + "/showcase/nimAI/")
        challenge_accepted_button = self.driver.find_element_by_id("challenge-accepted")

        # WHEN the button is clicked
        challenge_accepted_button.click()

        # THEN the user is forwarded to the training screen
        self.assertEqual(self.driver.find_element_by_id("message-display").text, "Let the AI learn the game!")

    def test_input_slider_with_difficulty_label(self):
        # GIVEN the training screen with a difficulty slider on level "EASY PEASY"
        self.driver.get(self.live_server_url + "/showcase/nimAI/train/")
        slider = self.driver.find_element_by_class_name("train-slider")
        difficulty = self.driver.find_element_by_class_name("level")
        diff_display = self.driver.find_element_by_id("value-display")

        self.assertEqual(diff_display.text, "1")
        self.assertEqual(difficulty.text, "EASY PEASY")

        # WHEN the slider is moved 20 units to the right
        for _ in range(20):
            slider.send_keys(Keys.RIGHT)

        # THEN the new level is "A LIL' CHALLENGE"
        self.assertEqual(diff_display.text, "21")
        self.assertEqual(difficulty.text, "A LIL' CHALLENGE")

        # WHEN the slider is moved to the max value of 300
        for _ in range(279):
            slider.send_keys(Keys.RIGHT)

        # THEN the level is "PREPARE TO CRY" and the difficulty is 10000
        # due to the non-linear difficulty scale.
        self.assertEqual(diff_display.text, "10000")
        self.assertEqual(difficulty.text, "PREPARE TO CRY")
