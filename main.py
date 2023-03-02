import datetime
import sqlite3
from datetime import date


class Member:
    def __init__(self, name, age, phone):
        self.name = name
        self.age = age
        self.phone = phone

    def create_membership(self):
        self.name = input("Enter Name: ")
        try:
            self.age = int(input("Enter Age: "))
            if self.age <= 0:
                print("Invalid input. Enter a positive integer.")
                self.age = int(input("Enter Age: "))
        except ValueError:
            print("Invalid input. Enter a positive integer.")
            self.age = int(input("Enter Age: "))
        self.phone = input("Enter Cell no.: ")
        if len(self.phone) != 10:
            print("Invalid number. Enter again.")
        conn = sqlite3.connect('lib_db.db')
        insert_data = """INSERT INTO MemberRecord
                        (Name, Age, Phone)
                        VALUES ('{}', '{}', '{}');""".format(
            self.name, self.age, self.phone)
        cursor = conn.cursor()
        cursor.execute(insert_data)
        conn.commit()
        cursor.close()
        print("Membership Created.")


class Library(Member):
    def __init__(self, name, age, phone, list_of_books):
        super().__init__(name, age, phone)
        self.list_of_books = list_of_books

    def display_books(self):
        c = 1
        self.list_of_books = []
        print("Following books are available at the moment:")
        conn = sqlite3.connect('lib_db.db')
        cursor = conn.cursor()
        book_query = "SELECT * FROM BookInfo"
        cursor.execute(book_query)
        rows_1 = cursor.fetchall()
        for j in rows_1:
            self.list_of_books.append(j[1])
        for book in self.list_of_books:
            print(f"{c}. {book}")
            c += 1

    def issue_book(self):
        name_list = []
        issued_book_info = {}
        check = input("Enter User's full name: ")
        conn = sqlite3.connect('lib_db.db')
        cursor = conn.cursor()
        sql_command = """SELECT * FROM MemberRecord"""
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        for i in rows:
            name_list.append(i[0])
        cursor.close()
        if check in name_list:
            cursor = conn.cursor()
            book_query = "SELECT * FROM BookInfo"
            cursor.execute(book_query)
            rows_1 = cursor.fetchall()
            for j in rows_1:
                book_list.append(j[1])
                issued_book_info[j[1]] = [j[0], j[2]]
            book_name = input("Enter the name of the book to be issued: ")
            if book_name in self.list_of_books:
                doi = date.today()
                t = datetime.timedelta(days=14)
                rd = doi + t
                print(f"{book_name} has been issued to {check}.")
                borrow_info = """INSERT INTO BorrowerRec
                        (BorrowerName, BookID, BookName, Author, DateOfIssue, ReturnDate)
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""".format(
                    check, issued_book_info[book_name][0], book_name,
                    issued_book_info[book_name][1], doi, rd
                )
                cursor = conn.cursor()
                cursor.execute(borrow_info)
                cursor.execute("""
                DELETE FROM BookInfo
                WHERE Book = ?
                """, (book_name,))
                conn.commit()
                conn.close()
            else:
                print("The requested book is not available.")
        else:
            print("User does not exist.")

    @staticmethod
    def return_book():
        name_list = []
        borrower_list = []
        borrowed_book_info = {}
        check = input("Enter User's full name: ")
        conn = sqlite3.connect('lib_db.db')
        cursor = conn.cursor()
        borrow_query = """SELECT * FROM BorrowerRec"""
        user_query = """SELECT * FROM MemberRecord"""
        cursor.execute(user_query)
        rows_1 = cursor.fetchall()
        for i in rows_1:
            name_list.append(i[0])
        cursor.execute(borrow_query)
        rows_2 = cursor.fetchall()
        for b in rows_2:
            borrower_list.append(b[0])
            borrowed_book_info[b[0]] = [b[1], b[2], b[3]]
        if check in name_list and check in borrower_list:
            print(f"{check} wants to return {borrowed_book_info[check][1]}")
            press = input("Press 'y' to return.")
            if press == 'y':
                cursor = conn.cursor()
                book_return = """INSERT INTO BookInfo
                                        (BookID, Book, Author)
                                        VALUES ('{}', '{}', '{}');""".format(
                    borrowed_book_info[check][0], borrowed_book_info[check][1],
                    borrowed_book_info[check][2]
                )
                cursor.execute(book_return)
                conn.commit()
                cursor.execute("""
                                DELETE FROM BorrowerRec
                                WHERE BorrowerName = ?
                                """, (check,))
                conn.commit()
                conn.close()
                print("Book returned successfully.")
        elif check in name_list and check is not borrower_list:
            print(f"{check} has not borrowed any book as of now.")
        else:
            print("User does not exist.")

    @staticmethod
    def add_book():
        new_book = input("Enter the name of book to be added: ")
        try:
            book_id = int(input("Enter BookID: "))
            if len(str(book_id)) != 4:
                print("Please enter a 4-digit number.")
            author = input("Name of Author: ").title()
            conn = sqlite3.connect('lib_db.db')
            cursor = conn.cursor()
            add_book = """INSERT INTO BookInfo
                                (BookID, Book, Author)
                                VALUES ('{}', '{}', '{}');""".format(
                book_id, new_book, author
            )
            cursor.execute(add_book)
            conn.commit()
            print(f"{new_book} has been added to the library.")
        except ValueError:
            print("Please enter a 4-digit number.")


