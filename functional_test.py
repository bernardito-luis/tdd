from selenium import webdriver
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
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box (Elaine's hobby 
        # is tying fly-fishing lures)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text boc inviting her to add another item. She enters
        # "Use peacock to make a fly" (Elaine is very methodical)

        # The page updates again and shows both items on her list

        # Elaine wonders wether the site will remember her list. THe she sees 
        # that the site has generated a unique URL for her -- there is some 
        # explanatory text text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied she goes to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')