"""
This script is to automate timesheet using Selenium webdriver.
Reads an Excel workbook (consist: config and individual sheets for week details) through xlrd module
and yaml file to update timecard or adjustment summary.
"""
import sys
import time
import re
import yaml
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import xlrd

'''loading yml file which contains required hardcode data'''
with open('C:/Users/admin/PycharmProjects/Practice/seleniumPractice/timecard_resource.yml', 'r') as yml_f:
    parse_yaml = yaml.safe_load(yml_f)


class TimecardEntry:
    def __init__(self):
        # self.service = Service(executable_path='C:/drivers/chromedriver_win32/chromedriver.exe')
        self.service = Service(executable_path=parse_yaml['execute_path'])
        self.driver = webdriver.Chrome(service=self.service)

    def authentication(self):
        corp_id = self.driver.find_element(by=By.NAME, value="subject")  # for corp id
        corp_id_value = self.workbook[0].cell_value(0, 1)
        corp_id.send_keys(corp_id_value)
        # Corp id filled in Timecard from excel
        print("Corp Id filled.")
        time.sleep(5)
        print(corp_id.get_attribute("value"))
        # self.driver.find_element(By.XPATH, "//*[@id='postButton']/a").click()
        self.driver.find_element(By.XPATH, parse_yaml['next_button_xpath']).click()
        # next button click
        time.sleep(5)
        authentic = str.lower(self.workbook[0].cell_value(1, 1))
        # authentication method selection
        if authentic == 'pingid':
            # self.driver.find_element(By.XPATH, "//*[@id='pingid-div']/a").click()
            self.driver.find_element(By.XPATH, parse_yaml['ping_id_xpath']).click()
            # pingId selected
            print("Verify by Ping id.")
            time.sleep(30)
        elif authentic == 'mobilepass':
            # self.driver.find_element(By.XPATH, "//*[@id='mobilepass-div']/a").click()
            self.driver.find_element(By.XPATH, parse_yaml['mobilepass_xpath']).click()
            # mobilepass selected
            print("Verify by Mobilepass")
            time.sleep(30)
            # self.driver.find_element(By.XPATH, '// *[ @ id = "signOnButton"]').click()
            self.driver.find_element(By.XPATH, parse_yaml['mobilepass_sign_on']).click()
        else:
            print("Select valid Authentication method")
            time.sleep(5)
            self.closing()
        return True

    def closing(self):
        """
        to quit the browser
        """
        try:
            self.driver.quit()
            sys.exit()
        except Exception:
            print("Something went wrong")

    def value_from_excel(self, week_no, row, column):
        """
        to recursively read Excel cell values
        :params week_no, row, column
        """
        try:
            yield self.workbook[week_no].cell(row, column).value
            return True
        except Exception:
            print("Excel is not available..")
            return False

    def timecard(self):
        """
        to select timecard summary
        """
        try:
            # self.driver.find_element(By.XPATH, "//*[contains(text(),'Timecard Summary')]").click()
            self.driver.find_element(By.XPATH, parse_yaml['timecard_xpath']).click()
            # timecard summery
            print("Timecard Summary clicked")
            time.sleep(10)
            return True
        except Exception:
            print("Timecard summary xpath not found...")
            return False

    def adjustment(self):
        """
        to select Adjustment summary
        """
        try:
            # self.driver.find_element(By.XPATH, "//*[@id='ctl00_Menu1']/ul/li[2]/a").click()
            self.driver.find_element(By.XPATH, parse_yaml['adjustment_xpath']).click()
            print("Adjustment Summary clicked")
            # Adjustment summery click
            time.sleep(10)
            return True
        except Exception:
            print("Adjustment summary xpath not found...")
            return False

    def week_validation(self):
        """
        to validate week values in config sheet
        """
        try:
            weeks = str(self.workbook[0].cell_value(2, 1))
            print("Weeks from excel:", weeks)
            if weeks == '0.0':
                print("Invalid week entered")
                # sys.exit()
                self.closing()
            if ',' not in weeks:
                if weeks == "all":
                    count = 0
                    for sheet in self.workbook:
                        print("updating sheet no. :", sheet)
                        count += 1
                    # weeks = [i for i in range(1, count)]
                    weeks = list(1, count)
                elif isinstance(weeks, str):
                    weeks = [int(eval(weeks))]
            else:
                weeks = weeks.split(",")
            self.weekly_entry(weeks)
            return True
        except Exception:
            print("something went wrong in Week number")
            return False

    def operation(self):
        operate = str.lower(self.workbook[0].cell_value(4, 1))
        print(operate)
        if operate == "save":
            # self.driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnSave"]').click()
            self.driver.find_element(By.XPATH, parse_yaml['save_xpath']).click()
            print("this week entry saved")
            # this week timecard saved
        elif operate == "submit":
            # self.driver.find_element(By.XPATH, '// *[ @ id = "ctl00_ContentPlaceHolder1_btnSubmit"]').click()
            self.driver.find_element(By.XPATH, parse_yaml['submit_xpath']).click()
            print("this week entries submitted")
        time.sleep(5)
        print("Back for next week")
        # self.driver.find_element(By.XPATH, '//input[@value="Back"]').click()
        self.driver.find_element(By.XPATH, parse_yaml['back_xpath']).click()
        time.sleep(5)  # back from timecard

    def weekly_entry(self, weeks):
        """
        to update weekly entries according to selected tab in config sheet
        :param weeks
        """
        try:
            if self.SELECT_TAB == 'timecard':
                # new_week_xpath_str = '//*[@id="ctl00_ContentPlaceHolder1_grvTimecardSummary_ctl02_lnkTimevcardID"]'
                new_week_xpath_str = parse_yaml['new_week_timecard_xpath']
            elif self.SELECT_TAB == 'adjustment':
                # new_week_xpath_str = '//*[@id="ctl00_ContentPlaceHolder1_grvApproveTimecard_ctl02_lnkTimevcardID"]'
                new_week_xpath_str = parse_yaml['new_week_adjustment_xpath']
            week_xpath_element_list = new_week_xpath_str.split("2")
            for week_no in weeks:
                week = int(week_no) + 1
                new_week_xpath_str = week_xpath_element_list[0] + str(week) + week_xpath_element_list[1]
                time.sleep(10)
                timecard_week = self.driver.find_element(By.XPATH, new_week_xpath_str)
                desired_y = (timecard_week.size['height'] / 2) + timecard_week.location['y']
                current_y = (self.driver.execute_script('return window.innerHeight') / 2) \
                            + self.driver.execute_script(
                    'return window.pageYOffset')
                scroll_y_by = desired_y - current_y
                self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
                actions = ActionChains(self.driver)
                actions.move_to_element(timecard_week).click().perform()
                print("New week clicked")
                time.sleep(5)  # next to timecard summery
                row_count = self.workbook[int(week_no)].nrows
                column_count = self.workbook[int(week_no)].ncols
                # xpath_str = '//*[@id="ctl00_ContentPlaceHolder1_grvTimeCard_ctl02_txtProject"]'
                xpath_str = parse_yaml['xpath_str1']
                field_id = ["txtProject']", "ddlTask']", "txtMonday']", "txtTuesday']",
                            "txtWednesday']", "txtThursday']",
                            "txtFriday']"]
                xpath_str_element_list = xpath_str.split("2")
                for i in range(1, row_count):
                    for j in range(column_count):
                        value = self.value_from_excel(int(week_no), i, j)
                        new_xpath = xpath_str_element_list[0] + str(i + 1) + "_" + field_id[j]
                        value = value.__next__()
                        if value == str(value):
                            value = value
                        elif value == int(value):
                            value = int(value)
                        else:
                            value = value
                        week_entry = self.driver.find_element(By.XPATH, new_xpath)
                        if week_entry.is_enabled():
                            if field_id[j] == "ddlTask']":
                                old_value = value
                            else:
                                old_value = week_entry.get_attribute("value")
                                if isinstance(old_value, str):
                                    # digit_pattern = re.findall(r'[0-9]', old_value)
                                    digit_pattern = re.findall(r'\d', old_value)
                                    if not len(digit_pattern) == 0:
                                        old_value = eval(old_value)
                            if old_value != value:
                                week_entry.clear()
                                time.sleep(5)
                                week_entry.send_keys(value)
                                actions = ActionChains(self.driver)
                                actions.send_keys(Keys.TAB).perform()
                    time.sleep(5)
                self.operation()
                time.sleep(5)
                week += 1
            return True
        except Exception:
            print("something wrong in Weekly entries")
            return False

    def automate(self):
        self.driver.get("https://timecard.in.capgemini.com")
        print("Timesheet opened on chrome...")
        self.driver.maximize_window()
        # Timesheet on Chrome browser opened and maximized
        try:
            self.workbook = xlrd.open_workbook("C:/Users/admin/Downloads/timesheet_data.xls")
            self.SELECT_TAB = str.lower(self.workbook[0].cell_value(3, 1))
            self.authentication()
            print("Authentication Successful")
        except Exception as exp:
            print("Authentication Failed : ", exp)
        # reading tab choice for timecard updates
        if self.SELECT_TAB == "timecard":
            self.timecard()
            # selected choice is Timecard summary
        elif self.SELECT_TAB == 'adjustment':
            self.adjustment()
            # selected choice is Adjustment summary
        self.week_validation()
        # week validation from config week entry
        time.sleep(10)
        print("Quiting application")
        self.closing()


if __name__ == "__main__":
    OBJ = TimecardEntry()
    OBJ.automate()
