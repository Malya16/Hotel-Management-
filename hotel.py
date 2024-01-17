import mysql.connector

myConnection = mysql.connector.connect(host="localhost", user="root", passwd="sql")
cur = myConnection.cursor()

# TO CREATE TABLES IN THE DATABASE
def DatabaseCreation():
    try:
        my_query = "CREATE TABLE IF NOT EXISTS cust_details (CID INT PRIMARY KEY NOT NULL AUTO_INCREMENT, C_NAME VARCHAR(30) NOT NULL, C_ADDRESS VARCHAR(30), C_COUNTRY VARCHAR(30), C_CONTACT CHAR(10))"
        cur.execute(my_query)

        my_query = "CREATE TABLE IF NOT EXISTS Booking_Rec (CID INT PRIMARY KEY, CHECK_IN_DATE DATE, CHECK_OUT_DATE DATE)"
        cur.execute(my_query)

        my_query = "CREATE TABLE IF NOT EXISTS Room_Rent (CID INT PRIMARY KEY, RoomChoice INT, NoOfRooms INT, Days INT, RoomNo TEXT, RoomRent INT)"
        cur.execute(my_query)

        my_query = "CREATE TABLE IF NOT EXISTS Restaurant (CID INT PRIMARY KEY NOT NULL, Cuisine INT(1), Quantity INT, Bill INT)"
        cur.execute(my_query)

        my_query = "CREATE TABLE IF NOT EXISTS Gaming (CID INT PRIMARY KEY NOT NULL, Games VARCHAR(30), Hours VARCHAR(30), Gaming_Bill INT)"
        cur.execute(my_query)

        my_query = "CREATE TABLE IF NOT EXISTS Total_Bill (CID INT PRIMARY KEY, C_NAME VARCHAR(30), GrandTotal INT, RoomRent INT, Restaurant_Bill INT, GamingBill INT)"
        cur.execute(my_query)

    except Exception as e:
        print(e)

def display(record):
    print("Customer ID:", record[0])
    print("Customer Name:", record[1])
    print("Customer Address:", record[2])
    print("Customer Country:", record[3])
    print("Customer Contact:", record[4])

def search_cust(display_result=False):
    phone = int(input("Enter Customer's Phone No.: "))
    cur.execute("SELECT * FROM cust_details WHERE C_CONTACT=%s", (phone,))
    record = cur.fetchone()

    if record:
        if display_result:
            display(record)
        return True, record
    else:
        if display_result:
            print("Record not found, Try Again!")
        return False, record

def UserEntry():
    C_NAME = input("Enter Customer Name: ").upper()
    C_ADDRESS = input("Enter Customer Address: ").upper()
    C_COUNTRY = input("Enter Customer Country: ").upper()
    C_CONTACT = int(input("Enter Customer Contact Number: "))

    cur.execute("INSERT INTO cust_details (C_NAME, C_ADDRESS, C_COUNTRY, C_CONTACT) VALUES (%s, %s, %s, %s)",
                (C_NAME, C_ADDRESS, C_COUNTRY, C_CONTACT))
    myConnection.commit()
    CID = cur.lastrowid
    BookingRec(CID)
    RoomRent(CID)
    cur.execute("INSERT INTO Restaurant VALUES (%s, %s, %s, %s)", (CID, 0, 0, 0))
    cur.execute("INSERT INTO Gaming VALUES (%s, %s, %s, %s)", (CID, 0, 0, 0))
    myConnection.commit()

def BookingRec(CID):
    checkin = input("\nEnter Customer Check-IN date [YYYY-MM-DD]: ")
    checkout = input("Enter Customer Check-OUT date [YYYY-MM-DD]: ")
    cur.execute("INSERT INTO Booking_Rec VALUES (%s, %s, %s)", (CID, checkin, checkout))
    myConnection.commit()
    print("CHECK-IN and CHECK-OUT entry added successfully")

def RoomRent(CID):
    print("\n ##### We have The Following Rooms For You #####")
    print("1.UltraRoyal------>10000s.")
    print("2.Royal ‒‒‒‒‒‒‒>5000Rs.")
    print("3.Elite --------->3500Rs.")
    print("4.Budget -------->2500Rs.")

    RoomChoice = int(input("Enter the type of room you want: "))
    Noofrooms = int(input("Enter the number of rooms you want: "))
    RoomNo = input("Enter Customer's Room no: ")

    cur.execute('SELECT DATEDIFF (CHECK_OUT_DATE, CHECK_IN_DATE) FROM Booking_Rec WHERE CID=%s', (CID,))
    Days = cur.fetchall()[0][0]

    if RoomChoice == 1:
        Roomrent = Days * 10000 * Noofrooms
        print("Ultra Royal RoomRent:", Roomrent)
    elif RoomChoice == 2:
        Roomrent = Days * 5000 * Noofrooms
        print("Royal Room Rent:", Roomrent)
    elif RoomChoice == 3:
        Roomrent = Days * 3500 * Noofrooms
        print("Elite Room Rent:", Roomrent)
    elif RoomChoice == 4:
        Roomrent = Days * 2500 * Noofrooms
        print("Budget Room Rent: ", Roomrent)
    else:
        print("Sorry, You are giving wrong inputs, Try Again!!")
        return

    cur.execute("INSERT INTO Room_Rent VALUES (%s, %s, %s, %s, %s, %s)",
                (CID, RoomChoice, Noofrooms, Days, RoomNo, int(Roomrent)))
    myConnection.commit()
    print("Thank You, Your", Noofrooms, "Room(s) Has Been Booked For:", Days, "Days")
    print("Your Total Room Rent is: Rs.", Roomrent)

