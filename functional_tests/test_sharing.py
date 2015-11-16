from selenium import webdriver

from .base import FunctionalTest
from.home_and_list_pages import HomePage


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
        list_page = HomePage(self).start_new_list('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # She shares her list.
        # The page updates to say that it's shared with Guybrush
        list_page.share_list_with('guybrush@example.com')

        # Guybrush now goes to the lists page with his browser
        self.browser = guybrush_browser
        HomePage(self).go_to_home_page().go_to_my_lists_page()

        # He sees Elaine's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page Guybrush can see says that it's Elaine's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'elaine@example.com'
        ))

        # He adds an item to the list
        list_page.add_new_item('Hi Elaine!')

        # When Elaine refreshes the page. she sees Guybrush's addition
        self.browser = elaine_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('Hi Elaine!', 2)
