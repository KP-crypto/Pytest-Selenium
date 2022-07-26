from Pages.BasePage import DomHelper
from Locators.locators import LoginPage

class Login(DomHelper):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def do_login(self,username,password):
        self.enter_text_field(LoginPage.username,username)
        self.enter_text_field(LoginPage.password,password)
        self.click_button(LoginPage.login_Btn)

    def verify_login_err(self):
        self.verify_text_of_el(LoginPage.login_Err,"Login failed!\nPlease try again.")

    def verify_successfull_login(self,title):
        my_title = self.get_page_title(title)
        return my_title

    def select_dropdown_element_by_text(self,text):
        self.select_dropdown_by_visible_text(text,LoginPage.dropdown_ele)

    def should_see_text(self,text):
        wepage_html = self.get_webpage_html_as_text()
        return wepage_html





