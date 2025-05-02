import re
import sqlActions

def login_signup():
    userChoice = ""
    while (userChoice != "1" and userChoice != "2"):
        userChoice = input("\nChoose (1) to log-in or (2) to sign-up: ")

        userChoice = userChoice.strip()
        if (userChoice != "1" and userChoice != "2"):
            print("ERROR: Invalid input! Please enter again.")
    
    if userChoice == "1":
        return "login"
    return "signup"


def is_valid_ssn(ssn):
    pattern = r"^\d{3}-\d{2}-\d{4}$"
    return bool(re.match(pattern, ssn))


def signup(conn, cur):
    isValid = False

    name = ""
    ssn = ""
    email = ""
    while (not isValid):
        print("Please enter the required information: ")
        name = input("Full name: ").strip()
        ssn = input("SSN (xxx-xx-xxxx): ").strip()
        email = input("Email: ").strip()

        if (name == ""):
            print("[_ERROR_]: Name cannot be empty. Please enter again.\n")
        elif (ssn == ""):
            print("[_ERROR_]: SSN cannot be empty. Please enter again.\n")
        elif (not is_valid_ssn(ssn)):
            print("[_ERROR_]: SSN is not in a valid format. Please enter again.\n")
        elif (email == ""):
            print("[_ERROR_]: Email cannot be empty. Please enter again.\n")
        else:
            isValid = True

    query = "INSERT INTO MANAGER (manager_name, ssn, manager_email) VALUES (%s, %s, %s)"
    sqlActions.modifyData(conn, cur, query, [name, ssn, email])
    print("Sign-up successfull!")


def login(cur):
    isCorrect = False

    print("Please enter your SSN to log-in or 'quit' to quit:")
    while (not isCorrect):
        userInput = input("SSN: ").strip()

        if (userInput.lower() == "quit"):
            break

        query = """
            SELECT * FROM MANAGER
            WHERE ssn = %s
            """
        cur.execute(query, (userInput,))
        result = cur.fetchone()

        if (result is None):
            print("Incorect SSN. Pleaes enter again.\n")
        else:
            print("Login successful.")
            isCorrect = True
    
    return isCorrect


def taskOptions():
    print("\nTasks:")
    print("1. Insert/remove cars or model")
    print("2. Insert/remove drivers")
    print("3. Top-k clients")
    print("4. List all car models")
    print("5. List all drivers")
    print("6. Find client based on city")
    print("x. Exit")


def add_car(conn, cur):
    print("\nEnter car information:")
    brand = input("Brand name: ").strip()
    carid = input("Car ID: ").strip()

    query = """
        INSERT INTO CAR (brand, car_id) VALUES (%s, %s)
        """
    sqlActions.modifyData(conn, cur, query, [brand, carid])
    print("Car added succfully!")


def remove_car(conn, cur):
    isValid = False
    deleteBy = ""
    while (not isValid):
        deleteBy = input("\nDelete by: car_id (1) or brand (2): ").strip().lower()

        if (deleteBy != "1" and deleteBy != "2" and deleteBy != "car_id" and deleteBy != "brand"):
            print("__ERROR__: Invalid input. Please enter again.")
        else:
            isValid = True
    
    if (deleteBy == "1" or deleteBy == "car_id"):
        validCarID = False
        car_id = ""
        while (not validCarID):
            car_id = input("\nEnter car_id to delete: ").strip().lower()
            
            if (not car_id.isdigit() or len(car_id) != 5):
                print("__ERROR__: Invalid car_id. Please enter again.")
            else:
                validCarID = True
        
        query1 = """
            DELETE FROM CAR WHERE car_id = %s
            """
        query2 = """
            DELETE FROM MODEL WHERE car_id = %s
            """
        
        sqlActions.modifyData(conn, cur, query2, [car_id])
        sqlActions.modifyData(conn, cur, query1, [car_id])
    else:
        notEmpty = False
        brand = ""
        while (not notEmpty):
            brand = input("\nEnter car brand to delete: ").strip()
            
            if (brand == ""):
                print("__ERROR__: Brand name cannot be empty. Please enter again.")
            else:
                notEmpty = True
        
        query1 = """
            SELECT DISTINCT car_id FROM CAR WHERE brand = %s
            """
        query2 = """
            DELETE FROM CAR WHERE brand = %s
            """
        
        sqlResult_IDs = sqlActions.fetchAllData(cur, query1, [brand])
        placeHolders = ','.join(['%s'] * len(sqlResult_IDs))

        removedIDs = []
        for item in sqlResult_IDs:
            removedIDs.append(item[0])
        
        query3 = f"""
            DELETE FROM MODEL WHERE car_id in ({placeHolders})
            """
        sqlActions.modifyData(conn, cur, query3, removedIDs)
        sqlActions.modifyData(conn, cur, query2, [brand])
        
    print("Delete car(s) successfully!") 


def add_model(conn, cur):
    print("\nEnter model information:")
    model_id = input("Model ID: ").strip()
    car_id = input("Associated car_id (5 digits): ").strip()
    color = input("Color: ").strip()
    year = input("Construction year: ").strip()
    type = input("Tranmission type: ").strip()
    
    query = "INSERT INTO MODEL (model_id, car_id, color, construction_year, transmission_type) VALUES (%s, %s, %s, %s, %s)"
    sqlActions.modifyData(conn, cur, query, [model_id, car_id, color, year, type])


def remove_model(conn, cur):
    model_id = input("\nEnter model_id to remove: ")
     
    query = """
        DELETE FROM MODEL WHERE model_id = %s
        """
    sqlActions.modifyData(conn, cur, query, [model_id])


