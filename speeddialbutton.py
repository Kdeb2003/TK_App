import datetime

import mysql.connector
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.snackbar import Snackbar

Window.size = (320, 580)

class DynamicButtonsApp(MDApp):

    database = mysql.connector.Connect(host="localhost", user="root", password="Kushal@2003",
                                        database="jahir",)
    #database = mysql.connector.connect(user="sql12643515",host="sql12.freesqldatabase.com",password="gSpCSP2vBZ",database="sql12643515")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    cursor = database.cursor()

    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("eventmanagershowstudentsapply.kv"))
        sm.add_widget(Builder.load_file("listofstudentsappliedtodance.kv"))
        sm.add_widget(Builder.load_file("student_details_dance.kv"))
        return sm

    def show_applied_dance_list(self):
        sm.current = "applied dance list"
        dance = "Dance"
        self.cursor.execute("select stu_name,event_name,performance_category from applied_event_list where performance_category ='Dance'")
        row = self.cursor.fetchall()
        dance_list = self.root.get_screen('applied dance list').ids.dance_list
        dance_list.clear_widgets()
        for i in row:
            item = ThreeLineListItem(text = i[0], secondary_text = str(i[1]),tertiary_text = str(i[2]))
            item.bind(on_release= self.dance_student_details)
            dance_list.add_widget(item)


    def dance_student_details(self,item):
        self.cursor.execute("select * from applied_event_list where performance_category ='Dance'")
        row = self.cursor.fetchone()
        sm.current = "student details dance"
        student_details_screen = sm.get_screen("student details dance")
        if student_details_screen:
            student_details_screen.ids.stuname.text=str(row[0])
            student_details_screen.ids.reg_no.text=str(row[1])
            student_details_screen.ids.eventname.text=str(row[2])
            student_details_screen.ids.perfcat.text = str(row[3])
            student_details_screen.ids.dateofapplying.text = str(row[4])

    def show_snackbar(self, text):
        Snackbar(text=text).open()

    def shortlist(self):
        det = sm.get_screen('student details dance')
        stu_name = det.ids.stuname.text
        reg_no = det.ids.reg_no.text
        eventname = det.ids.eventname.text
        perfcat = det.ids.perfcat.text
        today = datetime.date.today()
        a = "shortlisted"

        # Check if the student is already rejected
        existing_query = f"SELECT * FROM status_of_applied_students WHERE reg_no = '{reg_no}'"
        self.cursor.execute(existing_query)
        existing_record = self.cursor.fetchone()

        if existing_record:
            # Student is already rejected, so update the 'shortlisted_ornot' column
            try:
                self.cursor.execute(
                    "UPDATE status_of_applied_students set date_of_response = %s, status = %s where reg_no = %s",
                    (today, a, reg_no)
                )
                self.database.commit()
                self.show_snackbar("Student status updated successfully.")
            except Exception as e:
                self.database.rollback()  # Rollback the transaction if an error occurs
                self.show_snackbar("Error: " + str(e))
        else:
            # Student is not rejected, so insert a new record
            try:
                self.cursor.execute(
                    "INSERT INTO status_of_applied_students VALUES (%s,%s,%s,%s,%s,%s) ",
                    ( stu_name, reg_no, eventname, perfcat, today, a)
                )
                self.database.commit()
                self.show_snackbar("Student shortlisted successfully.")
            except Exception as e:
                self.database.rollback()  # Rollback the transaction if an error occurs
                self.show_snackbar("Error: " + str(e))
                print("Internet connection lost")

    def reject(self):
        det = sm.get_screen('student details dance')
        stu_name = det.ids.stuname.text
        reg_no = det.ids.reg_no.text
        eventname = det.ids.eventname.text
        perfcat = det.ids.perfcat.text
        today = datetime.date.today()
        a = "rejected"

        # Check if the student is already shortlisted
        existing_query = f"SELECT * FROM status_of_applied_students WHERE reg_no = '{reg_no}'"
        self.cursor.execute(existing_query)
        existing_record = self.cursor.fetchone()

        if existing_record:
            # Student is already shortlisted, so update the 'shortlisted_ornot' column
            try:
                self.cursor.execute(
                    "UPDATE status_of_applied_students set date_of_response = %s, status = %s where reg_no = %s",
                    (today, a, reg_no)
                )
                self.database.commit()
                self.show_snackbar("Student status updated successfully.")
            except Exception as e:
                self.database.rollback()  # Rollback the transaction if an error occurs
                self.show_snackbar("Error: " + str(e))
        else:
            # Student is not rejected, so insert a new record
            try:
                self.cursor.execute(
                    "INSERT INTO status_of_applied_students VALUES (%s,%s,%s,%s,%s,%s) ",
                    (stu_name, reg_no, eventname, perfcat, today, a)
                )
                self.database.commit()
                self.show_snackbar("Student rejected successfully.")
            except Exception as e:
                self.database.rollback()  # Rollback the transaction if an error occurs
                self.show_snackbar("Error: " + str(e))
                print("Internet connection lost")


if __name__ == '__main__':
    DynamicButtonsApp().run()
