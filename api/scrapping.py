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
    elif not (isinstance(tags, list)):
        return HttpResponse("Error: El atributo 'tags' no es válido")


def scrapping():
    validation_response = validate_params(url, tags)
    if isinstance(validation_response, HttpResponse):
        return validation_response

    driver = webdriver.Chrome()
    driver.get(url)

    # Obtener todo el texto de la página
    body = driver.find_element(By.TAG_NAME, "body")

    # Excluir los elementos dentro de 'header' y 'footer'
    elements = body.find_elements(
        By.XPATH, f".//*[not(ancestor::header) and not(ancestor::footer)]")

    for element in elements:
        for tag in tags:
            print(element.tag_name)
            if element.tag_name == tag:
                return HttpResponse(element.text)

    driver.quit()
