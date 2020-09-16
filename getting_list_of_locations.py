import platform
import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_WINDOWS, chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_MAC, chrome_options=chrome_options)

    driver.get('https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population?fbclid=IwAR1_HD7D1w4vgVU8EBUwuvWmrT2Ca6JSa5ug5J0F_MB21mPAb6feXEjFvmU')
    table = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[1]')

    table_body = table.find_element_by_tag_name('tbody')
    all_rows_in_body = table_body.find_elements_by_tag_name('tr')

    all_cities = []
    all_states = []

    for row in all_rows_in_body:
        complete_row = row.find_elements_by_tag_name('td')

        all_cities.append(complete_row[1].text.strip().lower())
        all_states.append(complete_row[2].text.strip().lower())

    driver.close()

    all_cities = list(set(all_cities))
    all_states = list(set(all_states))

    all_locations = [city + ', australia' for city in all_cities] + [state + ', australia' for state in all_states]

    print('Total states: ', len(all_states))
    print('Total cities: ', len(all_cities))
    print('Total locations: ', len(all_locations))

    file = open("locations.txt", "w")
    locations_text = '\n'.join(all_locations)
    file.write(locations_text)
    file.close()


if __name__=="__main__":
    """ Example: python3 getting_list_of_locations.py """
    main()
