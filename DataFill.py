"""
This module is in charge of Database intarractions
"""


import mysql.connector
import api

MYDB = mysql.connector.connect(host="localhost", user="root", passwd="", database="off")


def create_db():
    """
    This function reads the given .sql file to create the database
    """
    file = open("Script.sql", 'r')
    querries = file.readlines()
    cursor_db = MYDB.cursor()
    for query in querries:
        cursor_db.execute(query)


def fill_db():
    """
    This function sends a request to the OpenFoodFacts API to get a Json file,
    containing various products,
    then calls make_product_list() to parse the list,
    and insert every item in it in the database
    """
    categories_dict = dict()
    mycursor = MYDB.cursor(buffered=True)
    sql = "INSERT INTO produit (Nom_P, Grade, Magasin) VALUES (%s, %s, %s)"
    products, categories_list = api.make_product_list(100)
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
                    "SELECT ID_C from Categorie_produit where Code_P = "
                    + str(product_code) + ";")
                var = mycursor.fetchall()
                if var is not None and categories_dict[category] not in var:
                    mycursor.execute(
                        'INSERT INTO categorie_produit (Code_P, ID_C) VALUES'
                        '(' + str(product_code) + ',' + str(categories_dict[category]) + ')')


def main():
    """
    main function
    """
    create_db()
    fill_db()


main()
