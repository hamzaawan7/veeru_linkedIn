"""
HOW TO SETUP
    1) Check your google chrome version 
        -> Settings
        -> About Chrome
    2) Download the corresponding chrome driver version for your
       particular OS from https://chromedriver.chromium.org/downloads
"""

import platform
import time
import config
import helper_functions
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_WINDOWS, chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_MAC, chrome_options=chrome_options)

    linked_in_search_people = "https://www.linkedin.com/search/results/people/"
    linked_in_sign_in_url = "https://www.linkedin.com/login?fromSignIn=true"

    driver.get(linked_in_sign_in_url)

    print("Signing In ...")

    time.sleep(1)

    driver.find_element_by_id('username').send_keys(config.USERNAME)

    time.sleep(1)

    driver.find_element_by_id('password').send_keys(config.PASSWORD)

    time.sleep(1)

    driver.find_element_by_class_name('login__form_action_container ').click()

    driver.get(linked_in_search_people)


    listed=[]
    with open('screen_names.csv', "r") as csvfile:
            reader = csv.reader(csvfile)

            for query in reader:
                listed.append(query)
            l=[]
            for i in listed:
                try:
                    l.append(i[0])
                except:
                    pass

    first_iteration = True
    for query in l:
            if not first_iteration:
                time.sleep(3)

                print("Clearing Search Filters!!")

                clear_button = driver.find_element(By.XPATH, "//button[@data-control-name='clear_filters']")
                driver.execute_script("arguments[0].click();", clear_button)
                first_iteration = False

            time.sleep(3)

            search_field = driver.find_element(
                By.XPATH,
                "//input[@class='search-global-typeahead__input always-show-placeholder']"
            )

            search_field.clear()
            search_field.send_keys(query)
            search_field.send_keys(Keys.ENTER)

            print("Search Query Entered: " , query)

            # for location in all_locations:
#             time.sleep(3)
            
            # all_filters.send_keys(Keys.ENTER)
            #
            #     locations_input_field = all_filters.find_element(By.XPATH, "//input[@aria-label='Add a country/region']")
            #     locations_input_field.send_keys(location)
            #     locations_input_field.click()
            #
            #     print("Location Value Entered: " + location.upper())
            #
            #     time.sleep(5)
            #
            #     req_val = locations_input_field.get_attribute('aria-owns')
            #
            #     try:
            #         dynamic_locations_list = driver.find_element(By.XPATH, "//div[@id='" + req_val + "']")
            #     except Exception:
            #         locations_input_field.clear()
            #         continue
            #
            #     all_divs = dynamic_locations_list.find_elements_by_tag_name('div')
            #
            #     for div in all_divs:
            #         if (div.get_attribute('aria-selected')) and ((div.get_attribute('aria-selected')) == 'false'):
            #             div.click()
            #
            #             break
            #
#             time.sleep(5)

            # apply_button = driver.find_element(
            #     By.XPATH,
            #     "//button[@class='search-advanced-facets__button--apply ml4 mr2 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']"
            # )
            # apply_button.click()

            time.sleep(5)
            try:
                estimated_results = driver.find_element(By.CLASS_NAME, 'search-results__total').text
                total_results = int(''.join(filter(str.isdigit, estimated_results)))
                print('total results', total_results)
                if(total_results > 100):
                    print('intry')
                    for industry_ind in range(5):
                        
                          
                      
                            time.sleep(5)

                            all_filters = driver.find_element(By.XPATH, "//button[@data-control-name='all_filters']")
                            all_filters.send_keys(Keys.ENTER)

                            all_filters_element = driver.find_element(
                                By.XPATH,"//ul[@class='search-advanced-facets__facets-list']"
                            )
                            industries_element = all_filters_element.find_element(
                                By.XPATH,
                                "//li[@class='search-s-facet search-s-facet--industry inline-block ember-view']"
                            )
                            all_industry_checkboxes = industries_element.find_elements_by_tag_name('input')

                            for industry_checkbox in all_industry_checkboxes:
                                if industry_checkbox.get_attribute("type") == "checkbox":
                                    result = industry_checkbox.is_selected()

                                    if result:
                                        driver.execute_script("arguments[0].click();", industry_checkbox)
                                        print('Checkbox already selected')

                            industry_checkbox = all_industry_checkboxes[industry_ind + 1]

                            if industry_checkbox.get_attribute("type") == "checkbox":
                                driver.execute_script(
                                    "arguments[0].click();", industry_checkbox)

                            time.sleep(5)

                            apply_button = driver.find_element(
                                By.XPATH,
                                "//button[@class='search-advanced-facets__button--apply ml4 mr2 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']"
                            )
                            apply_button.click()

                            # Do Scraping #
                            time.sleep(3)

                            helper_functions.perform_pagination(driver, total_results, query,  industry_ind)
                else:
                    helper_functions.perform_pagination(driver, total_results, query,location=None)
                    time.sleep(3)
                    print("Clearing Search Filters!!")
                    clear_button = driver.find_element(By.XPATH, "//button[@data-control-name='clear_filters']")
                    driver.execute_script("arguments[0].click();", clear_button)
            except:
                print("no results")


    driver.close()

    

if __name__ == "__main__":
    main()
