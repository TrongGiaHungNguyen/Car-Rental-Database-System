import sqlActions

def taskOptions():
    print("\nTasks:")
    print("1. Change address")
    print("2. Car models list")
    print("3. Declare car models")

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


def login(conn, cur):
    query = """
        SELECT * FROM DRIVER
        WHERE driver_name = %s;
        """
    
    name = ""
    isCorrect = False
    while (not isCorrect):
        name = input("\nEnter your name to log-in or 'quit' to quit: ").strip()

        if (name == 'quit'):
            break

        queryResult = sqlActions.fetchOneData(cur, query, [name])

        if (queryResult is None):
            print("Name not found! Please enter again.")
        else:
            isCorrect = True

    if (not isCorrect):
        return ""
    
    return name


def command1(conn, cur, info):
    print("\nEnter your new address:")
    address_number = input("Address number: ")
    road_name = input("Road name: ")
    city = input("City: ")
    
    query = """
        UPDATE DRIVER
        SET address_number = %s, road_name = %s, city = %s
        WHERE driver_name = %s;
        """
    
    sqlActions.modifyData(conn, cur, query, [address_number, road_name, city, info])


def command2(conn, cur):
    print("\nCar model lis: ")
    query = """
        SELECT * FROM MODEL;
        """
    
    queryResult = sqlActions.fetchAllData(cur, query)
    for i, item in enumerate(queryResult):
        print(f"{i + 1}. {item[0]} {item[1]} {item[2]} {item[3]} {item[4]}")


def command3(conn, cur, info):
    print("\nEnter car information: ")
    modelID = input("Model ID: ")
    carID = input("Car ID: ")

    query = """
        INSERT INTO DRIVE (model_id, car_id, driver_name) VALUES (%s, %s, %s);
        """
    
    sqlActions.modifyData(conn, cur, query, [modelID, carID, info])


def main_driver(conn, cur):
    info = login(conn, cur)
    if (info == ""):
        return

    userInput = ""
    while (userInput != 'x'):
        taskOptions()
        userInput = input("Enter a task number or 'x' to exit: ")

        if (userInput == '1'):
            command1(conn, cur, info)
        elif (userInput == '2'):
            command2(conn, cur)
        elif (userInput == '3'):
            command3(conn, cur, info)