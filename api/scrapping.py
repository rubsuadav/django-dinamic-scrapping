from selenium import webdriver
from selenium.webdriver.common.by import By
from django.http import HttpResponse
from urllib.parse import urlparse

# local imports
from local_settings import url, tags


def validate_url(url):
    if not isinstance(url, str):
        return HttpResponse("Error: El atributo 'url' no es válido, debe de ser una url, o una lista de urls, o un diccionario de urls.")
    else:
        try:
            result = urlparse(url)
            url = result.geturl()
            return True
        except ValueError:
            return HttpResponse("Error: El atributo 'url' no es válido, debe de ser una url, o una lista de urls, o un diccionario de urls.")


def is_valid_url(url):
    if isinstance(url, str):
        return validate_url(url)
    elif isinstance(url, list):
        return all(validate_url(u) for u in url)
    elif isinstance(url, dict):
        return all(validate_url(u) for u in url.values())
    else:
        return False


def validate_params(url, tags):
    check_url = is_valid_url(url)
    if isinstance(check_url, HttpResponse):
        return check_url
    elif not (isinstance(tags, list) or isinstance(tags, str)):
        return HttpResponse("Error: El atributo 'tags' no es válido")


def scrapping():
    validation_response = validate_params(url, tags)
    if isinstance(validation_response, HttpResponse):
        return validation_response

    driver = webdriver.Chrome()
    driver.get(url)

    # Obtener todo el texto de la página
    root = driver.find_element(By.TAG_NAME, "body").tag_name
    elements = driver.find_elements(By.TAG_NAME, root)
    for element in elements:
        tag_name = element.tag_name
        if tag_name != 'header' and tag_name != "footer":
            for tag in tags:
                print(tag)
                try:
                    main_element = element.find_element(By.TAG_NAME, tag)
                    return HttpResponse(main_element.text)
                except:
                    continue
    driver.quit()
