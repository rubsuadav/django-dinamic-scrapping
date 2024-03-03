from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.http import HttpResponse
from urllib.parse import urlparse

# local imports
from local_settings import url


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


def validate_params(url):
    check_url = is_valid_url(url)
    if isinstance(check_url, HttpResponse):
        return check_url


def scrapping():
    validation_response = validate_params(url)
    if isinstance(validation_response, HttpResponse):
        return validation_response

    # Configuración de Selenium sin interfaz gráfica
    options = Options()
    options.add_argument("--headless")
    # Para evitar error 403 Forbidden
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Obtener todo el texto de la página
    body = driver.find_element(By.TAG_NAME, "body")

    # Excluir los elementos dentro de 'header' y 'footer'
    elements = body.find_elements(
        By.XPATH, f".//*[not(ancestor::header) and not(ancestor::footer)]")

    # Crear una lista para almacenar el texto de los elementos
    elements_text = []

    for element in elements:
        tag_name = element.tag_name
        if tag_name != "script" and tag_name != "iframe" and tag_name != "noscript" and tag_name != "style":
            elements_text.append(element.get_dom_attribute("class"))

    driver.quit()
    return HttpResponse(elements_text)