def command1(conn, cur):
    isValidInput = False
    while (not isValidInput):
        print("\nEnter your action: ")
        action = input("Insert(1) / remove(2): ").strip().lower()
        object = input("Car(1) / Model(2): ").strip().lower()

        if (action != "1" and action != "2" and action != "insert" and action != "remove"):
            print("__ERROR__: Invalid action. Please enter again.\n")
        elif (object != "1" and object != "2" and object != "car" and object != "model"):
            print("__ERROR__: Invalid action. Please enter again.\n")
        else:
            isValidInput = True
        
    if (object == "1" or object == "car"):
        if (action == "1" or action == "insert"):
            add_car(conn, cur)
        else:
            remove_car(conn, cur)
    else:
        if (action == "1" or action == "insert"):
            add_model(conn, cur)
        else:
            remove_model(conn, cur)


def add_driver(conn, cur):
    print("\nEnter driver information:")
    name = input("Driver name: ")
    print("Address information:")
    addNum = input("Address number: ")
    roadName = input("Road name: ")
    city = input ("City: ")

    query = """
        INSERT INTO DRIVER (driver_name, address_number, road_name, city) VALUES (%s, %s, %s, %s)
        """

    sqlActions.modifyData(conn, cur, query, [name, addNum, roadName, city])


def remove_driver(conn, cur):
    name = input("\nEnter name of driver to remove: ")

    query = """
        DELETE FROM DRIVER WHERE driver_name = %s
        """
    
    sqlActions.modifyData(conn, cur, query, [name])
        
def command2(conn, cur):
    isValidInput = False
    action = ""
    while (not isValidInput):
        print("\nEnter your action: ")
        action = input("Insert(1) / remove(2): ").strip().lower()

        if (action != "1" and action != "2" and action != "insert" and action != "remove"):
            print("__ERROR__: Invalid action. Please enter again.\n")
        else:
            isValidInput = True
    
    if (action == "1" or action == "insert"):
        add_driver(conn, cur)
    else:
        remove_driver(conn, cur)
    

def command3(conn, cur):
    k = input("\nEnter K: ")

    query = """
        SELECT CLIENT.client_name, CLIENT.client_email, COUNT(RENT.rent_id) as numRent FROM client
        JOIN RENT ON RENT.client_email = CLIENT.client_email
        GROUP BY CLIENT.client_email
        ORDER BY numRent DESC
        LIMIT %s;
        """
    
    queryResult = sqlActions.fetchAllData(cur, query, [k])
    print(f"\nTop {k} client with the most trips booked: ")
    for i, item in enumerate(queryResult):
        print(f"{i + 1}. Name: {item[0]} - Email: {item[1]}")


def command4(conn, cur):
    query1 = """
        SELECT MODEL.car_id, MODEL.model_id, color, transmission_type, construction_year FROM MODEL;
        """

    query2 = """
        SELECT COUNT(*) FROM RENT
        WHERE car_id = %s and model_id = %s
        """

    allModels = sqlActions.fetchAllData(cur, query1)
    
    print("\nCar model list:")
    for i, item in enumerate(allModels):
        numUsed = sqlActions.fetchOneData(cur, query2, [item[0], item[1]])
        print(f"{i + 1}. {item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {numUsed[0]}")


def command5(conn, cur):
    query1 = """
        SELECT driver_name FROM DRIVER;
        """
    
    query2 = """
        SELECT COUNT(*) FROM RENT
        WHERE driver_name = %s
        """
    
    query3 = """
        SELECT SUM(rating) / COUNT(*) FROM REVIEW
        WHERE driver_name = %s
        """
    
    driverNames = sqlActions.fetchAllData(cur, query1)

    print("\n Driver list:")
    for i, item in enumerate(driverNames):
        numRent = sqlActions.fetchOneData(cur, query2, [item[0]])
        avgRating = sqlActions.fetchOneData(cur, query3, [item[0]])

        if (avgRating[0] is None):
            avgRating = ('N/A',)

        print(f"{i + 1}. {item[0]} {numRent[0]} {avgRating[0]}")


def command6(conn, cur):
    query = """
        SELECT CLIENT.client_name, CLIENT.client_email, COUNT(*) FROM CLIENT
        JOIN RENT ON RENT.client_email = CLIENT.client_email
        JOIN DRIVER ON RENT.driver_name = DRIVER.driver_name
        JOIN LIVE ON CLIENT.client_email = LIVE.client_email
        WHERE LIVE.city = %s AND DRIVER.city = %s
        GROUP BY CLIENT.client_email;
        """

    city1 = input("Client's city: ")
    city2 = input("Driver's city: ")

    queryResult = sqlActions.fetchAllData(cur, query, [city1, city2])

    print("\nResult")
    for i, item in enumerate(queryResult):
        print(f"{i + 1}. {item[0]} {item[1]}")


def tasks(conn, cur):
    userInput = ""
    while (userInput != "x"):
        taskOptions()
        userInput = input("Enter a task number or 'x' to exit: ")

        if (userInput == "1"):
            command1(conn, cur)
        elif (userInput == "2"):
            command2(conn, cur)
        elif (userInput == "3"):
            command3(conn, cur)
        elif (userInput == "4"):
            command4(conn, cur)
        elif (userInput == "5"):
            command5(conn, cur)
        elif (userInput == "6"):
            command6(conn, cur)


def main_manager(conn, cur):
    if (login_signup() == "signup"):
        signup(conn, cur)
    else:
        isSuccess = login(cur)

        if (not isSuccess):
            return
        else:
            tasks(conn, cur)
        
