#MINI PROJECT 
from os import EX_PROTOCOL
from mysql_python import *
import csv

#Import / Export CSV format
def csv_write(opt):
    rows = select(opt)
    if (opt == "products"):
        header = ['product_id','name', 'price', 'active']
        file_name = "products.csv"
    elif (opt == "couriers"):
        header = ['courier_id','name', 'phone', 'active']
        file_name = "couriers.csv"
    elif (opt == "orders"):
#A view was created in the database (view_orders_producsts is a Inner Join of the orders and orders_products tables. )    
        rows = select("view_orders_products")   
        header = ['id','customer_name', 'customer_address', 'customer_phone', 'customer_id', 'status', 'product_id']
        file_name = "orders.csv"    
    fp = open(file_name,'w')
    csv_file = csv.writer(fp)
    csv_file.writerow(header)
    csv_file.writerows(rows)

#LIST (Product / Courier / Order)
def list_db(opt):
    if (opt == "products"):
        where = "active = 1"
        LIST = select(opt, where)
        if LIST:
            print("\n****** PRODUCT LIST ******")
            for x in LIST:
                print(f'''\nProduct ID: {x[0]}
Product Name: {x[1]} 
Product Price: £{x[2]} ''')
        else:
            print("\n****** PRODUCT LIST IS EMPTY! ******")
            menu(opt)
    
    elif (opt == "couriers"):
        where = "active = 1"
        LIST = select(opt, where)
        if LIST:
            print("\n****** COURIER LIST ******")
            for x in LIST:
                print(f'''\nCourier ID: {x[0]}
Courier Name: {x[1]}
Courier Phone: {x[2]} ''')
        else:
            print("\n****** COURIER LIST IS EMPTY! ******")
            menu(opt)

    elif (opt == "orders"):
        order_by = "courier_id DESC"    # LIST ORDERS BY COURIER 
        LIST = select(opt, order=order_by)
        if LIST: 
            print("\n****** ORDER LIST ******")
            for x in LIST:
                print(f'''\nOrder ID: {x[0]}
Customer Name: {x[1]}
Customer Address: {x[2]}
Customer Phone: {x[3]}
Courier: {x[4]}
Status: {x[5]}''')
                where = f'order_id = {x[0]} '
                order_prod = select("orders_products", where)
                for prod in order_prod:
                    print(f'Product ID: {prod[1]}')
        else:
            print("\n****** ORDER LIST IS EMPTY! ******")
            menu_order(opt) 

    elif (opt == "order_status" ):
        LIST = select(opt)
        print("\n****** ORDER STATUS ******")
        for x in LIST:
            print(f'''Status ID: {x[0]}
Status: {x[1]}\n''')      

#INSERT (Product / Courier / Order)
def add(opt):   
    if (opt == "products"):
        print("\n****** NEW PRODUCT ******")
        name = input("Insert the product name: ")
        price = float(input("Insert the product price: "))
        att = f'"{name}", {price}' 
        insert(opt, "name, price", att)

    elif (opt == "couriers"):
        print("\n****** NEW COURIER ******")
        name = input("Insert the courier name: ")
        phone = int(input("Insert the courier phone: "))
        att = f'"{name}", {phone}' 
        insert(opt, "name, phone", att)

    elif (opt == "orders"):
        print("\n****** NEW ORDER ******")
        customer_name = input("Insert the customer name: ")
        customer_address = input("Insert the customer address: ")
        customer_phone = input("Insert the customer phone: ")
        list_db("products")
        prods_id = input("\nInput the products ID separated for comma: ")
        prods_id = list(map(int, prods_id.split(",")))
    
        list_db("couriers")
        courier = int(input("\nInput the the Curier ID: "))
        status = "Preparing"
        
        column = "customer_name, customer_address, customer_phone, courier_id, status"
        att = f'"{customer_name}", "{customer_address}", {customer_phone}, {courier}, "{status}"'
        order_id = insert(opt, column, att)
        for p in prods_id:
            att = f'"{order_id}", "{p}"'
            insert("orders_products", "order_id, product_id", att)    

