from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_list_and_retrieve_it_later(self):
        # Elain has just heard about a cool new to-do webapp.
        # She goes to check its homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mentionto-do lists
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Elaine's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        elaine_list_url = self.browser.current_url
        self.assertRegex(elaine_list_url, '/lists/.+')

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She enters
        # "Use peacock to make a fly" (Elaine is very methodical)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock to make a fly')

        # Now a new user, Guybrush, comes along to the site

        ## We use a new browser session to make sure that no information
        ## of Elaine's is coming through from cookies etc
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Guybrush visits the home page. There is no sign of Elaine's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Guybrush starts a new list by entering a new item. He is as
        # interesting as Elaine
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Find a treasure map')
        inputbox.send_keys(Keys.ENTER)

        # Guybrush gets his own unique URL
        guybrush_list_url = self.browser.current_url
        self.assertRegex(guybrush_list_url, '/lists/.+')
        self.assertNotEqual(guybrush_list_url, elaine_list_url)

        # Again, there is no trace of Elaine's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Find a treasure map', page_text)

        # Saisfied they both go to sleep
