import re
import sqlActions

def signup(conn, cur):
    name  = input("Name: ").strip()
    email = input("Email: ").strip()
    sqlActions.modifyData(conn, cur, "INSERT INTO CLIENT (client_name, client_email) VALUES (%s, %s)", [name,email])


    # home address for new client
    n_addr = int(input("How many home addresses do you wish to add? ").strip())
    for _ in range(n_addr):
        road = input("Address Road Name: ").strip()
        num  = int(input("Address Number: ").strip())
        city = input("City: ").strip()

        sqlActions.modifyData(conn, cur, ("INSERT INTO ADDRESS (road_name, address_number, city) VALUES (%s,%s,%s) ON CONFLICT (road_name, address_number, city) DO NOTHING"), [road,num,city])
        sqlActions.modifyData(conn, cur, ("INSERT INTO NM_CLIENT_ADDRESS (client_email, road_name, address_number, city) VALUES (%s,%s,%s,%s)"), [email,road,num,city])


    # credit card + billing address
    n_cc = int(input("How many credit cards do you wish to add? ").strip())
    for _ in range(n_cc):
        ccnum = input(" Credit Card Number: ").strip()
        print(" Billing Address:")
        proad = input("  Billing Address Road Name: ").strip()
        pnum  = int(input("  Billing Address Number: ").strip())
        pcity = input("  Billing Address City: ").strip()

        sqlActions.modifyData(conn, cur, ("INSERT INTO ADDRESS (road_name, address_number, city) VALUES (%s,%s,%s) ON CONFLICT (road_name, address_number, city) DO NOTHING"), [proad,pnum,pcity])
        sqlActions.modifyData(conn, cur, ("INSERT INTO CREDIT_CARD (credit_card_number, client_email, road_name, address_number, city) VALUES (%s,%s,%s,%s,%s)"), [ccnum,email,proad,pnum,pcity])

    print("Sign-up complete!\n")



def login(cur):
    email = input("Email: ").strip()
    row = sqlActions.fetchOneData(cur, "SELECT client_email FROM CLIENT WHERE client_email = %s", [email])

    if row:
        print("Logged in!\n")
        return email
    else:
        print("Client wasn't found. Please make sure you've signed up first.")
        return None



def show_models(cur):
    date = input("Enter desired rent date (YYYY-MM-DD): ").strip()
    query = """
    SELECT m.model_id, m.car_id, m.color, m.transmission_type, m.construction_year FROM MODEL m
    WHERE NOT EXISTS (SELECT 1 FROM RENT r WHERE r.model_id = m.model_id 
                       AND r.car_id = m.car_id 
                       AND r.rent_date = %s
    )
    AND EXISTS (SELECT 1 FROM DRIVE d WHERE d.model_id = m.model_id
                       AND d.car_id = m.car_id
                       AND NOT EXISTS (SELECT 1 FROM RENT r2 WHERE r2.driver_name = d.driver_name
                                       AND r2.rent_date   = %s)
    )
    ORDER BY m.car_id, m.model_id;
    """
    rows = sqlActions.fetchAllData(cur, query, [date, date])

    if not rows:
        print(f"\nNo models available on {date}.\n")
        return []

    print(f"\nAvailable models on {date}:")
    for mid, cid, color, trans, year in rows:
        print(f"  Model {mid} (Car {cid}): {color}, {trans}, {year}")
    print()
    return rows



def book_rent(conn, cur, email):
    # gets the next rent id
    mx = sqlActions.fetchOneData(cur, "SELECT COALESCE(MAX(rent_id),0) FROM RENT", [])
    new_id = mx[0] + 1

    date = input("Date (YYYY-MM-DD): ").strip()
    mid  = int(input("Model ID: ").strip())
    cid  = int(input("Car ID: ").strip())
    drv  = input("Driver Name: ").strip()

    sqlActions.modifyData(conn, cur, ("INSERT INTO RENT (rent_id, rent_date, client_email, model_id, car_id, driver_name) VALUES (%s,%s,%s,%s,%s,%s)"), [new_id, date, email, mid, cid, drv])
    print(f"Booked rent {new_id} on {date}.\n")



def list_rents(cur, email):
    rows = sqlActions.fetchAllData(cur, ("SELECT rent_id, rent_date, model_id, car_id, driver_name FROM RENT WHERE client_email=%s ORDER BY rent_date"), [email])

    if not rows:
        print("No bookings found.\n")
        return
    
    print("\nYour rents:")
    for rid, d, mid, cid, drv in rows:
        print(f" Rent {rid} on {d}: model {mid}, car {cid}, driver {drv}")
    print()



def review_driver(conn, cur, email):
    drv = input("Driver Name to Review: ").strip()
    ok = sqlActions.fetchOneData(cur, ("SELECT 1 FROM RENT WHERE client_email=%s AND driver_name=%s"), [email, drv])
    if not ok:
        print("You can only review drivers you've booked a rent with.\n")
        return
    
    rid    = int(input("Review ID: ").strip())
    rating = int(input("Rating (1–5): ").strip())
    msg    = input("Message: ").strip()

    sqlActions.modifyData(conn, cur, ("INSERT INTO REVIEW (review_id, driver_name, client_email, rating, review_message) VALUES (%s,%s,%s,%s,%s)"), [rid, drv, email, rating, msg])
    print("Review submitted!\n")



def list_reviews(cur, email):
    rows = sqlActions.fetchAllData( cur, ("SELECT review_id, driver_name, rating, review_message FROM REVIEW WHERE client_email=%s ORDER BY review_id"), [email])
    if not rows:
        print("You haven’t written any reviews yet.\n")
        return

    print("\nYour reviews:")
    for rid, drv, rating, msg in rows:
        print(f" Review {rid} for {drv}: {rating}/5 — {msg}")
    print()



def client_menu():
    print("Client Tasks:")
    print(" 1. Show available models")
    print(" 2. Book a rent with a driver")
    print(" 3. List my rents")
    print(" 4. Review a driver")
    print(" 5. List my reviews")
    print(" x. Logout")



def main_client(conn, cur):
    user = None
    while True:
        if not user:
            print("\nClient")
            print("1. Sign up")
            print("2. Log in")
            print("x. Exit")
            choice = input("Choose an option: ").strip().lower()
            if choice == '1':
                signup(conn, cur)
            elif choice == '2':
                user = login(cur)
            elif choice == 'x':
                break
            else:
                print("Invalid choice.\n")
        else:
            client_menu()
            choice = input("Choose an action: ").strip().lower()
            if choice == '1':
                show_models(cur)
            elif choice == '2':
                book_rent(conn, cur, user)
            elif choice == '3':
                list_rents(cur, user)
            elif choice == '4':
                review_driver(conn, cur, user)
            elif choice == '5':
                list_reviews(cur, user)
            elif choice == 'x':
                user = None
                print("Logged out.\n")
            else:
                print("Invalid choice.\n")
