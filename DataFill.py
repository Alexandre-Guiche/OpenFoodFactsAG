import requests
from Product import *
import mysql.connector


def create_db():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="")
    file = open("Script.sql", 'r')
    query = file.readlines()
    cursor_db = mydb.cursor()
    for q in query:
        cursor_db.execute(q)


def fill_db():
    categories_list = list()
    categories = dict()
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="off")
    pagenum = 1
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=10&page=' + str(pagenum) +
                     '&action=process&json=1').json()
    mycursor = mydb.cursor()
    sql = "INSERT INTO produit (Nom_P, Grade, Magasin) VALUES (%s, %s, %s)"
    for i in range(10):
        products = make_product_list(10, r)
        for j in range(len(products)):
            val = (products[j].name, products[j].grade, products[j].stores)
            mycursor.execute(sql, val)
            categories_list.append((r["products"][j]["categories"].split(",")))
            product_code = mycursor.lastrowid
            for li in categories_list:
                for category in li:
                    category = category.replace('"', "'").replace("'", "")
                    if category not in categories:
                        mycursor.execute(
                            "INSERT INTO categorie (Nom_C) VALUES ('" + category + "');")
                        categories[category] = mycursor.lastrowid
                        mycursor.execute(
                            'INSERT INTO categorie_produit (Code_P, ID_C) VALUES'
                            '(' + str(product_code) + ',' + str(mycursor.lastrowid) + ')')
        pagenum += 1
        r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=10&page=' + str(pagenum) +
                         '&action=process&json=1').json()


def make_product_list(size, r):
    liste = []
    for i in range(size):
        if r["products"][i] != '':
            if "product_name_fr" in r["products"][i] and r["products"][i]["product_name_fr"] != '':
                if "nutrition_grades" in r["products"][i] and r["products"][i]["nutrition_grades"] != '':
                    if "categories" in r["products"][i] and r["products"][i]["categories"] != '':
                        if "stores" in r["products"][i] and r["products"][i]["stores"] != '':
                            first_store = r["products"][i]["stores"].split(",")[0]
                            liste.append(Product(r["products"][i]["product_name_fr"],
                                                 r["products"][i]["nutrition_grades"],
                                                 first_store))
    return liste


def main():
    create_db()
    fill_db()


main()
