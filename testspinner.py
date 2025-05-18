import datetime

import mysql.connector
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
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
        sm.add_widget(Builder.load_file("studeshboard.kv"))
        sm.add_widget(Builder.load_file("stuprof.kv"))
        sm.add_widget(Builder.load_file("applied_events.kv"))
        return sm

    def show_applied_events_to_student(self):
        a = sm.get_screen("Student Profile")
        reg = a.ids.reg_no.text
        sm.current = "applied events"

        query = """
        SELECT a.event_name, a.performance_category, a.date_of_apply, s.status
        FROM applied_event_list a
        LEFT JOIN status_of_applied_students s ON a.reg_no = s.reg_no AND a.event_name = s.event_name
        WHERE a.reg_no = %s
        """

        self.cursor.execute(query, (reg,))
        rows = self.cursor.fetchall()
        event_list = sm.get_screen('applied events').ids.applied_events_list
        event_list.clear_widgets()

        for row in rows:
            event_name, performance_category, date_of_apply, status = row

            # Create a BoxLayout to arrange the text and icon button
            box_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)

            # Create and add the ThreeLineListItem text
            list_item = ThreeLineListItem(
                text=event_name,
                secondary_text=str(performance_category),
                tertiary_text=str(date_of_apply)
            )
            box_layout.add_widget(list_item)

            # Determine the icon and message based on status
            if status == "shortlisted":
                icon = "check"
                message = "You are selected for performance"
            elif status == "rejected":
                icon = "close"
                message = "You are rejected and you can't perform"
            else:
                icon = "eye"
                message = "Your application is under evaluation"

            # Create and add the MDIconButton
            icon_button = MDIconButton(icon=icon)
            icon_button.bind(on_release=lambda x, msg=message: self.show_status_dialog(msg))
            icon_button.padding = [0, -50, 0, 0]
            box_layout.add_widget(icon_button)

            # Add the BoxLayout to the event list
            event_list.add_widget(box_layout)

    def show_status_dialog(self, message):
        dialog = MDDialog(
            title="Status",
            text=message,
            size_hint=(0.8, 1),
            auto_dismiss=True,
            elevation=0  # Remove the shadow
        )
        dialog.open()
if __name__ == '__main__':
    DynamicButtonsApp().run()