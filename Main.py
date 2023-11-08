import mysql.connector as db
from art import *
import random
import os
from datetime import date
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import calendar


connection = db.connect(host="localhost", user="root", password="", database="PROJECT_w")
cursor = connection.cursor()

def Banner():

    print(text2art("Wealth Tracking APP"))


Banner()

def user_login():
    print(text2art("User Login"))
    global username_input
    username_input=input("Enter your Username:")
    password_input=input("Enter your Account Password:")

    cursor.execute("SELECT USERNAME,PASSWORD FROM USER;")
    userinfo = cursor.fetchall()

    for i in userinfo:
        if i[0] == username_input and i[1]==password_input:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("---Login Successfull---")
            user_dashboard()
            break
        else:
            print("User Not Found!")


def register_user():
    print(text2art("NEW USER ?"))
    Firstname = input("Enter your First Name:")
    Lastname = input("Enter your Last Name:")
    password_input=input("Please Select Password for your Account:")
    username = Firstname[0]+Lastname[-1]+str(random.randint(1000,3000))
    age = int(input("Enter your Age:"))

    print(f"Your Accout has Created SuccessFully ! Please remember this {username} It is your Username")

    user_info = cursor.execute(f"INSERT INTO USER (USERNAME, PASSWORD, FIRSTNAME, LASTNAME, AGE) VALUES ('{username}', '{password_input}', '{Firstname}', '{Lastname}', {age})")
    connection.commit()

    user_login()


def user_dashboard():
    
    cursor.execute(f"SELECT NETWORTH FROM USER WHERE USERNAME = '{username_input}';")
    Net_worth = cursor.fetchall()    
    print("Your Current Net Worth is: ", Net_worth[0][0])
    User_Menu()


def User_Menu():
    menu_options = {
    '1': Expense_Tracker,
    '2': Asset_Tracker,
    '3': Budget_Tracker,
    '4': exit
}
    continue_menu = True  

    while continue_menu:
        print("Menu:")
        print("1. Expense Tracker")
        print("2. Asset Tracker")
        print("3. Budget Tracker")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")

        if choice in menu_options:
            menu_options[choice]()
            break
        else:
            print("Invalid Choice")
    
