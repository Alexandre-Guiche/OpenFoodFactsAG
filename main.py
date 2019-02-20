import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="off")


def select_product():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM categorie")
    categories = mycursor.fetchall()
    for cat in categories:
        print(cat)
    id_cat = input("Select a category (ID): ")
    mycursor.execute("SELECT * FROM categorie WHERE ID_C = " + id_cat)
    cat = mycursor.fetchone()
    print("Products in category '" + str(cat[1]) + "' :")
    mycursor.execute(
        "SELECT produit.Code_P, Nom_P FROM produit NATURAL JOIN categorie_produit where ID_C = " + str(cat[0]))
    products = mycursor.fetchall()
    for product in products:
        print(product)
    return substitute(input("Select a product (ID): "), str(cat[0]))


def substitute(id_product, category):
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT produit.Code_P, Nom_P, Grade FROM produit NATURAL JOIN categorie_produit where ID_C = " + category +
        " ORDER BY Grade ASC")
    best_product = mycursor.fetchone()
    if str(best_product[0]) <= id_product:
        return "This product is already the best in this category"
    else:
        return "The best product in this category is : " + best_product[1] + ", With a nutrition grade of " + \
               best_product[2]


if __name__ == '__main__':
    print("1- Substitute an aliment")
    print("2- Find substituted aliment")
    var = int(input())
    if var == 1:
        print(select_product())
    elif var == 2:
        # find_substitute()
        pass
