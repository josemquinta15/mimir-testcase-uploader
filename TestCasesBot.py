from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time

COURSE_LINK = 'https://class.mimir.io/courses/4f1e9d3e-57b4-4a0e-9e5e-3091fd35f5b2'
MAIL = input('Mail: ')
PSWD = getpass()
autogenerate_output_time = 3

ALL_COURSE_XPATH = '/html/body/div[3]/div/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/div[2]'
EDIT_BUT_XPATH = '/html/body/div[3]/div/div[2]/div[3]/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/a[1]'
visibility_options_id = ['TestCaseForm--showInputCheckbox-label', 'TestCaseForm--showSubmissionOutputCheckbox-label', \
    'TestCaseForm--showCompilerOutputCheckbox-label', 'TestCaseForm--showSubmissionDiffCheckbox-label',\
        'TestCaseForm--showExpectedOutputCheckbox-label', 'TestCaseForm--showErrorSummariesCheckbox-label']


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

    def select_assignment(self, assignment_name):
        # assignments = self.driver.find_elements_by_xpath(ALL_COURSE_XPATH)
        try:
            i = 1
            ready = False
            while not ready:
                xpath = ALL_COURSE_XPATH + f'/div[{i}]/div[2]/div/div/a'
                if self.driver.find_element_by_xpath(xpath).text == assignment_name:
                    print(f'Entering: {self.driver.find_element_by_xpath(xpath).text}')
                    ready = True
                    self.driver.find_element_by_xpath(xpath).click()
                i += 1

        except NoSuchElementException as e:
           print(e)
        
        finally:
            time.sleep(1)

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
           print(e)
        
        finally:
            time.sleep(1)

    def enter_edit_menu(self):
        edit_but = self.driver.find_element_by_id('AssignmentOverview--editAssignment')
        edit_but.click()
        time.sleep(2)

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
        base_xpath = self.select_part(question_name, '//*[@id="AssignmentForm--editQuestionsContainer"]')        
        
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
                continue

        # Settings of the test case
        self.send_data_by_id('TestCaseForm--nameInput', name)
        self.send_data_by_id('TestCaseForm--pointsInput', points)

        #Set I/O testcase
        test_case_type = self.driver.find_element_by_xpath('//*[@id="TestCaseForm--testTypeSelect"]/option[2]').click()
        time.sleep(1)

        #Set Description
        self.send_data_by_id('TestCaseForm--descriptionInput', description)

        #Set input of testcase
        input_space = self.driver.find_element_by_xpath('//*[@id="TestCaseForm--inputEditor"]/textarea')
        input_space.send_keys(Keys.BACK_SPACE)
        input_space.send_keys(input_code)

        #Generate output of testcase
        self.click_by_id('TestCaseForm--autoGenerateOutputButton', autogenerate_output_time)

        # Set strict whitespace
        if strict_whitespace:
            self.click_by_id('TestCaseForm--strictWhitespaceCheckbox-label', 0)

        # Set success threshold and command line arguments
        self.send_data_by_id('TestCaseForm--thresholdInput', success_threshold)
        self.send_data_by_id('TestCaseForm--executionClargsInput', command_line_args)

        # Set private or public
        if not public:
            for id in visibility_options_id:
                self.click_by_id(id, 0)
        time.sleep(1)

        # Save and exit
        self.click_by_id('TestCaseForm--saveButton', 1)
        self.click_by_id('TestCaseForm--exitWithoutSaving', 2)
        print(f'Added Correctly {name} testcase')
        
        




if __name__ == '__main__':
    bot = Bot()
    bot.login_mimir(MAIL, PSWD)
    bot.enter_course()
    bot.select_assignment('Tarea 1')
    bot.enter_edit_menu()
    bot.add_testcase('Auto generated Private Testcase', 5, 'description', 'input code\npasswd\npasswd', 'Parte 1 - Conexión Wi-Fi', public = False)
    bot.add_testcase('Auto generated Public Testcase', 6, 'description', 'network\npass1\npass2', 'Parte 2 - Prueba')
    

    