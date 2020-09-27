import helper_functions
import config
import glob
import pandas as pd

#parsing downloaded htmls one by one
def parse_html_files():
    total_people = 0
    non_linkedin_members = 0
    files = glob.glob(config.ABSOLUTE_HTML_PATH + '/*.html')
    helper_functions.append_data('data.csv', "Name", "Location", "Employer at", "Position", "LinkedIn Profile URL", delete_file=True)
    for index, file in enumerate(files):
        print("Parsing File: ", file)
        tp, nlm = helper_functions.parse_html(file)
        if tp:
            total_people+=tp
            non_linkedin_members+=nlm


    print("##### All Stats #####")
    print("Total People: ", total_people)
    print("Total LinkedIn Members:", total_people-non_linkedin_members)
    print("Total Records Scraped:", non_linkedin_members)
    print("Total Unique Records Scraped:", remove_redundant())
    print("#################### ")


# removing redundant results if any
def remove_redundant():
    all_data = pd.read_csv('data.csv')
    helper_functions.append_data('unique_instances_data.csv', "Name", "Location", "Employer at", "Position",
                                 "LinkedIn Profile URL", delete_file=True)
    all_data = all_data.drop_duplicates('LinkedIn Profile URL')
    counter = 0
    for index, row in all_data.iterrows():
        helper_functions.append_data('unique_instances_data.csv', row["Name"], row["Location"], row["Employer at"],
                                     row["Position"]
                                     , row["LinkedIn Profile URL"])
        counter += 1

    return counter

if __name__ == "__main__":
    parse_html_files()
