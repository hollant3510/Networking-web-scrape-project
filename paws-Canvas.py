from selenium import webdriver
import datetime
import time
import sys
from selenium.webdriver.common.keys import Keys
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
from bs4 import BeautifulSoup

#replace username/password with yours
#Do not share your credential with anyone!!!
ACCOUNTS = {
    "user":"pass"
}

URL = 'https://paws.tcnj.edu/'
# login webpage
LOGIN_INI = 'https://paws.tcnj.edu/psp/paws/?cmd=login&languageCd=ENG&'
# after login webpage
# you need to change this URL. The current one is for faculty.
LOGIN_URL = 'https://paws.tcnj.edu/psp/paws/EMPLOYEE/SA/h/?tab=DEFAULT'
MAIN_URL =   'https://paws.tcnj.edu/psp/paws/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?PORTALPARAM_PTCNAV=HC_SSS_STUDENT_CENTER&EOPP.SCNode=SA&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_SELF_SERVICE&EOPP.SCLabel=&EOPP.SCPTcname=PT_PTPP_SCFNAV_BASEPAGE_SCR&FolderPath=PORTAL_ROOT_OBJECT.PORTAL_BASE_DATA.CO_NAVIGATION_COLLECTIONS.ADMN_SELF_SERVICE.ADMN_S20090220233408332651753&IsFolder=false'
SEARCH_URL = 'https://paws.tcnj.edu/psp/paws/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?PORTALPARAM_PTCNAV=HC_SSS_STUDENT_CENTER&EOPP.SCNode=SA&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_SELF_SERVICE&EOPP.SCLabel=&EOPP.SCPTcname=PT_PTPP_SCFNAV_BASEPAGE_SCR&FolderPath=PORTAL_ROOT_OBJECT.PORTAL_BASE_DATA.CO_NAVIGATION_COLLECTIONS.ADMN_SELF_SERVICE.ADMN_S20090220233408332651753&IsFolder=false'
StartingTime = '2019-08-16 10:07:10'

#prints class in format that was requested
def print_class(class_html):
    print(class_html.find("a", ptlinktgt="pt_peoplecode").text)
    professors = class_html.find_all("span", class_="PSLONGEDITBOX")
    print(professors[0].text)
    print(professors[2].text)
    print()
    print()
    print('--------------------------')
    

def searchCourse(driver, user, programName, courseN):
    #moves to main page of paws for self service
    driver.find_element_by_xpath('//*[@id="ADMN_SC_PGT_SELF_SERVICE_Data"]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a').click()
    while True:
        time.sleep(0.05)
        if MAIN_URL == driver.current_url:
           print("Opening...")
           break
    try:
        print(user + " on main page...")
    except:
        print(user + " error on main page")

    time.sleep(5)
    
    #moves to searching page 
    seq = driver.find_elements_by_tag_name('iframe')
    driver.switch_to.frame(seq[0])
    driver.find_element_by_xpath('//*[@id="DERIVED_SSS_SCL_SSS_GO_4$83$"]').click()
    while True:
        time.sleep(0.05)
        if SEARCH_URL == driver.current_url:
           print("Opening Search Page...")
           break
    try:
        time.sleep(4)
        print(user + " on Search page...")
    except:
        print(user + " error on Search page")

    #puts in the values for the search query
    select = Select(driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_STRM$35$"]'))
    select.select_by_visible_text('2019 Fall')
    select = Select(driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_STRM$35$"]'))
    select.select_by_visible_text('2019 Fall')
    time.sleep(1)

    select_class = Select(driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]'))
    select_class.select_by_value(programName.upper())
    select_class = Select(driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]'))
    select_class.select_by_value(programName.upper())
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_CATALOG_NBR$1"]').send_keys(courseN)
    time.sleep(1)
    under_grad = Select(driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_ACAD_CAREER$2"]'))
    under_grad.select_by_visible_text('Undergraduate')
    time.sleep(1)
    #driver.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_SSR_OPEN_ONLY$3"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]').click()
    time.sleep(3)

    #checks that there is a result for the search
    if len(driver.find_elements_by_xpath('//*[@id="DERIVED_CLSMSG_ERROR_TEXT"]')) == 1:
        print('======= No Match =========')
        return

    #turns the results into a soup object
    classes = driver.find_element_by_xpath('//*[@id="ACE_$ICField48$0"]')
    soup = BeautifulSoup(classes.get_attribute('innerHTML'), 'lxml')
    
    #finds all classes in the nearest row object available as a table
    class_list = soup.find_all("table", class_="PSLEVEL1GRIDNBONBO")
    open_class_list = list()
    closed_class_list = list()

    
    #puts the classes on an open and closed classes lists
    for x in class_list:
        if x.find("img", src="/cs/paws/cache/PS_CS_STATUS_CLOSED_ICN_1.gif") is not None:
            if "Closed" in x.find("img", src="/cs/paws/cache/PS_CS_STATUS_CLOSED_ICN_1.gif")['alt']:
                closed_class_list.append(x)
        if x.find("img", src="/cs/paws/cache/PS_CS_STATUS_OPEN_ICN_1.gif") is not None:
            if "Open" in x.find("img", src="/cs/paws/cache/PS_CS_STATUS_OPEN_ICN_1.gif")['alt']:
                open_class_list.append(x)
              

        print('')
        print('')
        print('')

    #prints out the outputs of the different classes
    print('================Open Sections===================')
    for x in open_class_list:
        print_class(x)
        print()

    print('================Closed Sections===================')
    for x in closed_class_list:
        print_class(x)
        print()


    




    #driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_STRM$35$"]/option[2]').click()
# Funtion to login
def login(user,pwd, programName, courseN):
    driver = webdriver.Chrome()
    driver.get(URL)
    LoginStat = False
    while True:
        time.sleep(0.05)
        if LOGIN_INI == driver.current_url:
           print("Opening...")
           break
    try:
        loginForm = driver.find_element_by_xpath('//*[@id="userid"]')
        #longinForm.click()
        loginForm.send_keys(user)
        #time.sleep(1)
        print('send username')
        passwordForm = driver.find_element_by_xpath('//*[@id="pwd"]')
        passwordForm.click()
        passwordForm.send_keys(pwd)
        submit = driver.find_element_by_xpath('//*[@name="submit"]')
        submit.click()
        print(user + " login in process...")
    except:
        print(user + " input error")

    while True:
        time.sleep(0.05)
        if LOGIN_URL == driver.current_url :
           print(user + " login succeed")
           break
    time.sleep(5)
    searchCourse(driver, user, programName, courseN)

if __name__ == "__main__":
    # username & passwords
    data = ACCOUNTS
    # argument sys.argv[1] is discipline name, such as CSC, MAT, BIO, csc, bio ...
    # argument sys.argv[2] is course number, such as 220, 230, 250, 360
    
    # build threads
    threads = []
    for account, pwd in data.items():
        t = Thread(target=login,args=(account,pwd, sys.argv[1], sys.argv[2]))
        threads.append(t)
    for thr in threads:
        time.sleep(0.05)
        thr.start()

