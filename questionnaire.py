# Retrieves 2016 MLB players salary data and displays
# the average of top 125 salaries. The code here is
# substantially the same as the code in questionnaire.ipynb

from collections import namedtuple
import requests
from bs4 import BeautifulSoup


def convert_salary(s):
    """
    Converts a string representation of a dollar amount into an integer

    Parameters:
        s (string): String representation of a dollar-denominated salary

    Returns:
        int: Salary converted into an integer.

    Raises:
        ValueError: input string does not represent a valid dollar amount
    """
    s = s.replace("$", "").replace(",", "")

    if not s.isdigit():
        raise ValueError("{} is not a valid salary".format(s))

    return int(s)


def validate_salary(row):
    """
    Checks whether the salary row data is in proper format.

    Parameters:
        row (list): List contain player name, salary, year, and level

    Returns:
        (boolean): Whether the row was successfully validated.
    """
    # We expect every row to have the form [player, salary, year, level]
    if len(row) != 4:
        return False

    player, salary, year, level = row

    # We should not have any empty data
    # or invalid data formats. We are also
    # only interested in 2016 MLB salaries.
    if any([x == "" for x in row]):
        return False

    if year != "2016" or level != "MLB":
        return False

    try:
        convert_salary(salary)
    except ValueError as e:
        return False

    return True


def get_salaries_average():
    # Retrieve the salaries data and generate the average of the top 125
    #
    # Parameters:
    # Returns:
    #   average (string): average salary in USD format

    # 1. Retrieve the salaries data
    URL = "https://questionnaire-148920.appspot.com/swe/data.html"
    TOP_COUNT = 125
    Salary = namedtuple("Salary", ["player", "salary", "year", "level"])

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    print("Successfully retrieved salaries data.")

    # 2. Validate the data
    salaries_table = soup.find(id="salaries-table")
    salaries_rows = salaries_table.find_all("tr")
    salaries = []
    invalid_data = []

    for tr in salaries_rows:
        td = tr.find_all("td")
        row = [x.text for x in td]

        if not validate_salary(row):
            invalid_data.append(row)
        else:
            player, salary, year, level = row
            salary = int(salary.replace("$", "").replace(",", ""))
            salaries.append(Salary(player, salary, year, level))
    print("Validation complete. {} invalid data found.".format(len(invalid_data)))

    # 3. Calculate the average of top 125 salaries
    if len(salaries) < TOP_COUNT:
        return "Insufficient Data: only {} salaries found.".format(len(salaries))

    salaries.sort(reverse=True, key=lambda x: x.salary)

    # Float-to-USD conversion code from: https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
    average = sum([x.salary for x in salaries[:TOP_COUNT]]) / TOP_COUNT
    average = "${:,.2f}".format(average)

    return "The average salary of top 125 MLB players in 2016: {}".format(average)



if __name__ == "__main__":
    print(get_salaries_average())