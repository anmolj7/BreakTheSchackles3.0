from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.common.by import By


class download:
    def __init__(self, email, password, time, code, date):
        self.email = email
        self.password = password
        self.time = time
        self.code = code
        self.date = date
        opt = Options()
        # opt.add_argument("--start-maximized")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1,
            'download.default_directory': os.getcwd()
        })
        opt.add_experimental_option('excludeSwitches', ['test-type'])
        try:
            s = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=s, options=opt)
        except:
            s = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=s, options=opt)

    def google_login(self):
        # self.messages.send_message("Initating the process.")
        print("Logging into gmail id")
        self.driver.get(
            'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

        # input Gmail
        self.driver.find_element_by_id("identifierId").send_keys(self.email)
        self.driver.find_element_by_id("identifierNext").click()
        self.driver.implicitly_wait(10)

        # input Password
        self.driver.find_element(By.XPATH,
                                 '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.password)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("passwordNext").click()
        self.driver.implicitly_wait(10)

        # go to google home page
        self.driver.get('https://google.com/')
        self.driver.implicitly_wait(100)
        time.sleep(2)

    def downloadfile(self):
        print(f"In downloading files function.")
        self.driver.get(
            "https://mail.google.com/mail/u/1/#search/meet-recordings")
        time.sleep(2)
        for i in range(1, 15):
            print(f"In downloading files function.")
            text = self.driver.find_element(
                By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[5]/div[2]/div/table/tbody/tr[{}]/td[5]/div[1]/div/div[3]/span/span'.format(i)).text
            checker = self.code+" ("+self.date+" at "+self.time+" GMT-8)"
            print(checker)
            if(checker == text):
                print(f"Found the meet, breaking out")
                self.driver.find_element(
                    By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[5]/div[2]/div/table/tbody/tr[{}]/td[5]/div[2]/div'.format(i)).click()
                time.sleep(5)
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.find_element(
                    By.XPATH, '/html/body/div[4]/div[4]/div/div[3]/div[2]/div[2]/div[3]/div').click()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                break
        self.driver.close()
        time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()