member = Member(" ", 0, 0)
book_list = []
lms = Library(" ", 0, 0, book_list)
while True:
    print("***** LIBRARY MENU *****\n\t"
          "\n\t"
          "1. Create Membership.\n\t"
          "2. Display available books.\n\t"
          "3. Lend book.\n\t"
          "4. Return book.\n\t"
          "5. Add a new book.\n\t"
          "6. Exit.")
    print("")
    try:
        choice = int(input("Enter choice(1/2/3/4/5/6):"))
        print()
        if choice == 1:
            lms.create_membership()
            print()
            ask = ''
            while ask != 'm':
                print()
                ask = input("Press 'n' to register next member\n"
                            "and press 'm' to return to main-menu. ").lower()
                if ask == 'n':
                    lms.create_membership()
                elif ask == 'm':
                    continue
                else:
                    print("Invalid keypress. Try again")
                    ask = input("Press 'n' to register next member\n"
                                "and press 'm' to return to main-menu.").lower()

        elif choice == 2:
            lms.display_books()
            print()
            continue
        elif choice == 3:
            lms.issue_book()
            print()
            ask = ''
            while ask != 'm':
                print()
                ask = input("Press 'n' to issue another book\n"
                            "and press 'm' to return to main-menu.").lower()
                if ask == 'n':
                    lms.issue_book()
                elif ask == 'm':
                    continue
                else:
                    print("Invalid keypress. Try again")
                    ask = input("Press 'n' to issue another book\n"
                                "and press 'm' to return to main-menu.").lower()

        elif choice == 4:
            lms.return_book()
            print()
            ask = ''
            while ask != 'm':
                print()
                ask = input("Press 'n' to return another book\n"
                            "and press 'm' to return to main-menu.").lower()
                if ask == 'n':
                    lms.return_book()
                elif ask == 'm':
                    continue
                else:
                    print("Invalid keypress. Try again")
                    ask = input("Press 'n' to return another book\n"
                                "and press 'm' to return to main-menu.").lower()

        elif choice == 5:
            lms.add_book()
            print()
            ask = ''
            while ask != 'm':
                print()
                ask = input("Press 'n' to add another book\n"
                            "and press 'm' to return to main-menu.").lower()
                if ask == 'n':
                    lms.add_book()
                elif ask == 'm':
                    continue
                else:
                    print("Invalid keypress. Try again")
                    ask = input("Press 'n' to add another book\n"
                                "and press 'm' to return to main-menu.").lower()

        elif choice == 6:
            break
        else:
            print("Invalid Choice. Enter again.")
            continue
    except ValueError:
        print("Please enter a number between 1 and 6.")
        continue
