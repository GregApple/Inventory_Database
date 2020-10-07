from collections import OrderedDict
import csv
import datetime
import sys

from peewee import *

db = SqliteDatabase('inventory.db')
    
class Product (Model):
    product_id = IntegerField(primary_key=True, unique=True)
    product_name = CharField(max_length=60, unique=True)
    product_quantity = IntegerField(default=1)
    product_price = IntegerField(default=1)
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
##    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Product], safe=True)
  

def menu_loop():
##    """Create a function to handle interaction with the user of your app.
##    This function should prompt the user to enter v in order to view the details of a single product in the database,
##    a to add a new product to the database, or b to make a backup of the entire contents of the database."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
    
        if choice in menu:
            menu[choice]()
        elif choice == 'q':
            print("")
        else:
            print("You have made an invalid selection. Please enter 'a', 'v', or 'b'. \n")
  

def upload_database():
    with open('inventory.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            try:
                Product.create(product_name = str(row['product_name']),    
                product_price = int(float(row['product_price'][1:])*100),
                product_quantity = int(row['product_quantity']),
                date_updated = datetime.datetime.strptime(row['date_updated'],"%m/%d/%Y").strftime("%m/%d/%Y"))
            except IntegrityError:
                product_record = Product.get(product_name=str(row['product_name']))
                product_record.product_price = int(float(row['product_price'][1:])*100)
                product_record.product_quantity = int(row['product_quantity'])
                product_record.date_updated = datetime.datetime.strptime(row['date_updated'],"%m/%d/%Y").strftime("%m/%d/%Y")
                product_record.save()

  
def add_product():
    """Add a new product to the database."""
##    """Create a function to handle adding a new product to the database. This function should prompt the user to enter the product's name, quantity, and price.
##    The function must process the user provided value for price from a string to an int.
##    Be sure the value you stored for the price field to the database is converted to cents ($2.99 becomes 299, for example)."""
    try:
        eproduct_name = str(input("\nPlease enter the product name. \n"))
        try:    
            eproduct_price = int(float(input("Please enter the product price without a dollar sign. \n"))*100)
            try:    
                eproduct_quantity = int(input("Please enter the product quantity. \n"))
                try:                   
                    Product.create(product_name = eproduct_name, product_price = eproduct_price, 
                                   product_quantity = eproduct_quantity, 
                                   date_updated = datetime.datetime.now().strftime("%m/%d/%Y"))
                except IntegrityError:
                    product_record = Product.get(product_name=eproduct_name)
                    product_record.product_price = int(eproduct_price)
                    product_record.product_quantity = int(eproduct_quantity)
                    product_record.date_updated = datetime.datetime.now().strftime("%m/%d/%Y")
                    product_record.save()
            except ValueError:
                print("The format you used to enter the product quantity is invalid. \n")
        except ValueError:
            print("You used an invalid format to enter the product price. \n")
    except ValueError:
        print("You entered an invalid product name. \n")
  
def view_product():
    """View a product by its product_id."""
##    """Create a function to handle getting and displaying a product by its product_id."""
    try:
        product_record = Product.get(product_id=input("Please enter a product id. \n"))
        print("\n  Product ID: ", product_record.product_id, " \n ", "Product Name: ", product_record.product_name, " \n ", "Product Price: ", product_record.product_price,
              " \n ", "Product Quantity: ", product_record.product_quantity," \n ", "Date Updated: ", product_record.date_updated, " \n ")
    except Product.DoesNotExist:
        print("You entered an invalid number. Please try again.\n")
    except ValueError:
        print("The value you provided is not a valid product id. Please lookup you product id and try again.\n")


def backup_database():
    """Backup the database."""
##    """Create a function to handle making a backup of the database. The backup should be written to a .csv file."""
    with open('backup.csv', 'w') as csv_file:
        fieldnames = ['product_id', 'product_name', 'product_price', 'product_quantity', 'date_updated']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

        product = Product.select().dicts()
        writer.writeheader()
        for row in product:
            writer.writerow({'product_id': row['product_id'],
                            'product_name': row['product_name'],
                            'product_price': row['product_price'],
                            'product_quantity': row['product_quantity'],
                            'date_updated': row['date_updated']})


menu = OrderedDict([
    ('a', add_product),
    ('v', view_product),
    ('b', backup_database),
  ])  
  
if __name__ == '__main__':
    initialize()
    upload_database()
    menu_loop()

