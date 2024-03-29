import time

from unittest.mock import patch
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from AITA.models import Post


class AITATest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome("tests/UI/chromedriver.exe")

    def tearDown(self) -> None:
        self.driver.quit()

    @patch("AITA.views.Post", autospec=True)
    def test_feedback_to_verdict_is_correct(self, post_stub):
        """GIVEN a user on the post detail page of the AITA project and
        a post with the community verdict 'asshole'

        WHEN the user clicks the Asshole button

        THEN the screen becomes green and a success feedback is shown.
        """
        # GIVEN
        # Model stub (s.t. database isn't hit)
        post = Post.objects.create(title="Title", body="Lorem ipsum dolor...", is_asshole=1)
        post_stub.objects.all.return_value = [post]

        self.driver.get(self.live_server_url + "/showcase/AITA/post/")
        body = self.driver.find_element_by_tag_name("body")

        # Guard assertion: Background is white at first
        self.assertEqual(body.value_of_css_property("background-color"), "rgba(255, 255, 255, 1)")

        asshole_button = self.driver.find_element_by_id("asshole")

        # WHEN
        asshole_button.click()
        time.sleep(1.1)

        # THEN
        self.assertEqual(
            body.value_of_css_property("background-color"),
            "rgba(61, 153, 112, 1)"
        )
        self.assertTrue(body.find_element_by_class_name("feedback-correct").is_displayed())
        self.assertFalse(body.find_element_by_class_name("feedback-incorrect").is_displayed())
