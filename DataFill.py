import requests
from product import *
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="off")
pagenum = 1
r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=10&page=' + str(pagenum) +
                 '&action=process&json=1').json()


def make_product_list(size):
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
                                                 first_store,
                                                 r["products"][i]["categories"]))

    return liste


mycursor = mydb.cursor()
sql = "INSERT INTO produit (Nom_P, Grade, Magasin) VALUES (%s, %s, %s)"
for j in range(10):
    for produit in make_product_list(10):
        val = (produit.name, produit.grade, produit.stores)
        mycursor.execute(sql, val)
    pagenum += 1
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=10&page=' + str(pagenum) +
                     '&action=process&json=1').json()
