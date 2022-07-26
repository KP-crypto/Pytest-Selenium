import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from Utilities import xlutils


class DomHelper:

    def __init__(self, driver,):
        self.driver = driver

    def open_page(self, url):
        self.driver.get(url)

    def reload_page(self):
        self.driver.refresh()

    def maximize_window(self):
        self.driver.maximize_window()

    def print_el(self, element):
        print(
        'tag: ' + element.tag_name + ' id: ' + element.get_attribute('id') + ' class: ' + element.get_attribute(
            'class') + ' text: ' + element.text)

    def get_el(self, selector):
          return self.driver.find_element('xpath',selector)


    def get_els(self, selector):
        if isinstance(selector, (str)):
            return self.driver.find_elements_by_xpath(selector)
        else:
            return selector

    def get_child_el(self, parent, selector):
        try:
            return parent.find_element_by_css_selector(selector)
        except NoSuchElementException:
            return None

    def get_child_els(self, parent, selector):
        return parent.find_elements_by_css_selector(selector)

    def is_el_present(self, selector):
        try:
            self.driver.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False

    def verify_el_present(self, selector):
        if not self.is_el_present(selector):
            raise Exception('Element %s not found' % selector)

    def is_el_visible(self, selector):
        return self.get_el(selector).is_displayed()

    def click_button(self, selector):
        if self.driver.name == 'iPhone':
            self.driver.execute_script('$("%s").trigger("tap")' % (selector))
        else:
            self.get_el(selector).click()

    def enter_text_field(self, selector, text):
        text_field = self.get_el(selector)
        text_field.clear()
        text_field.send_keys(text)

    def select_checkbox(self, selector, name, deselect=False):
        found_checkbox = False
        checkboxes = self.get_els(selector)
        for checkbox in checkboxes:
            if checkbox.get_attribute('name') == name:
                found_checkbox = True
                if not deselect and not checkbox.is_selected():
                    checkbox.click()
                if deselect and checkbox.is_selected():
                    checkbox.click()
        if not found_checkbox:
            raise Exception('Checkbox %s not found.' % (name))

    def select_option(self, selector, value):
        found_option = False
        options = self.get_els(selector)
        for option in options:
            if option.get_attribute('value') == str(value):
                found_option = True
                option.click()
        if not found_option:
            raise Exception('Option %s not found' % (value))

    def get_selected_option(self, selector):
        options = self.get_els(selector)
        for option in options:
            if option.is_selected():
                return option.get_attribute('value')

    def is_option_selected(self, selector, value):
        options = self.get_els(selector)
        for option in options:
            if option.is_selected() != (value == option.get_attribute('value')):
                print(option.get_attribute('value'))
                return False
        return True

    def is_text_equal(self, selector, text):
        print(self.get_el(selector).text)
        return self.get_el(selector).text == text

    def verify_inputs_checked(self, selector, checked):
        checkboxes = self.get_els(selector)
        for checkbox in checkboxes:
            name = checkbox.get_attribute('name')
            if checkbox.is_selected() != (name in checked):
                raise Exception('Input isnt checked as expected - %s' % (name))

    def verify_option_selected(self, selector, value):
        if not self.is_option_selected(selector, value):
            raise Exception('Option isnt selected as expected')

    def verify_radio_value(self, selector, value):
        value = str(value)
        radios = self.get_els(selector)
        for radio in radios:
            radio_value = radio.get_attribute('value')
            if radio.is_selected() and radio_value != value:
                raise Exception('Radio with value %s is checked and shouldnt be' % radio_value)
            elif not radio.is_selected() and radio_value == value:
                raise Exception('Radio with value %s isnt checked and should be' % radio_value)

    def verify_text_field(self, selector, text):
        text_field = self.get_el(selector)
        value = text_field.get_attribute('value')
        if value != text:
            raise Exception('Text field contains %s, not %s' % (value, text))

    def verify_text_value(self, selector, value):
        text_field = self.get_el(selector)
        if text_field.get_attribute('value') != value:
            raise Exception('Value of %s not equal to "%s" - instead saw "%s"' % (
            selector, value, text_field.get_attribute('value')))

    def verify_text_of_el(self, selector, text):
        if not self.is_text_equal(selector, text):
            raise Exception(
                'Text of %s not equal to "%s" - instead saw "%s"' % (selector, text, self.get_el(selector).text))

    def verify_text_in_els(self, selector, text):
        els = self.get_els(selector)
        found_text = False
        for el in els:
            if text in el.text:
                found_text = True
        if not found_text:
            raise Exception('Didnt find text: %s' % (text))

    def verify_text_not_in_els(self, selector, text):
        els = self.get_els(selector)
        found_text = False
        for el in els:
            if text in el.text:
                found_text = True
        if found_text:
            raise Exception('Found text: %s' % (text))

    def select_dropdown_by_visible_text(self,text,selector):
        ele = self.get_el(selector)
        drp_ele = Select(ele)
        drp_ele.select_by_visible_text(text)


    def select_dropdown_by_index(self, index,selector):
        ele = self.get_el(selector)
        drp_ele = Select(ele)
        drp_ele.select_by_index(index)

    def select_dropdown_by_value(self,value,selector):
        ele = self.get_el(selector)
        drp_ele = Select(ele)
        drp_ele.select_by_value(value)

    def is_button_enabled(self, selector):
        return (self.get_el(selector).get_attribute('disabled') == 'false')

    def get_page_title(self, title):
        try:
            page_title = self.driver.title
            return page_title

        except Exception:
            return False

    def accept_alert(self):
        alert = Alert(self.driver)
        alert.accept()

    def dismiss_alert(self):
        alert = Alert(self.driver)
        alert.dismiss()

    def get_alert_text(self,text):
        try:
            alert = Alert(self.driver)
            return alert.text

        except Exception:
            return False

    def press_enter_key(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)

    def press_escape_key(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    def scroll_down(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.END)

    def scroll_up(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)

    def switch_to_window(self,index):
        self.driver.switch_to.window(self.driver.window_handles[index])

    def do_double_click(self,selector):
        element = self.get_el(selector)
        action = ActionChains(self.driver)
        action.double_click(on_element=element).perform()

    def do_right_click(self,selector):
        element = self.get_el(selector)
        action = ActionChains(self.driver)
        action.context_click(on_element=element).perform()

    def do_drag_and_drop(self,source,target):
        source = self.get_el(source)
        target = self.get_el(target)
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target).perform()

    def do_mouseHover(self,selector):
        element = self.get_el(selector)
        action = ActionChains(self.driver)
        action.move_to_element(to_element=element).perform()

    def move_to_element_and_click(self,selector):
        element = self.get_el(selector)
        action = ActionChains(self.driver)
        action.move_to_element(to_element=element).click().perform()

    def switch_to_frame(self,selector):
        element = self.get_el(selector)
        self.driver.switch_to.frame(element)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def get_webpage_html_as_text(self):
        webpage_text = self.driver.find_element_by_tag_name('body').text
        return webpage_text

    def wait_for(self,time_in_sec):
        time.sleep(time_in_sec)

    def read_excel(self,file,sheetname,rownum,colnum):
        xl_value = xlutils.readexel(file,sheetname,rownum,colnum)
        return xl_value


















