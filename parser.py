from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from io import StringIO


def find_titles(dr):
    """
    Finds all "title" class elements on the page
    :param dr: selenium driver
    :return: book_titles list
    """
    title_class_elements = dr.find_elements(by=By.CLASS_NAME, value="title")
    book_titles = []
    for ti in title_class_elements:
        book_titles.append(ti.get_attribute("textContent"))
    return book_titles


def description_dict(titles, page_text):
    """
    Makes a dictionary: {book_title: book_description} from titles list and all text on the page
    :param titles: list of book titles
    :param page_text: list of all "DIV" tagged elements text
    :return: dictionary {book_title: book_description}
    """

    title_content_dict = {}
    for title in titles:
        t = None
        for t in page_text:
            if title in t:
                break
        title_content_dict[title] = t
    return title_content_dict


def next_page_button(dr):
    """
    Finds a "Next Page" button by class name "button"
    :param dr: selenium driver
    :return: selenium element or None
    """
    button_class_elements = dr.find_elements(by=By.CLASS_NAME, value="button")
    for element in button_class_elements:
        if "Next Page" in element.text:
            return element
    return None


def dict_to_csv(dic):
    """
    Sends dic to StringIO in ['', 'title', 'description'] columns format (index, title, description)
    :param dic: {book_title: book_description} dictionary
    :return: csv like data string
    """
    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(['', 'title', 'description'])
    for i, (key, value) in enumerate(dic.items()):
        writer.writerow([i, key, value])
    data = out.getvalue()
    out.close()
    return data


def parse(link):
    """
    Gets url to be parsed (https://alwaysjudgeabookbyitscover.com/)
    :param link: can be any link, but works only with https://alwaysjudgeabookbyitscover.com/
    :return: csv like data string
    """
    driver = webdriver.Edge()
    driver.get(link)
    time.sleep(2)

    titles = []
    description_dictionary = {}
    button = next_page_button(driver)
    while True:
        titles = find_titles(driver)

        # find all book descriptions and excluding redundant elements
        text = list(set([text for text in list([div.text for div in driver.find_elements(by=By.TAG_NAME, value="DIV")
                                                if (div.text != '' and len(div.text) < 2000)])]))

        description_dictionary = description_dictionary | description_dict(titles, text)

        button = next_page_button(driver)

        if button is None:
            break

        button.click()
        time.sleep(3)

    driver.quit()
    return dict_to_csv(description_dictionary)