def Expense_Tracker():

    print(text2art("Expense Tracker"))

    cursor.execute(f"SELECT SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' and EXPENSE_DATE = '{date.today()}';")

    exptoday = cursor.fetchall()
    print("Your Total Expense of Today is:",exptoday[0][0],"₹" )

    menu_options = {
    '1': Add_Expense,
    '2': Todays_Expenses,
    '3': Monthly_Expenses,
    '4': User_Menu,
    '5': exit
}
    continue_menu = True  

    while continue_menu:
        print("Menu:")
        print("1. Add_Expense")
        print("2. Today's Expense")
        print("3. Monthly Expenses")
        print("4. Back")
        print("5. Exit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice in menu_options:
            menu_options[choice]()
            break
        else:
            print("Invalid Choice")

        





def Asset_Tracker():
    print(text2art("Asset Tracker"))

def Budget_Tracker():
    print(text2art("Budget Tracker"))


def Add_Expense():

    while True:
        choice=input("Want to add Expense (Y/n)")
        if choice=='Y' or choice=='':
            expense_name=input("Enter the name of the expense: ")
            amount=float(input("Enter the cost of the expense: "))
            category = input("Enter Category of Your Expense (Travel,Food,Office):").upper()
            desc = input("Add Description of your Expense:")

            cursor.execute(f"INSERT INTO EXPENSE (USERNAME,EXPENSE_NAME,EXPENSE_AMOUNT,EXPENSE_DATE,EXPENSE_CATEGORY,DESCRIPTION) VALUES('{username_input}', '{expense_name}','{amount}','{date.today()}','{category}','{desc}')")

            connection.commit()

        elif choice=='n' or 'N':
            Expense_Tracker()
            break

        else:
            print("Invalid Choice")

def Todays_Expenses():

    print(text2art("Today's Expenses"))
    cursor.execute(f"SELECT SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' and EXPENSE_DATE = '{date.today()}';")
    total_expense_result = cursor.fetchall()
    total_expense = total_expense_result[0][0]

    cursor.execute(f"SELECT EXPENSE_CATEGORY, SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' and EXPENSE_DATE = '{date.today()}' GROUP BY EXPENSE_CATEGORY;")
    category_expenses = cursor.fetchall()

    percentage_spent = []
    for category, expense in category_expenses:
        category_percentage = (expense / total_expense) * 100
        percentage_spent.append((category, category_percentage))

    print(f"Total expenses for the day: {total_expense}")
    for category, percentage in percentage_spent:
        print(f"{category}: {percentage:.2f}%")
    print("<------------------------->")

        # Calculate the top expense categories for the day
    cursor.execute(f"SELECT EXPENSE_CATEGORY, SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' and EXPENSE_DATE = '{date.today()}' GROUP BY EXPENSE_CATEGORY ORDER BY SUM(EXPENSE_AMOUNT) DESC LIMIT 5;")
    top_categories = cursor.fetchall()


    # Display the top categories
    print("Top Expense Categories for the Day:")
    for category, total_amount in top_categories:
        print(f"{category}: ${total_amount:.2f}")
    print("<------------------------->")

    categories, amounts = zip(*top_categories)
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Top Expense Categories for the Day')
    plt.axis('equal')

    plt.show()


    cursor.execute(f"SELECT EXPENSE_NAME, EXPENSE_AMOUNT, EXPENSE_DATE, EXPENSE_CATEGORY FROM EXPENSE WHERE USERNAME = '{username_input}' and EXPENSE_DATE = '{date.today()}';")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses recorded for today.")
        return

    table = PrettyTable()
    table.field_names = ["Expense Name", "Amount", "Date", "Category"]

    for expense in expenses:
        table.add_row([expense[0], f"${expense[1]:.2f}", expense[2], expense[3]])

    print("Expense History for Today:")
    print(table)




    Expense_Tracker()



def Monthly_Expenses():
    print(text2art("Monthly Expenses"))
    today = date.today()
    current_month = today.month
    current_year = today.year

    first_day_of_month = date(current_year, current_month, 1)
    last_day_of_month = date(current_year, current_month, calendar.monthrange(current_year, current_month)[1])

    print(text2art("Monthly Expenses"))

    # Calculate total monthly expenses
    cursor.execute(f"SELECT SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' AND EXPENSE_DATE BETWEEN '{first_day_of_month}' AND '{last_day_of_month}';")
    total_monthly_expense_result = cursor.fetchall()
    total_monthly_expense = total_monthly_expense_result[0][0]

    # Calculate expenses by category
    cursor.execute(f"SELECT EXPENSE_CATEGORY, SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' AND EXPENSE_DATE BETWEEN '{first_day_of_month}' AND '{last_day_of_month}' GROUP BY EXPENSE_CATEGORY;")
    category_monthly_expenses = cursor.fetchall()

    # Calculate the percentage spent on each category
    percentage_spent = []
    for category, expense in category_monthly_expenses:
        category_percentage = (expense / total_monthly_expense) * 100
        percentage_spent.append((category, category_percentage))

    print(f"Total monthly expenses: {total_monthly_expense}")
    for category, percentage in percentage_spent:
        print(f"{category}: {percentage:.2f}%")
    print("<------------------------->")

    # Calculate the top expense categories for the month
    cursor.execute(f"SELECT EXPENSE_CATEGORY, SUM(EXPENSE_AMOUNT) FROM EXPENSE WHERE USERNAME = '{username_input}' AND EXPENSE_DATE BETWEEN '{first_day_of_month}' AND '{last_day_of_month}' GROUP BY EXPENSE_CATEGORY ORDER BY SUM(EXPENSE_AMOUNT) DESC LIMIT 5;")
    top_monthly_categories = cursor.fetchall()

    # Display the top categories
    print("Top Expense Categories for the Month:")
    for category, total_amount in top_monthly_categories:
        print(f"{category}: ${total_amount:.2f}")
    print("<------------------------->")

    categories, amounts = zip(*top_monthly_categories)
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title('Top Expense Categories for the Month')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    
    


menu_options = {
    '1': user_login,
    '2': register_user,
    '3': exit
}

continue_menu = True  

while continue_menu:
    print("Menu:")
    print("1. User Login")
    print("2. Register User")
    print("3. Exit")
    
    choice = input("Enter your choice (1/2/3): ")

    if choice in menu_options:
        menu_options[choice]()
        break
    else:
        print("Invalid Choice")

