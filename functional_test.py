from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        # Elain has just heard about a cool new to-do webapp. 
        # She goes to check its homepage
        self.browser.get('http://localhost:8008')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item didn't appear in table"
        )

        # There is still a text boc inviting her to add another item. She enters
        # "Use peacock to make a fly" (Elaine is very methodical)
        self.fail('Finish the test!')

        # The page updates again and shows both items on her list

        # Elaine wonders wether the site will remember her list. THe she sees 
        # that the site has generated a unique URL for her -- there is some 
        # explanatory text text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied she goes to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')