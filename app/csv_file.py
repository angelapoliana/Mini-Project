import csv
def read_csv(file_name):
    LIST = []
    try:
        with open(file_name, "r") as file:
            csv_file = csv.DictReader(file)  #Read a CSV file as a dictionary 
            for row in csv_file:
                LIST.append(row)
    except FileNotFoundError:
        with open((file_name), 'w') as file:    
            LIST=[]
    finally:
        return LIST    
        
def write_csv(list, opt):
    field_prod = ['name', 'price']
    field_courier = ['name', 'phone']
    field_order = ['customer_name', 'customer_address', 'customer_phone', 'courier', 'status', 'items']
    
    if(opt == "prod"):
        fieldnames = field_prod
        file_name = "products.csv"
    elif(opt == "courier"):
        fieldnames = field_courier
        file_name = "couries.csv"
    elif(opt == "order"):
        fieldnames = field_order
        file_name = "orders.csv"
    
    if list:    
        with open(file_name, mode="w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for x in list:
                writer.writerow(x)
    else:
        with open((file_name), 'w') as file:            
            LIST=[]
        




