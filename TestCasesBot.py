from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time

from parameters import EDIT_BUT_XPATH, visibility_options_id
import parameters as p

COURSE_LINK = 'https://class.mimir.io/courses/4f1e9d3e-57b4-4a0e-9e5e-3091fd35f5b2'
autogenerate_output_time = 3




class Bot:
    def __init__(self, link = 'https://class.mimir.io/login'):
        self.driver = webdriver.Chrome()
        self.driver.get(link)

    def login_mimir(self, email, pswd):
        input_name = self.driver.find_element_by_id('LoginForm--emailInput')
        input_name.send_keys(email)
        input_pswd = self.driver.find_element_by_id('LoginForm--passwordInput')
        input_pswd.send_keys(pswd)
        login_but = self.driver.find_element_by_id('LoginForm--submitButton')
        login_but.click()
        time.sleep(1)
    
    def enter_course(self):
        self.driver.get(COURSE_LINK)
        time.sleep(1)

    def get_assignments(self):
        assignments = []
        assignments.append(self.driver.find_elements_by_xpath(p.DRAFT_COURSE_XPATH))
        assignments.append(self.driver.find_elements_by_xpath(p.SCHEDULED_COURSE_XPATH))
        assignments.append(self.driver.find_elements_by_xpath(p.LIVE_COURSE_XPATH))

        return assignments

    def select_assignment(self, assignment_name):
        assignments = self.get_assignments()

        paths = [p.DRAFT_COURSE_XPATH, p.SCHEDULED_COURSE_XPATH, p.LIVE_COURSE_XPATH]

        for path in paths:
            for i in range(p.MAX_TASKS_PER_COURSEWORK):
                try:
                    xpath = path + f'/div[{i}]/div[2]/div/div/a'
                    if self.driver.find_element_by_xpath(xpath).text == assignment_name:
                        print(f'Entering: {self.driver.find_element_by_xpath(xpath).text}')
                        self.driver.find_element_by_xpath(xpath).click()
                
                except NoSuchElementException as e:
                    pass
                


        
        # found = False
        # while not found:
        #     try:
        #         i = 1
        #         ready = False
        #         while not ready:
        #             xpath = ALL_COURSE_XPATH + f'/div[{i}]/div[2]/div/div/a'
        #             if self.driver.find_element_by_xpath(xpath).text == assignment_name:
        #                 print(f'Entering: {self.driver.find_element_by_xpath(xpath).text}')
        #                 ready = True
        #             self.driver.find_element_by_xpath(xpath).click()
        #             i += 1
        #         found = True 
        #         continue   
        #     except NoSuchElementException as e:
        #         print(e)
            
        # time.sleep(4)

    def select_part(self, part_name, base_xpath):
        try:
            i = 1
            ready = False
            while not ready:
                xpath = base_xpath + f'/div[{i}]/div/div[1]/div[1]/h2/input'
                if self.driver.find_element_by_xpath(xpath).get_attribute('value') == part_name:
                    return base_xpath + f'/div[{i}]/div'
                     
                i += 1

        except NoSuchElementException as e:
          time.sleep(0.5)

    def enter_edit_menu(self):
        while True:
            try:
                edit_but = self.driver.find_element_by_id('AssignmentOverview--editAssignment')
                edit_but.click()
                break
            except NoSuchElementException:
                time.sleep(0.5)

    def send_data_by_id(self, element_id, data_to_send, sleep_time = 0.5):
        element = self.driver.find_element_by_id(element_id)
        element.clear()
        element.send_keys(data_to_send)
        time.sleep(sleep_time)
    
    def click_by_id(self, element_id, sleep_time):
        element = self.driver.find_element_by_id(element_id)
        element.click()
        time.sleep(sleep_time)

    def add_testcase(self, name, points, description, input_code, question_name, strict_whitespace = True, success_threshold = 100, \
        command_line_args = '--fail-on-nonzero-exit', public = True):

        # Select part of the homework to add testcase
        base_xpath = None
        while not base_xpath:
            base_xpath = self.select_part(question_name, '//*[@id="AssignmentForm--editQuestionsContainer"]')        
            # time.sleep(1)
            
        
        # Add new testcase to the preselected homework part
        open_menu = False
        while not open_menu:
            try:
                self.driver.find_element_by_xpath(f'{base_xpath}/div[4]/div[4]/button').click()
                time.sleep(0.8)
                self.driver.find_element_by_xpath(f'{base_xpath}/div[4]/div[4]/div/div/div[1]/div/div/div/button').click()
                time.sleep(0.8)
                self.driver.find_element_by_xpath(f'{base_xpath}/div[4]/div[4]/div/div/div[1]/div/div/div/div/a[1]').click()
                time.sleep(2)
                open_menu = True
            except ElementNotInteractableException:
                time.sleep(0.5)

        # Settings of the test case
        passed = False
        while not passed:
            try:
                self.send_data_by_id('TestCaseForm--nameInput', name)
                self.send_data_by_id('TestCaseForm--pointsInput', points)
                passed = True
            except:
                time.sleep(0.5)

        #Set I/O testcase
        passed = False
        while not passed:
            try:
                test_case_type = self.driver.find_element_by_xpath('//*[@id="TestCaseForm--testTypeSelect"]/option[2]').click()
                passed = True
            except:
                time.sleep(0.5)

        #Set Description
        # self.send_data_by_id('TestCaseForm--descriptionInput', description)

        #Set input of testcase
        passed = False
        while not passed:
            try:
                input_space = self.driver.find_element_by_xpath('//*[@id="TestCaseForm--inputEditor"]/textarea')
                input_space.send_keys(Keys.BACK_SPACE)
                input_space.send_keys(input_code)
                passed = True
            except:
                time.sleep(0.5)

        #Generate output of testcase
        while True:
            try:
                self.click_by_id('TestCaseForm--autoGenerateOutputButton', autogenerate_output_time)
                break
            except:
                time.sleep(0.5)
        # time.sleep(2)

        # Set strict whitespace
        while True:
            try:
                if strict_whitespace:
                    self.click_by_id('TestCaseForm--strictWhitespaceCheckbox-label', 0)
                break
            except:
                time.sleep(0.5)

        # Set success threshold and command line arguments
        while True:
            try:
                self.send_data_by_id('TestCaseForm--thresholdInput', success_threshold)
                self.send_data_by_id('TestCaseForm--executionClargsInput', command_line_args)
                break
            except:
                time.sleep(0.5)

        # Set private or public
        while True:
            try:
                if not public:
                    for id in visibility_options_id:
                        self.click_by_id(id, 0)
                break
            
            except:
                time.sleep(0.5)

        # Save and exit
        while True:
            try:
                self.click_by_id('TestCaseForm--saveButton', 1)
                self.click_by_id('TestCaseForm--exitWithoutSaving', 2)
                print(f'Added Correctly {name} testcase')
                break
            except:
                time.sleep(0.5)
        
        




if __name__ == '__main__':
    bot = Bot()
    MAIL = input('Mail: ')
    PSWD = getpass()
    bot.login_mimir(MAIL, PSWD)
    bot.enter_course()
    bot.select_assignment('Tarea 1')
    bot.enter_edit_menu()
    bot.add_testcase('Auto generated Private Testcase', 5, 'description', 'input code\npasswd\npasswd', 'Parte 5 - Conexión a Wi-Fi', public = False)
    bot.add_testcase('Auto generated Public Testcase', 6, 'description', 'network\npass1\npass2', 'Parte 5 - Conexión a Wi-Fi')
    

    