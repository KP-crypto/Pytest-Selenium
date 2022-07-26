import pytest
from Pages.LoginPage import Login
from TestData import testdata
from decouple import config

@pytest.mark.usefixtures("createDirectories")
@pytest.mark.usefixtures("clear_results")
class TestloginPage:

    def test_login(self,setup):
        global loginpage
        self.driver = setup
        loginpage = Login(self.driver)
        #loginpage.do_login(config('USER'),config("PASSWORD"))
        title = loginpage.verify_successfull_login(testdata.HomePageTitle)
        assert title == testdata.HomePageTitle

    # def test_login_err(self):
    #     loginpage.verify_login_err()

    def test_select_continent(self):
        loginpage.select_dropdown_element_by_text('Europe')

    def test_webpage_contains_text(self):
        html_text = loginpage.should_see_text(testdata.SearchText)
        assert testdata.SearchText in html_text






















    # Helper.enter_text_field(locator.Username,username)
    # Helper.enter_text_field(locator.Password,password)
    # Helper.click_button(locator.Login_Btn)
    # Helper.is_text_equal(locator.Login_Err_text,"Login failed!")








