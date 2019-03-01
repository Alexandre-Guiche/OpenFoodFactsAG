import requests
from Product import *
import mysql.connector


def create_db():
    mydb = mysql.connector.connect(host="***", user="***", passwd="***")
    file = open("Script.sql", 'r')
    query = file.readlines()
    cursor_db = mydb.cursor()
    for q in query:
        cursor_db.execute(q)


def fill_db():
    categories_dict = dict()
    mydb = mysql.connector.connect(host="***", user="***", passwd="***", database="***")
    pagenum = 1
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=10&page=' + str(pagenum) +
                     '&action=process&json=1').json()
    mycursor = mydb.cursor(buffered=True)
    sql = "INSERT INTO produit (Nom_P, Grade, Magasin) VALUES (%s, %s, %s)"
    for i in range(10):
        products, categories_list = make_product_list(10, r)
        for product, categories in zip(products, categories_list):
            val = (product.name, product.grade, product.stores)
            mycursor.execute(sql, val)
            product_code = mycursor.lastrowid
            for category in categories:
                category = category.replace('"', "'").replace("'", "").strip(" ")
                if category not in categories_dict:
                    mycursor.execute(
                        "INSERT INTO categorie (Nom_C) VALUES ('" + category + "');")
                    categories_dict[category] = mycursor.lastrowid
                    mycursor.execute(
                        'INSERT INTO categorie_produit (Code_P, ID_C) VALUES'
                        '(' + str(product_code) + ',' + str(mycursor.lastrowid) + ')')
                else:
                    mycursor.execute(
                        "SELECT ID_C from Categorie_produit where Code_P = " + str(product_code) + ";")
                    var = mycursor.fetchall()
                    if var is not None and categories_dict[category] not in var:
                        mycursor.execute(
                            'INSERT INTO categorie_produit (Code_P, ID_C) VALUES'
                            '(' + str(product_code) + ',' + str(categories_dict[category]) + ')')

        pagenum += 1
        r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=10&page=' + str(pagenum) +
                         '&action=process&json=1').json()


def make_product_list(size, r):
    prod_list = list()
    cat_list = list()
    for i in range(size):
        if r["products"][i] != '':
            if "product_name_fr" in r["products"][i] and r["products"][i]["product_name_fr"] != '':
                if "nutrition_grades" in r["products"][i] and r["products"][i]["nutrition_grades"] != '':
                    if "categories" in r["products"][i] and r["products"][i]["categories"] != '':
                        if "stores" in r["products"][i] and r["products"][i]["stores"] != '':
                            first_store = r["products"][i]["stores"].split(",")[0]
                            prod_list.append(Product(r["products"][i]["product_name_fr"],
                                                     r["products"][i]["nutrition_grades"],
                                                     first_store))
                            cat_list.append(r["products"][i]["categories"].split(","))
    return prod_list, cat_list


def main():
    create_db()
    fill_db()


main()
