from selenium import webdriver

from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Elaine is a logged-in user
        self.create_pre_authenticated_session('elaine@example.com')
        elaine_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(elaine_browser))

        # Her friend Guybrush is also hanging out on the lists site
        guybrush_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(guybrush_browser))
        self.browser = guybrush_browser
        self.create_pre_authenticated_session('guybrush@example.com')

        # Elaine goes to ht home page and starts a list
        self.browser = elaine_browser
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Get help\n')

        # She notices a "Share this list" option
        share_box = self.browser.find_element_by_css_selector(
            'input[name=email]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
