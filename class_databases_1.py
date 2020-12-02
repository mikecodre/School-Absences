import os
import sqlite3
import smtplib
from email.message import EmailMessage
import shutil
from colorama import Fore

colors = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "RESET"]

print(f"{Fore.BLUE}School Script by Mixalis Tsaxakis")
print(f"School script by Python-Cod{Fore.RESET} ")

def replay():
    temp = input("Do you want to run again? (Y/N)")
    while temp.lower() != "y" and temp.lower() != "n":
        temp = input("Do you want to run again? (Y/N)")
    if temp.lower() == "y":
        menu()
    else:
        pass

class Data:
    def __init__(self):
        if self.first_time() == "y":
            print("exists")
        elif self.first_time() == "n":
            print("doesn't exist")
        x = 0
        class_dict = {1: "Α1",
                      2: "Α2",
                      3: "Α3",
                      4: "Α4",
                      5: "Α5",
                      6: "Α6",
                      7: "Β1",
                      8: "Β2",
                      9: "Β3",
                      10: "Β4",
                      11: "Γ1",
                      12: "Γ2",
                      14: "Γ3"}

        class_list = ["A1", "A2", "A3", "A4", "Α5", "Α6", "Β1", "Β2", "Β3", "Β4", "Γ1", "Γ2", "Γ3"]
        dir_check = os.path.isdir("class_databases_1")
        if not dir_check:
            os.mkdir("class_databases_1")
        elif dir_check:
            pass
        os.chdir("{}/class_databases_1".format(os.getcwd()))

        for i in class_list:
            x += 1
            print("{}.".format(x), i)
            if not os.path.isfile("{}.db".format(i)):
                connection = sqlite3.connect("{}.db".format(i))
                connection.close()
        for i in class_list:
            self.connection = sqlite3.connect("{}.db".format(i))
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS basic (id INTEGER PRIMARY KEY, name TEXT, last_name TEXT, absences 
                INTEGER DEFAULT 0)""")
            self.connection.commit()
        print(f"{Fore.YELLOW}TABLES created or verified Successfully!{Fore.RESET}")
        # print(Fore.RESET)
        class_selection = int(input("Give class number: "))
        for i in class_dict:
            while class_selection not in class_dict:
                class_selection = int(input("Give class number: "))
            self.class_name = class_dict[class_selection]
        class_selection = self.class_name
        print("Class selection = ", self.class_name)

        self.connection = sqlite3.connect(f"{class_selection}.db")
        self.cursor = self.connection.cursor()

    def first_time(self):
        if os.path.isfile("first.txt"):
            print(os.path)
            return "y"
        else:
            with open("first.txt", "w") as file:
                file.write("hi")
            return "n"
    def credentials(self):
        current = os.getcwd()
        split = current.split("/")
        path = ""
        for i in split[:-1]:
            path = path + f"{i}/"
        os.chdir(path)
        self.user_mail = input("Give your mail: ")
        self.user_password = input("Give your password: ")
        self.end_user_mail = input("Give end user mail: ")
        new_line = "\n"
        all = f"{self.user_mail}" + new_line + f"{self.user_password}" + new_line + f"{self.end_user_mail}"
        with open("credents.txt", "w") as file:
            file.write(all)
        os.chdir(path)

    def send_mail(self, report):
        with open("credents.txt", "r") as file:
            lines = file.readlines()
            length = 0
            for i in lines:
                if length == 0:
                    fmail = i.strip()
                elif length == 1:
                    password = i.strip()
                elif length == 2:
                    endmail = i.strip()
                length += 1
        msg = EmailMessage()
        msg["Subject"] = f'{self.class_name}'
        msg["From"] = fmail
        msg["To"] = endmail
        msg.set_content(f"{self.report}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(fmail, password)
            smtp.send_message(msg)

    def option_1(self):
        self.cursor.execute("Select * from basic")
        data = self.cursor.fetchall()
        for id, name, last, absence in data:
            print("Name =", name, last, " absences = ", absence)
        replay()

    def option_2(self):
        nam = input("Give name: ")
        last_nam = input("Give last name: ")
        self.cursor.execute("INSERT OR IGNORE INTO basic (name, last_name)VALUES('{}','{}')".format(nam, last_nam))
        self.connection.commit()
        print("Commited Successfully!")
        choice = input("Do you want to add another student? (Y/N) ")
        if choice.lower() == "y":
            self.option_2()
        else:
            pass
        replay()

    def option_3(self):
        print()
        print("Options: ")
        print("1. See Absences")
        print("2. Add Absences")
        print("3. Delete Absences")
        choice = int(input("Select an option: "))
        print()
        while choice > 3 or choice < 1:
            choice = int(input("Select an option: "))
        if choice == 1:
            self.cursor.execute("Select * from basic")
            data = self.cursor.fetchall()
            for id, name, last, absence in data:
                print("Name =", name, last, " absences = ", absence)
        elif choice == 2:
            self.cursor.execute("Select * from basic")
            data = self.cursor.fetchall()
            for id, name, last, absence in data:
                print("{}.{} {} | Absences = {}".format(id, name, last, absence))
            id = int(input("Select an id to add absence: "))
            self.cursor.execute("UPDATE basic set absences = absences + 1 WHERE id = ?", ('{}'.format(id),))
            self.connection.commit()
            self.cursor.execute("Select * from basic")
            data = self.cursor.fetchall()
            print("Record Updated successfully!")
            print("Updated Values: ")
            for id, name, last, absence in data:
                print("Name =", name, last, " absences = ", absence)
        elif choice == 3:
            self.cursor.execute("Select * from basic")
            data = self.cursor.fetchall()
            for id, name, last, absence in data:
                print("{}.{} {} | Absences = {}".format(id, name, last, absence))
            id = int(input("Select an id to remove absence: "))
            self.cursor.execute("UPDATE basic set absences = absences - 1 WHERE id = ?", ('{}'.format(id),))
            self.connection.commit()
            self.cursor.execute("Select * from basic")
            data = self.cursor.fetchall()
            print("Record Updated successfully!")
            print("Updated Values: ")
            for id, name, last, absence in data:
                print("Name =", name, last, " absences = ", absence)
        replay()

    def option_4(self):
        print("Report Option")
        self.cursor.execute("Select * from basic")
        data = self.cursor.fetchall()
        self.report = ""
        for id, name, last, absence in data:
            self.report += "\n-The student {} {} has {} absences".format(name, last, absence)
        print("Report:", self.report)
        print()
        choice = input("Do you want to send the report?(Y/N) ")
        while choice.lower() != "y" and choice.lower() != "n":
            choice = input("Do you want to send the report?(Y/N) ")
        if choice.lower() == "y":
            print("Sending report...")
            self.send_mail(self.report)
            print("Report sent successfully!")
        replay()

    def option_5(self):
        print("Settings Option")
        print("1. Change the receiver and the sender mail")
        print("2. Reset All")
        choice = int(input("Select an option: "))
        if choice == 1:
            print("MAKE SURE THE EMAIL IS CORRECT!")
            with open("credents.txt", "w") as file:
                fmail = input("Give your mail: ")
                password = input("Give your password: ")
                endmail = input("Give the sender mail: ")
                file.write(f"{fmail}\n{password}\n{endmail}")
        elif choice == 2:
            print("Reset option Enabled")
            print("Resetting")
            shutil.rmtree(f"{os.getcwd()}")
            print("Reset Done!")
        replay()


object = Data()

creds_check = os.path.isfile("credents.txt")
if not creds_check:
    object.credentials()
else:
    pass



def menu():
    print("Options:")
    print("1. See data")
    print("2. Add student")
    print("3. Absences")
    print("4. Report")
    print("5. General Settings")
    option = int(input("Select an option: "))
    while option < 1 or option > 5:
        option = int(input("Select an option: "))
    if option == 1:
        object.option_1()
    elif option == 2:
        object.option_2()
    elif option == 3:
        object.option_3()
    elif option == 4:
        object.option_4()
    elif option == 5:
        object.option_5()

menu()
