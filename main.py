import psycopg2
import re
import manager
import driver
import client


def userMenu():
    print("\n=========================================================")
    print("Select 1 of the options below to log-in/sign-up:")
    print("1 - Manager")
    print("2 - Client")
    print("3 - Driver")
    print("0 - Exit")
    

def connectDatabase():
    conn = psycopg2.connect(
        dbname="CS480_PROJECT",
        user="postgres",
        password="Jim010422Nguyen",
        host="localhost",      # or an IP/domain name
        port="5432"            # default PostgreSQL port
    )

    cur = conn.cursor()
    return conn, cur


def main(conn, cur):
    print("TAXI RENTAL MANAGEMENT APPLICATION")

    userChoice = ""
    while userChoice != "0":
        userMenu()
        userChoice = input("Your choice: ")

        userChoice = userChoice.strip()
        if (userChoice == "1"):
            manager.main_manager(conn, cur)
        elif (userChoice == "2"):
            client.main_client(conn, cur)
        elif (userChoice == '3'):
            driver.main_driver(conn, cur)

    cur.close()
    conn.close()


if __name__ == "__main__":
    conn, cur = connectDatabase()
    main(conn, cur)

