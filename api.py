"""
This module is in charge of API interractions
"""

import requests
from Product import Product

REQUEST = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=100&page='
                       '1&action=process&json=1').json()


def make_product_list(size):
    """
    This function takes two parameters : the desired size of the product list,
    and a json file containing products.
    It then reads every product in the file and transform it into a Python object,
    and put it in a list
    """
    prod_list = list()
    cat_list = list()
    for i in range(size):
        if REQUEST["products"][i] != '':
            if "product_name_fr" in REQUEST["products"][i] and \
                    "nutrition_grades" in REQUEST["products"][i] and \
                    "categories" in REQUEST["products"][i] and \
                    "stores" in REQUEST["products"][i]:
                if REQUEST["products"][i]["product_name_fr"] != '' and \
                        REQUEST["products"][i]["nutrition_grades"] != '' and \
                        REQUEST["products"][i]["categories"] != '' and \
                        REQUEST["products"][i]["stores"] != '':
                    first_store = REQUEST["products"][i]["stores"].split(",")[0]
                    prod_list.append(Product(REQUEST["products"][i]["product_name_fr"],
                                             REQUEST["products"][i]["nutrition_grades"],
                                             first_store))
                cat_list.append(REQUEST["products"][i]["categories"].split(","))
    return prod_list, cat_list
