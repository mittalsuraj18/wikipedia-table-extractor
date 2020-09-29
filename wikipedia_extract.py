import time

from selenium.webdriver import Firefox, FirefoxOptions
from tqdm import tqdm as tqdm

WIKI_LINK = "https://en.wikipedia.org/wiki/Neighborhoods_in_New_York_City"
SAVE_NAME = wikipedia_link.split("/")[-1]

# noinspection DuplicatedCode
def extract_cell_data(cell_element):
    lis = cell_element.find_elements_by_tag_name("li")
    if lis:
        cell_data = []
        for li in lis:
            cell_data.append(li.text)
    else:
        cell_data = cell_element.text
    return cell_data


def extract_row_items(row_element):
    ths = row_element.find_elements_by_tag_name("th")
    tds = row_element.find_elements_by_tag_name("td")
    rows_elements = []
    for cell in ths:
        col_span = cell.get_attribute("colspan")
        cell_data = extract_cell_data(cell)
        if col_span:
            for i in range(int(col_span)):
                rows_elements.append(cell_data)
        else:
            rows_elements.append(cell_data)
    for cell in tds:
        col_span = cell.get_attribute("colspan")
        cell_data = extract_cell_data(cell)
        if col_span:
            for i in range(int(col_span)):
                rows_elements.append(cell_data)
        else:
            rows_elements.append(cell_data)
    return rows_elements


def extract_header(header_element):
    rows = header_element.find_elements_by_tag_name("tr")


# noinspection DuplicatedCode
def _main():
    options = FirefoxOptions()
    options.headless = True
    selenium_webdriver = Firefox(options=options)

    selenium_webdriver.get(WIKI_LINK)
    time.sleep(2)
    # chrome_driver.implicitly_wait(2)

    tables = selenium_webdriver.find_elements_by_xpath(
        "//table[contains(@class,'wikitable')]"
    )

    for table_index, table in tqdm(enumerate(tables)):
        table.find_element_by_xpath(
            "//table[contains(@class,'wikitable sortable')]//th[1]"
        ).click()
        time.sleep(2)

        table_header_element = table.find_element_by_tag_name("thead")
        table_body_element = table.find_element_by_tag_name("tbody")

        header = table_header_element.find_elements_by_tag_name("tr")
        header_data = extract_row_items(header[0])

        rows = table_body_element.find_elements_by_tag_name("tr")
        row_data = [extract_row_items(row) for row in tqdm(rows)]
        row_data = [i for i in row_data if i]
        import pandas as pd

        df = pd.DataFrame(row_data, columns=header_data)
        print(df)
        df.to_json(
            f"./{SAVE_NAME}_{table_index}.json",
            orient="records",
            indent=4,
            force_ascii=False,
        )


if __name__ == "__main__":
    _main()
