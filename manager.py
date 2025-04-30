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
    sqlActions.action_insert(conn, cur, query, [name, ssn, email])
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
    print("1. Add/remove a car or a model")
    print("x. Exit")


def add_car(conn, cur):
    isValid = False
    
    while (not isValid):
        print("\nEnter car information:")
        brand = input("Brand name: ").strip()
        carid = input("Car ID (5 digits): ").strip()

        if (brand == ""):
            print("[_ERROR_]: Brand name cannot be empty. Please enter again.")
        elif (not carid.isdigit() or len(carid) != 5):
            print("[_ERROR_]: Invalid car id. Please enter again.")
        else:
            isValid = True

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
            print("[_ERROR_]: Invalid input. Please enter again.")
        else:
            isValid = True
    
    if (deleteBy == "1" or deleteBy == "car_id"):
        validCarID = False
        car_id = ""
        while (not validCarID):
            car_id = input("\nEnter car_id (5 digits) to delete: ").strip().lower()
            
            if (not car_id.isdigit() or len(car_id) != 5):
                print("[_ERROR_]: Invalid car_id. Please enter again.")
            else:
                validCarID = True
        
        query = """
            DELETE FROM CAR WHERE car_id = %s
            """
        
        sqlActions.modifyData(conn, cur, query, [car_id])
    else:
        notEmpty = False
        brand = ""
        while (not notEmpty):
            brand = input("\nEnter car brand to delete: ").strip()
            
            if (brand == ""):
                print("[_ERROR_]: Brand name cannot be empty. Please enter again.")
            else:
                notEmpty = True
        
        query = """
            DELETE FROM CAR WHERE brand = %s
            """
        
        sqlActions.modifyData(conn, cur, query, [brand])
        
    print("Delete car(s) successfully!") 


def command1(conn, cur):
    isValidInput = False
    while (not isValidInput):
        print("\nEnter your action: ")
        action = input("Insert(1) / remove(2): ").strip().lower()
        object = input("Car(1) / Model(2): ").strip().lower()

        if (action != "1" and action != "2" and action != "insert" and action != "remove"):
            print("[_ERROR_]: Invalid action. Please enter again.\n")
        elif (object != "1" and object != "2" and object != "car" and object != "model"):
            print("[_ERROR_]: Invalid action. Please enter again.\n")
        else:
            isValidInput = True
        
    if (object == "1" or object == "car"):
        if (action == "1" or action == "insert"):
            add_car(conn, cur)
        else:
            remove_car(conn, cur)
        


def tasks(conn, cur):
    userInput = ""
    while (userInput != "x"):
        taskOptions()
        userInput = input("Enter a task number or 'x' to exit: ")

        if (userInput == "1"):
            command1(conn, cur)


def main_manager(conn, cur):
    if (login_signup() == "signup"):
        signup(conn, cur)
    else:
        isSuccess = login(cur)

        if (not isSuccess):
            return
        else:
            tasks(conn, cur)
        
