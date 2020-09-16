import glob
import io
import os
import config
import time
import csv
from bs4 import BeautifulSoup


def perform_pagination(driver, total_results, query,location=None, industry=None):
    pages = total_pages(total_results)

    # delete_all_html_files()

    query = query.replace(" ", "_").lower()
    # location = location.replace(" ", "_").lower()

    for page in range(1, pages + 1):
        fname = config.ABSOLUTE_HTML_PATH + query.lower() + '-' + str(page)

        if industry is not None:
            fname += '-' + str(industry)

        fname += '.html'

        if exists_in_file(fname):
            print(fname + " - Exists Already")
            continue

        time.sleep(2)

        goto_page(driver, page)

        scroll_down_page(driver)

        time.sleep(5)

        if is_no_search_results(driver):
            print("Break Loop")
            break

        time.sleep(2)

        print(fname + " - Saving")
        save_html_file(driver, fname)

        time.sleep(2)


def save_html_file(driver, fname):
    element = driver.find_element_by_xpath("//div[@class='search-results-container']")
    html_str = element.get_attribute("outerHTML")

    time.sleep(2)

    with io.open(fname, "w", encoding="utf-8") as f:
        f.write(html_str)

    time.sleep(1)

    write_to_log_file(fname)


def scroll_down_page(driver, speed=8):
    current_scroll_position, new_height = 0, 1

    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def total_pages(total_records):
    pages = total_records / 10
    remainder = total_records % 10

    if remainder > 0:
        pages += 1

    return int(pages)


def goto_page(driver, page_no):
    driver.get(driver.current_url + "&page=" + str(page_no))


def is_no_search_results(driver):
    try:
        driver.find_element_by_xpath("//div[@class='search-no-results__container']")

        return True
    except:
        return False


def write_to_log_file(name):
    with io.open(config.LOG_FILE, "a") as f:
        f.write(name)
        f.write("\n")


def exists_in_file(name):
    logfile = open(config.LOG_FILE, 'r')
    log_list = logfile.readlines()
    logfile.close()

    for line in log_list:
        if name in line:
            return True

    return False


def delete_all_html_files():
    files = glob.glob(config.ABSOLUTE_HTML_PATH + '/*')

    for f in files:
        os.remove(f)


def append_data(file_path, name, location, workplace_name, position, url, delete_file=False):
    try:
        if delete_file:
            os.remove(file_path)
    except Exception as e:
        print(e)
    fieldnames = ['NAME', 'CURRENT_POSITION', 'WORK_PLACE', 'LOCATION', 'URL', ]

    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerow({
            "NAME": name,
            "CURRENT_POSITION": position,
            "WORK_PLACE": workplace_name,
            'LOCATION': location,
            'URL': url,

        })


def detail_parser(details_text):
    if ' at ' in details_text:
        position = details_text.split(' at ')[0]
        works_at = details_text.split(' at ')[1]
        if ' - ' in works_at:
            works_at = works_at.split(' - ')[0]
        if ' at ' in works_at:
            works_at = works_at.split(' at ')[1]
    elif ' | ' in details_text:
        position = details_text.split(' | ')[0]
        works_at = details_text.split(' | ')[1]
        if ' - ' in works_at:
            works_at = works_at.split(' - ')[0]
        if ' at ' in works_at:
            works_at = works_at.split(' at ')[1]
    elif ' @ ' in details_text:
        position = details_text.split(' @ ')[0]
        works_at = details_text.split(' @ ')[1]
        if ' - ' in works_at:
            works_at = works_at.split(' - ')[0]
        if ' at ' in works_at:
            works_at = works_at.split(' at ')[1]
    elif ' - ' in details_text:
        position = details_text.split(' - ')[0]
        works_at = details_text.split(' - ')[1]
        if ' - ' in works_at:
            works_at = works_at.split(' - ')[0]
        if ' at ' in works_at:
            works_at = works_at.split(' at ')[1]
    elif ' / ' in details_text:
        position = details_text.split(' / ')[0]
        works_at = details_text.split(' / ')[1]
        if ' - ' in works_at:
            works_at = works_at.split(' - ')[0]
        if ' at ' in works_at:
            works_at = works_at.split(' at ')[1]
    else:
        position = None
        works_at = None
    return position, works_at


def headline_parser(headline_text):
    if ' at ' in headline_text:
        position = headline_text.split(' at ')[0]
        works_at = headline_text.split(' at ')[1]
    elif ' | ' in headline_text:
        position = headline_text.split(' | ')[0]
        works_at = headline_text.split(' | ')[1]
    elif ' @ ' in headline_text:
        position = headline_text.split(' @ ')[0]
        works_at = headline_text.split(' @ ')[1]

    elif ' - ' in headline_text:
        position = headline_text.split(' - ')[0]
        works_at = headline_text.split(' - ')[1]

    elif ' / ' in headline_text:
        position = headline_text.split(' / ')[0]
        works_at = headline_text.split(' / ')[1]

    else:
        position = headline_text
        works_at = "Not Found"

    return position, works_at


def parse_html(filename):
    soup = BeautifulSoup(open(filename, encoding="utf-8"), "html.parser")
    total_people = 0
    non_linked_members = 0
    ul = soup.find('ul', {'class': 'search-results__list'})
    try:
        people = ul.find_all('li', {'class': 'search-result'})
        names = []
        for p in people:
            total_people+=1
            name_box = p.find('span', {'class': ['name', 'actor-name']})
            if name_box:
                name = name_box.text.strip()
                if name != "LinkedIn Member":
                    non_linked_members+=1
                    names.append(name)
                    # extract remaining data
                    location = p.find(
                        attrs={'class': 'subline-level-2 t-12 t-black--light t-normal search-result__truncate'}
                    )
                    location = location.text.strip()
                    detail = p.find('p', {'class': 'mt2 t-12 t-black--light t-normal search-result__snippets-black'})
                    headline = p.find(attrs={'class': 'subline-level-1 t-14 t-black t-normal search-result__truncate'})
                    url = p.find(attrs={'data-control-name': 'search_srp_result'}).get('href')
                    headline = headline.text.strip()

                    if detail:
                        detail = detail.text.strip()
                        # if detail.split(':')[0].lower() == 'current':

                        position, works_at = detail_parser(detail.split(':')[1])
                        if not position:
                            position, works_at = headline_parser(headline)
                        # else:
                        #     position, works_at = headline_parser(headline)
                    else:
                        position, works_at = headline_parser(headline)

                    if not url.startswith('https://www.linkedin.com'):
                        url = 'https://www.linkedin.com' + url
                    append_data('data.csv', name, location, works_at.strip(), position.strip(), url)

        return total_people, non_linked_members

    except Exception as e:
        print(e)
        return None, None
