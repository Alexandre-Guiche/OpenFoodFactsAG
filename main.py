import mysql.connector

mydb = mysql.connector.connect(host="****", user="****", passwd="****", database="****")


def register_substitution(id_product, id_substitute, category):
    mycursor = mydb.cursor()
    var = input("Do you wish to register that product substitution? Y/N")
    if var == "Y" or var == "y":
        mycursor.execute("select * from substituer where code_P_demande = " + id_product +
                         " AND code_P_substitut = " + id_substitute)
        rows = mycursor.fetchall()
        if not rows:
            mycursor.execute("INSERT INTO Substituer VALUES "
                             "(" + id_product + ", " + id_substitute + ", " + category + ")")
            print("Done!")
        else:
            print("substitution already registered")


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
    substitute(input("Select a product (ID): "), str(cat[0]))


def substitute(id_product, category):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT produit.Code_P, Nom_P, Grade FROM produit NATURAL JOIN categorie_produit where ID_C = " + category +
        " ORDER BY Grade ASC")
    best_product = mycursor.fetchone()
    if str(best_product[0]) == id_product:
        print("This product is already (one of) the best in this category")
    else:
        print("The best product in this category is : " + best_product[1] + ", With a nutrition grade of " +
              best_product[2])
        register_substitution(id_product, str(best_product[0]), category)


def find_substitute():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT Produit1.Nom_P, Produit2.Nom_P, Nom_C FROM Substituer "
                     "JOIN produit AS Produit1 ON Code_P_demande = Produit1.Code_P "
                     "JOIN produit AS produit2 ON Code_P_substitut = Produit2.Code_P "
                     "JOIN Categorie ON categorie = Categorie.ID_C")
    var = mycursor.fetchall()
    for sub in var:
        print(sub[0] + ", à remplacer par " + sub[1] + " dans la catégorie " + sub[2])


def main():
    print("1- Substitute an aliment")
    print("2- Find substituted aliment")
    print("3- Exit")
    var = int(input())
    if var == 1:
        select_product()
    elif var == 2:
        find_substitute()
    elif var == 3:
        exit()
    main()


if __name__ == '__main__':
    main()