def Restaurant():
    customer = search_cust()
    if customer[0]:
        print("1.Vegetarian Combo --->300Rs.")
        print("2.Non-Vegetarian Combo --------->500Rs.")
        print("3.Vegetarian and Non-Vegetarian Combo >750Rs.")
        print("4.Exit")
        ch_dish = int(input("Enter Your Choice Of Cusine:"))
        q = int(input("Enter Quantity:"))

        if ch_dish == 1:
            print("YOU HAVE ORDERED VEGETARIAN COMBO")
            RestaurantBill = q * 300
        elif ch_dish == 2:
            print("YOU HAVE ORDERED NON VEGETARIAN COMBO")
            RestaurantBill = q * 500
        elif ch_dish == 3:
            print("YOU HAVE ORDERED VEGETARIAN AND NON VEGETARIAN BOTH")
            RestaurantBill = q * 800
        elif ch_dish == 4:
            return
        else:
            print("Sorry, You are giving wrong inputs, try again!!")
            return

        cur.execute("UPDATE Restaurant SET Cuisine=%s, Quantity=%s, Bill=%s WHERE CID=%s",
                    (ch_dish, q, int(RestaurantBill), customer[1][0]))
        myConnection.commit()
        print("Your total Bill Amount is: Rs.", RestaurantBill)
        print("\n****WE HOPE YOU WILL ENJOY YOUR MEAL*****")
    else:
        print("\nSorry, No Such Customer Found")

def Gaming():
    customer = search_cust()
    if customer[0]:
        print("1.Table Tennis -->150Rs./HR")
        print("2.Bowling ->100Rs./HR")
        print("3.Snooker ->250Rs./HR")
        print("4.VR World Gaming -->400Rs./HR")
        print("5.Video Games ---->300Rs./HR")
        print("6.Swimming Pool Games ------>350Rs./HR")
        print("7.Exit")
        Games = int(input("Enter what game you want to play: "))
        Hours = float(input("Enter No. of Hours you want to play: "))

        if Games == 1:
            print("YOU HAVE SELECTED TABLE TENNIS")
            GamingBill = Hours * 150
        elif Games == 2:
            print("YOU HAVE SELECTED BOWLING")
            GamingBill = Hours * 100
        elif Games == 3:
            print("YOU HAVE SELECTED SNOOKER")
            GamingBill = Hours * 250
        elif Games == 4:
            print("YOU HAVE SELECTED VR WORLD GAMING")
            GamingBill = Hours * 400
        elif Games == 5:
            print("YOU HAVE SELECTED VIDEO GAMES")
            GamingBill = Hours * 300
        elif Games == 6:
            print("YOU HAVE SELECTED SWIMMING POOL GAMES")
            GamingBill = Hours * 350
        elif Games == 7:
            return
        else:
            print("Sorry wrong Input")
            return

        cur.execute("UPDATE Gaming SET Games=%s, Hours=%s, Gaming_Bill=%s WHERE CID=%s",
                    (Games, Hours, int(GamingBill), customer[1][0]))
        myConnection.commit()
        print("YOUR TOTAL GAMING BILL IS: Rs.", int(GamingBill) + 1, "For:", Hours, "Hours")
        print("\n ***** WE HOPE YOU ENJOY YOUR GAME *****")
    else:
        print("\nSorry, No Such Customer Found")

def Amount():
    customer = search_cust()
    if customer[0]:
        C_NAME = customer[1][1]
        cur.execute('SELECT RoomRent FROM Room_Rent WHERE CID=%s', (customer[1][0],))
        RoomRent = cur.fetchone()[0]
        cur.execute('SELECT Bill FROM Restaurant WHERE CID=%s', (customer[1][0],))
        RestaurantBill = cur.fetchone()[0]
        cur.execute('SELECT Gaming_Bill FROM Gaming WHERE CID=%s', (customer[1][0],))
        GamingBill = cur.fetchone()[0]

        grandTotal = RoomRent + RestaurantBill + GamingBill

        cur.execute("INSERT INTO Total_Bill VALUES (%s, %s, %s, %s, %s, %s)",
                    (customer[1][0], C_NAME, grandTotal, RoomRent, RestaurantBill, GamingBill))
        myConnection.commit()

        print("\n***** VENETIAN HOTEL ***** CUSTOMER BILLING********")
        print("CUSTOMER NAME:", C_NAME)
        print("ROOMRENT: Rs.", RoomRent)
        print("RESTAURANT BILL: Rs.", RestaurantBill)
        print("GAMING BILL: Rs.", GamingBill)
        print("TOTAL AMOUNT: Rs.", grandTotal)
    else:
        print("Sorry, No Such Customer Found")

def main():
    cur.execute("CREATE DATABASE IF NOT EXISTS HOTEL")
    cur.execute("USE HOTEL")
    DatabaseCreation()

    while True:
        print("\n\nWELCOME TO VENETIAN HOTEL MANAGEMENT ATITHI DEVO BHAVA")
        print("1---->NEW CUSTOMER")
        print("2->RESTAURANT BILL")
        print("3->GAMING BILL")
        print("4---->DISPLAY CUSTOMER DETAILS")
        print("5->GENERATE TOTAL BILL")
        print("6-->EXIT")
        ch = input("Enter your choice: ")

        if ch == '1':
            UserEntry()
        elif ch == '2':
            Restaurant()
        elif ch == '3':
            Gaming()
        elif ch == '4':
            search_cust(True)
        elif ch == '5':
            Amount()
        elif ch == '6':
            break
        else:
            print("SORRY WRONG INPUT, PLEASE TRY AGAIN")

if __name__ == "__main__":
    main()