#UPDATE (Product / Currier / Order) 
def update_app(opt):
    if (opt == "products"):
        list_db(opt)
        products_id = int(input("\nInput the Product ID you want to update: ")) 
        print("""\n****************************************
Leave blank if you don't want to update.
****************************************""")
        name = input("\nUpdate New Product Name: ")
        price = input("Update New Product Price: ")
        if name:
            att = f'name="{name}"'
            where = f'product_id={products_id}'
            update(opt, att, where)
        if price:
            att = f'price="{price}"'
            where = f'product_id={products_id}'
            update(opt, att, where)
    
    elif(opt == "couriers"):
        list_db(opt)
        courier_id = int(input("\nInput the Courier ID you want to update: "))
        print("""\n****************************************
Leave blank if you don't want to update.
****************************************""")
        name = input("\nUpdate New Courier Name: ")
        phone = input("Update New Courier Phone: ")
        where = f'courier_id ={courier_id}'
        if name:
            att = f'name="{name}"'
            update(opt, att, where)
        if phone:
            phone_int = int(phone) 
            att = f'phone="{phone_int}"'
            update(opt, att, where)     
    
    elif (opt == "orders"):   
        list_db(opt)         #Show the order list with the index
        order_id = int(input("\nInput the Order ID you want to update: "))    
        print("""\n****************************************
Leave blank if you don't want to update!
****************************************""")
        customer_name = input("\nUpdate New Customer Name: ")
        customer_address = input("Update New Customer Address: ")
        customer_phone = input("Update New Customer Phone: ")
        
        list_db("couriers")  #Show the courier list with the index
        print("""\n****************************************
Leave blank if you don't want to update!
****************************************""")
        courier = input("\nInsert the Courier ID: ")
        
        list_db("products")
        print("""\n****************************************
Leave blank if you don't want to update!
****************************************""")
        prods_id = input("\nInput the products ID separated for comma: ")
        
        where = f'id ={order_id}'
        if customer_name:
            att = f'customer_name="{customer_name}"'
            update(opt, att, where)    
        if customer_address:
            att = f'customer_address="{customer_address}"'
            update(opt, att, where) 
        if customer_phone:
            phone_int = int(customer_phone)
            att = f'customer_phone="{phone_int}"'
            update(opt, att, where)
        if courier:
            courier_int = int(courier)
            att = f'courier_id="{courier_int}"'
            update(opt, att, where)
        if prods_id:
            prods_id = list(map(int, prods_id.split(",")))
            where_del = f'order_id={order_id}'
            delete_db ("orders_products", where_del)
            for p in prods_id:
                att = f'"{order_id}", "{p}"'
                insert("orders_products", "order_id, product_id", att)  

#UPDATE Order Status 
def update_order_status(opt):
    list_db(opt)         #Show the list with the index
    order_id = int(input("\nInput the Order ID you want to update the Status: "))
    
    list_db("order_status")
    status_id = int(input("Input the Status ID you want to update: "))
    
    where_status = f'status_id={status_id}'
    status = select("order_status",where_status)
    
    where = f'id ={order_id}'
    att = f'status="{status[0][1]}"'
    update(opt, att, where)
    
#DELETE (Products / Couriers / Orders)    
def delete(opt):
    if (opt == "products"):
        list_db(opt)   #Show the product list with the index 
        products_id = int(input("\nInput the Product ID you want to delete: ")) 
        att = f'active=0'
        where = f'product_id={products_id}'
        update(opt, att, where)
    elif (opt == "couriers"):
        list_db("couriers")  #Show the courier list with the index    
        couriers_id = int(input("\nInput the Courier ID you want to delete: ")) 
        att = f'active=0'
        where = f'courier_id ={couriers_id}'
        update(opt, att, where)
    elif (opt == "orders"): 
        list_db("orders")  #Show the order list with the index    
        y = int(input("\nInput the Order ID you want to delete: ")) 
        where = f'id ={y}'
        delete_db (opt, where)

#MENU OPTIONS (Products / Curier)   
def menu(opt):    
    sub_op = 1
    if (opt == "products"):
        m ="Product"
    elif(opt == "couriers"):
        m = "Courier"
    try:
        while (sub_op !=0):
            sub_op = int(input("""\n
****** %s Menu ******
0 - Return to Main Menu 
1 - Print %ss List
2 - Insert a New %s
3 - Update a Existing %s
4 - Delete a %s 
**************************
Input the option: """ %(m,m,m,m,m)))          
            if (sub_op == 0):    
                main_menu()
            elif (sub_op == 1):
                list_db(opt)
            elif (sub_op == 2):
                add(opt)
            elif (sub_op == 3):
                update_app(opt)
            elif (sub_op == 4):
                delete(opt)       
            else:     
                print("\nInvalid Option")
                menu(opt)
    except ValueError:
        print("\nInvalid Option") 
        menu(opt)   

#MENU OPTIONS (Orders)
def menu_order(opt):    
    sub_op = 1      
    try:   
        while (sub_op !=0):
            sub_op = int(input("""\n
****** Order Menu ******
0 - Return to Main Menu 
1 - Print Orders List
2 - Insert a New Order
3 - Update a Existing Order Status
4 - Update a Existing Order
5 - Delete a Order
************************* 
Input the option: """))          
            if (sub_op == 0):    
                main_menu()
            elif (sub_op == 1):
                list_db(opt)
            elif (sub_op == 2):
                add(opt)
            elif (sub_op == 3):
                update_order_status(opt)
            elif (sub_op == 4):   
                update_app(opt)
            elif (sub_op == 5):
                delete(opt)       
            else:     
                print("\nInvalid Option")
                menu(opt)
    except ValueError:
            print("\nInvalid Option") 
            menu(opt) 

#PRINT Main Menu Options 
def main_menu():
    op = 1
    try:
        while (op == 1):
            op = int(input("""
****** MAIN MENU ****** 
0 - Exit App
1 - Products Menu  
2 - Couriers Menu
3 - Orders
***********************
Input the option: """))
            if (op == 1):  
                menu("products")
            elif (op == 2):
                menu("couriers")    
            elif (op == 3):
                menu_order("orders")
            elif (op == 0):
                csv_write("products")
                csv_write("couriers")
                csv_write("orders")
                exit()
            else:     
                print("\nInvalid Option")
                main_menu()   
    except ValueError:
        print("\nInvalid Option")
        main_menu()    

main_menu()