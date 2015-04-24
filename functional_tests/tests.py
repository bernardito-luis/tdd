from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_it_later(self):
        # Elain has just heard about a cool new to-do webapp.
        # She goes to check its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mentionto-do lists
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
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
        inputbox = self.browser.find_element_by_id('id_new_item')
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
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Guybrush starts a new list by entering a new item. He is as
        # interesting as Elaine
        inputbox = self.browser.find_element_by_id('id_new_item')
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

    def test_layout_and_styling(self):
        # Elaine goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=7
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=7
        )

