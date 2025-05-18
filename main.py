import os
import re
import urllib.parse
from firebase_admin import storage
from kivy.clock import Clock
from kivy.core.text import LabelBase, Label
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.videoplayer import VideoPlayer
from kivymd.app import MDApp
from kivy.core.window import Window
import firebase_admin
from firebase_admin import credentials, initialize_app, db
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineAvatarListItem, ThreeLineListItem
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDIcon
os.environ["KIVY_VIDEO"] = "ffpyplayer"
from kivy.uix.video import Video
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
import requests
Window.size = (320, 580)



firebase_config = {
    'apiKey': "AIzaSyAxzNLk7uaaVwb-QPwq-wHs62te9iFhbd0",
    'authDomain': "test-1a93c.firebaseapp.com",
    'databaseURL': "https://test-1a93c-default-rtdb.firebaseio.com",
    'projectId': "test-1a93c",
    'storageBucket': "test-1a93c.appspot.com",
    'messagingSenderId': "308704614979",
    'appId': "1:308704614979:web:273242f5c77fafa18752f6",
    'measurementId': "G-JZWT6EWDFC",
    'serviceAccount': "serviceaccount.json"
}

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("/Users/kusha/OneDrive/Pictures/Kushal Folder/friebase private key to test project/test-1a93c-firebase-adminsdk-frbti-7c2a90570e.json")
firebase_admin.initialize_app(cred, firebase_config)



class RegistrationApp(MDApp):
    #thumbnail_url = StringProperty("")
    time_duration = StringProperty("0:00 / 0:00")
    def change_slider_value(self, instance, value):
        # Update the slider value
        sm.get_screen("main_screen").ids.slider.value = value

    def update_time_label(self, dt):
        # Update the time_duration label based on the video's position and duration
        video_widget =sm.get_screen("main_screen").ids.video
        duration = video_widget.duration
        position = video_widget.position
        self.time_duration = f"{int(position // 60)}:{int(position % 60):02d} / {int(duration // 60)}:{int(duration % 60):02d}"

    def seek(self, position):
        # Seek to the specified video position
        video_widget = sm.get_screen("main_screen").ids.video
        video_widget.position = position

        # Update the slider value
        slider = sm.get_screen("main_screen").ids.slider
        slider.max = video_widget.duration  # Set the max value to the video duration
        slider.value = min(max(position, 0), slider.max)  # Ensure the value is within valid range

        # Update the time label
        self.update_time_label(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_image,
        )

    KV_FILES = {
        os.path.join(os.getcwd(),"studenthome.kv"),
        os.path.join(os.getcwd(), "tinni.kv"),
        os.path.join(os.getcwd(), "tinni2.kv"),
        os.path.join(os.getcwd(), "course1playlistvideos.kv")
    }
    def build(self):
        self.message = "Start Your\nGrade III & Gradde IV\nLearning Journey :-))\n By Team Karimganj"
        self.typing_speed = 0.1  # Adjust the typing speed as needed
        self.current_index = 0
        self.clock_event = None
        global sm
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("splash.kv"))
        sm.add_widget(Builder.load_file("o1.kv"))
        sm.add_widget(Builder.load_file("o2.kv"))
        sm.add_widget(Builder.load_file("o3.kv"))
        sm.add_widget(Builder.load_file("login.kv"))
        sm.add_widget(Builder.load_file("selection.kv"))
        sm.add_widget(Builder.load_file("student_registration.kv"))
        sm.add_widget(Builder.load_file("add_user.kv"))
        sm.add_widget(Builder.load_file("studenthome.kv"))
        sm.add_widget(Builder.load_file("adminhome.kv"))
        sm.add_widget(Builder.load_file("course1playlistvideos.kv"))
        sm.add_widget(Builder.load_file("addcourse.kv"))
        sm.add_widget(Builder.load_file("addvideosofcourse.kv"))
        sm.add_widget(Builder.load_file("view_videsunderthesubject.kv"))
        sm.add_widget(Builder.load_file("studentprofile.kv"))
        sm.add_widget(Builder.load_file("videoplayer.kv"))
        return sm

    def toggle_thumbnail(self, button):
        # Access the thumbnail_visible attribute through the root MDScreen
        root = sm.get_screen("main_screen")
        root.ids.thumbnail.opacity = 0 if root.thumbnail_visible else 1
        root.thumbnail_visible = not root.thumbnail_visible
        if button.icon == "play":
            button.icon = "pause"
        else:
            button.icon = "play"

    def toggle_play_pause(self):
        video_widget = sm.get_screen("main_screen").ids.video
        if video_widget.state == "play":
            video_widget.state = "pause"
        else:
            video_widget.state = "play"

    def on_start(self):
        # Check if the user is already registered
        is_registered = self.check_registration_status()

        if is_registered:
            Clock.schedule_once(self.goto_login_page, 7)
        else:
            Clock.schedule_once(self.onboarding, 7)
        self.load_courses()
        self.load_coursesforadmin()
        sm.get_screen("main_screen").ids.play_pause_button.icon = "replay"
        Clock.schedule_interval(self.update_time_label, 1)


    def on_pause(self):
        # Save the video position when the app is paused
        video_widget = sm.get_screen("main_screen").ids.video
        video_widget.stop()
        return True

    def on_resume(self):
        # Resume video playback when the app is resumed
        video_widget = sm.get_screen("main_screen").ids.video
        video_widget.play()

    def toggle_volume_slider(self):
        # Toggle the visibility of the volume Slider
        volume_slider = sm.get_screen("main_screen").ids.volume_slider
        volume_label = sm.get_screen("main_screen").ids.volume_label
        volume_thumb = sm.get_screen("main_screen").ids.volume_thumb
        if volume_slider.opacity == 0:
            volume_slider.opacity = 1
            volume_label.opacity = 1
            volume_thumb.opacity = 1
        else:
            volume_slider.opacity = 0
            volume_label.opacity = 0
            volume_thumb.opacity = 0

    def change_volume(self, value):
        # Change the volume based on the Slider value
        video_widget = sm.get_screen("main_screen").ids.video
        video_widget.volume = value
        volume_label = sm.get_screen("main_screen").ids.volume_label
        volume_label.text = f"{int(value * 100)}%"

    def toggle_controls_visibility(self):
        # Toggle the visibility of the control layout
        root = sm.get_screen("main_screen")
        controls_layout = root.ids.controls
        if controls_layout.opacity == 0:
            controls_layout.opacity = 1
        else:
            controls_layout.opacity = 0

    def on_touch_down(self, touch):
        # Toggle control layout visibility when the video screen is touched
        if sm.current == "main_screen":
            root = sm.get_screen("main_screen")
            video = root.ids.video
            if video.collide_point(*touch.pos):
                self.toggle_controls_visibility()

    def goto_login_page(*args):
        sm.current = "login"

    def onboarding(self, dt):
        sm.current = "onboarding1"
        self.start_typing()

    def start_typing(self):
        if self.clock_event:
            self.clock_event.cancel()
        self.current_index = 0
        det = sm.get_screen("onboarding1")
        det.ids.message_label.text = ""
        self.clock_event = Clock.schedule_interval(self.type_next_letter, self.typing_speed)

    def type_next_letter(self, dt):
        if self.current_index < len(self.message):
            det = sm.get_screen("onboarding1")
            det.ids.message_label.text += self.message[self.current_index]
            self.current_index += 1
        else:
            self.clock_event.cancel()

    def submit_student(self, username1, email1, password1, confirm_password1, phone_number1, address1):
        # Your existing submit logic for student registration
        data = {
            "username": username1,
            "email": email1,
            "password": password1,
            "confirm_password": confirm_password1,
            "phone_number": phone_number1,
            "address": address1
        }
        ref = db.reference('student')
        ref.push(data)
    def submit_admin(self, username, email, password, confirm_password, phone_number, address):
        # Your submit logic for admin registration
        data = {
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "phone_number": phone_number,
            "address": address
        }
        ref = db.reference('admin')
        ref.push(data)

    def verify_login(self, email, password):
        ref = db.reference('student')
        result = ref.get()
        student_list = []
        if result:
            for value in result.values():
                if 'email' in value:
                    student_list.append(value)

        ref1 = db.reference('admin')
        result1 = ref1.get()
        admin_list = []
        if result1:
            for value in result1.values():
                if 'email' in value:
                    admin_list.append(value)

        if any(entry.get('email') == email for entry in student_list) and email.strip() != "":
            if result:
                for entry in result.values():
                    if 'email' in entry and entry['email'] == email:
                        if 'password' in entry and entry['password'] == password:
                            self.show_snackbar("Login successful!")
                            self.display_student_details()
                            sm.current = "studenthome"
                            self.store_email(email)
                            return
                        else:
                            self.show_password_hint()
                            return
        elif any(entry.get('email') == email for entry in admin_list) and email.strip() != "":
            if result1:
                for entry in result1.values():
                    if 'email' in entry and entry['email'] == email:
                        if 'password' in entry and entry['password'] == password:
                            self.show_snackbar("Login successful!")
                            sm.current = "adminhome"
                            return
                        else:
                            self.show_password_hint()
                            return
        else:
            self.show_email_not_found()

    def store_email(self, email):
        storage_path = self.user_data_dir  # Application storage directory
        email_file_path = os.path.join(storage_path, "stored_email.txt")

        with open(email_file_path, "w") as file:
            file.write(email)

    def read_stored_email(self):
        storage_path = self.user_data_dir  # Application storage directory
        email_file_path = os.path.join(storage_path, "stored_email.txt")

        if os.path.exists(email_file_path):
            with open(email_file_path, "r") as file:
                return file.read().strip()

        return None

    def delete_stored_email(self):
        storage_path = self.user_data_dir  # Application storage directory
        email_file_path = os.path.join(storage_path, "stored_email.txt")

        if os.path.exists(email_file_path):
            os.remove(email_file_path)
            print("Stored email deleted.")
            sm.current = 'onboarding1'
            self.show_snackbar("Logged Out Successfully")

    def check_registration_status(self):
        stored_email = self.read_stored_email()

        if stored_email:
            ref = db.reference('student')
            result = ref.get()
            student_list = [value for value in result.values()]

            email_exists = any(entry['email'] == stored_email for entry in student_list)
            return email_exists
        elif stored_email:
            ref = db.reference('admin')
            result = ref.get()
            admin_list = [value for value in result.values()]
            email_exists = any(entry['email'] == stored_email for entry in admin_list)
            return email_exists


        return False
    def show_snackbar(self, text):
        snackbar = Snackbar(text=text)
        snackbar.open()

    def show_password_hint(self):
        self.show_snackbar("Please provide the correct password.")

    def show_email_not_found(self):
        self.show_snackbar("Email does not exist.")




    def open_file_manager(self):
        self.file_manager.show('/')  # You can change the initial directory as needed
        #file_manager.bind(on_select=self.select_image)

    def select_image(self, path):
        if path:
            # Upload the selected image to Firebase Storage
            try:
                # You should have initialized Firebase Storage earlier in your code
                #storage = firebase_admin.storage()
                bucket = storage.bucket()

                # Define a unique filename (you can use course ID or any other identifier)
                unique_filename = "course_thumbnail.png"

                # Upload the image to Firebase Storage
                blob = bucket.blob(unique_filename)
                blob.upload_from_filename(path)

                # Get the URL of the uploaded image
                image_url = blob.generate_signed_url(expiration=315360000)  # Adjust the expiration time as needed  # Expires in 10 years

                det = sm.get_screen("addcourse")
                course_data = {
                    "Subject_ID": det.ids.addsubjectid.text,
                    "subject_name": det.ids.addsubjectname.text,
                    "teacher_name": det.ids.addteachername.text,
                    "starting_date": det.ids.addstartingdate.text,
                    "thumbnail_url": image_url,  # Save the image URL in your course data
                    # Add more fields here as needed
                }

                # Push the course data to the Firebase Realtime Database under a "courses" node
                ref = db.reference('courses')
                ref.push(course_data)

                # Show a success message
                self.show_snackbar("Course added successfully!")

                # Close the file manager
                self.file_manager.close()
            except Exception as e:
                # Handle any exceptions that may occur during image upload
                print("Error:", str(e))
                self.show_snackbar("An error occurred while adding the course.")
    def exit_file_manager(self, *args):
        self.file_manager.close()
    def load_courses(self):
        # Retrieve course data from Firebase Realtime Database
        ref = db.reference('courses')
        result = ref.get()

        # Clear the existing course items in the list
        card_list = self.root.get_screen("studenthome").ids.hula_list
        card_list.clear_widgets()

        if result:
            for course_id, course_data in result.items():
                # Create an instance of CardItem widget using Factory
                card_item = Factory.CardItem()

                # Set the data for the CardItem
                card_item.ids.coursename.text = course_data.get("subject_name", "Course Name")
                card_item.ids.coursestartingdate.text = course_data.get("starting_date", "Starting Date")
                card_item.ids.courseteachername.text = course_data.get("teacher_name", "Teacher Name")
                card_item.ids.coursesid.text = course_data.get("Subject_ID", "Subject ID")
                course_id = course_data.get("Subject_ID", "Subject ID")
                card_item.bind(on_release=lambda instance, course_id=course_id: self.gotocourse1videos(course_id))

                # Load the course thumbnail image dynamically from the URL
                #thumbnail_url = course_data.get("thumbnail_url", "")
                # if thumbnail_url:
                #     card_item.ids.thumbnailimage.source = thumbnail_url
                # Add the CardItem to the MDList
                card_list.add_widget(card_item)
    def gotocourse1videos(self,course_id):
        self.add_course_to_study_history(course_id)
        course1video_screen = sm.get_screen("course1videos")
        course1video_screen.course_id = course_id
        #
        #     # Switch to the "addvideosofcourse" screen
        sm.current = "course1videos"
        self.display_videos_for_student(course_id)
    def sanitize_path(self, path):
        # Replace illegal characters in the path with underscores
        return re.sub(r'[.$#/[\]]', '_', path)

    def add_course_to_study_history(self, course_id):
        # Get the currently logged-in student's email
        email = self.read_stored_email()

        if email:
            # Retrieve the course details from Firebase based on course_id
            ref = db.reference(f'courses/{course_id}')
            course_data = ref.get()

            if course_data:
                # Create a dictionary containing course details
                course_history_data = {
                    "Subject_ID": course_data.get("Subject_ID", ""),
                    "subject_name": course_data.get("subject_name", ""),
                    "teacher_name": course_data.get("teacher_name", ""),
                    "starting_date": course_data.get("starting_date", ""),
                    "thumbnail_url": course_data.get("thumbnail_url", ""),
                    # Add other course details as needed
                }

                # Sanitize the student's email for use as a key
                encoded_email = urllib.parse.quote_plus(email)
                sanitized_email = self.sanitize_path(encoded_email)

                # Store the course details in the student's study history
                study_history_ref = db.reference(f'student/{sanitized_email}/study_history')

                # Generate a unique key for the new study history entry
                new_study_history_key = study_history_ref.push().key

                # Insert the course details into the study history
                study_history_ref.child(new_study_history_key).set(course_history_data)

                # Show a success message
                self.show_snackbar("Course added to study history successfully!")
            else:
                self.show_snackbar("Course not found in the database.")
        else:
            self.show_snackbar("Student email not found.")

            #ref.push(course_history_data)
    def display_videos_for_student(self, course_id):
        # Reference to the videos under the specified course ID
        ref = db.reference(f'courses/{course_id}/videos')

        # Get the video data from Firebase
        video_data = ref.get()

        # Clear the existing list items
        view_video_list = self.root.get_screen("course1videos").ids.course1_list
        view_video_list.clear_widgets()

        if video_data:
            for video_id, video_details in video_data.items():
                #video_item_layout = BoxLayout(orientation='horizontal',size_hint_y=None, height=100)

                # Create an MDListItem for each video
                video_item = ThreeLineListItem(
                    text=video_details.get("lesson_name", ""),
                    secondary_text=video_details.get("lesson_description", ""),
                    tertiary_text=video_details.get("video_url", "")
                )
                # delete_button.bind(on_release=lambda btn,video_id=video_id: self.delete_video(course_id, video_id))
                # video_item_layout.add_widget(video_item)
                # video_item_layout.add_widget(delete_button)
                video_item.bind(on_release=lambda item, video_id=video_id: self.navigate_to_videos(video_id))
                # Add the video item to the MDList
                view_video_list.add_widget(video_item)
        else:
            # If there is no content available, display a message
            no_content_label = MDLabel(
                text="NO CONTENTS AVAILABLE",
                halign="center",
                valign="middle",
                #size_hint_y=None,
                #height=dp(48),  # Set the desired height
                pos_hint={"center_x": 0.5, "center_y": 0.5}  # Adjust the position as needed
            )
            view_video_list.add_widget(no_content_label)

    def navigate_to_videos(self, video_id):
        sm.current = "main_screen"

        # Get the course ID from the current screen
        course_id = self.root.get_screen("course1videos").course_id

        # Retrieve the video details from Firebase based on video_id
        ref = db.reference(f'courses/{course_id}/videos/{video_id}')
        video_data = ref.get()

        if video_data:
            lesson_name = video_data.get("lesson_name", "")
            det = sm.get_screen("main_screen")
            det.ids.lessonname.text = lesson_name
            lessondescription = video_data.get("lesson_description", "")
            det.ids.lessondescription.text = lessondescription



            video_url = video_data.get("video_url", "")
            print(video_url)
            det = sm.get_screen("main_screen")
            det.ids.video.source = video_url
        else:
            self.show_snackbar("Video not found.")


    def load_coursesforadmin(self):
        # Retrieve course data from Firebase Realtime Database
        ref = db.reference('courses')
        result = ref.get()

        # Clear the existing course items in the list
        card_list = self.root.get_screen("adminhome").ids.ourcourse_list
        card_list.clear_widgets()

        if result:
            for course_id, course_data in result.items():
                # Create an instance of CardItem widget using Factory
                card_item = Factory.CardItems()

                # Set the data for the CardItem
                card_item.ids.coursename.text = course_data.get("subject_name", "Course Name")
                card_item.ids.coursestartingdate.text = course_data.get("starting_date", "Starting Date")
                card_item.ids.courseteachername.text = course_data.get("teacher_name", "Teacher Name")
                card_item.ids.coursesid.text = course_data.get("Subject_ID", "Subject ID")
                course_id = course_data.get("Subject_ID", "Subject ID")
                print(course_id)
                card_item.bind(on_release=lambda instance, course_id=course_id: self.gotocourse1videos(course_id))
                # Load the course thumbnail image dynamically from the URL
                thumbnail_url = course_data.get("thumbnail_url", "")
                #thumbnail_url = "https://firebasestorage.googleapis.com/v0/b/test-1a93c.appspot.com/o/course_thumbnail.png?alt=media&token=0fbb8353-a154-4e5d-a5a0-da77a2b51966"
                # if thumbnail_url:
                #     try:
                #         card_item.ids.hula.source = thumbnail_url
                #     except Exception as e:
                #         # Handle the exception here
                #         print(f"An error occurred: {e}")
                # # Add the CardItem to the MDList
                #thumbnail_url = course_data.get("thumbnail_url", "")
                card_list.add_widget(card_item)



    def gotocourse1videosadmin(self, course_id):
    #     # Set the course_id attribute of the "addvideosofcourse" screen
        addvideos_screen = sm.get_screen("addvideosofcourse")
        addvideos_screen.course_id = course_id
    #
    #     # Switch to the "addvideosofcourse" screen
        sm.current = "viewvideostoadmin"
        self.display_videos_for_admin(course_id)
    def submit_video(self, course_id):
        lesson_name = self.root.get_screen("addvideosofcourse").ids.lessonname.text
        lesson_description = self.root.get_screen("addvideosofcourse").ids.lessondescription.text
        video_url = self.root.get_screen("addvideosofcourse").ids.videourl.text

        # Create a dictionary containing video details
        video_data = {
            "lesson_name": lesson_name,
            "lesson_description": lesson_description,
            "video_url": video_url,
            # Add other video details as needed
        }

        # Push the video data to the Firebase Realtime Database under the specified course ID
        ref = db.reference(f'courses/{course_id}/videos')
        ref.push(video_data)

        # Show a success message or perform any other desired actions
        self.show_snackbar("Video added successfully!")

        # Clear the text fields after submission (optional)
        self.root.get_screen("addvideosofcourse").ids.lessonname.text = ""
        self.root.get_screen("addvideosofcourse").ids.lessondescription.text = ""
        self.root.get_screen("addvideosofcourse").ids.videourl.text = ""
        self.display_videos_for_admin(course_id)
    #
    #
    # def display_videos_for_admin(self, course_id):
    #     # Reference to the videos under the specified course ID
    #     ref = db.reference(f'courses/{course_id}/videos')
    #
    #     # Get the video data from Firebase
    #     video_data = ref.get()
    #
    #     # Clear the existing list items
    #     view_video_list = self.root.get_screen("viewvideostoadmin").ids.viewvideoliststoadmin
    #     view_video_list.clear_widgets()
    #
    #     if video_data:
    #         for video_id, video_details in video_data.items():
    #             # Create an MDListItem for each video
    #             video_item = ThreeLineAvatarListItem(
    #                 text=video_details.get("lesson_name", ""),
    #                 secondary_text=video_details.get("lesson_description", ""),
    #                 tertiary_text=video_details.get("video_url", "")
    #             )
    #
    #             # Add the video item to the MDList
    #             view_video_list.add_widget(video_item)

    def delete_video(self, course_id, video_id):
        # Reference to the specific video under the course ID
        ref = db.reference(f'courses/{course_id}/videos/{video_id}')

        try:
            # Delete the video entry from the Firebase Realtime Database
            ref.delete()
            self.show_snackbar("Video deleted successfully!")
            self.display_videos_for_admin(course_id)
        except Exception as e:
            print(f"An error occurred while deleting the video: {e}")
            self.show_snackbar("An error occurred while deleting the video.")

    def display_videos_for_admin(self, course_id):
        # Reference to the videos under the specified course ID
        ref = db.reference(f'courses/{course_id}/videos')

        # Get the video data from Firebase
        video_data = ref.get()

        # Clear the existing list items
        view_video_list = self.root.get_screen("viewvideostoadmin").ids.viewvideoliststoadmin
        view_video_list.clear_widgets()

        if video_data:
            for video_id, video_details in video_data.items():
                video_item_layout = BoxLayout(orientation='horizontal',size_hint_y=None, height=100)

                # Create an MDListItem for each video
                video_item = ThreeLineListItem(
                    text=video_details.get("lesson_name", ""),
                    secondary_text=video_details.get("lesson_description", ""),
                    tertiary_text=video_details.get("video_url", "")
                )
                delete_button = MDIconButton(
                    icon='trash-can-outline',
                    size_hint=(None, None),
                )
                delete_button.bind(on_release=lambda btn,video_id=video_id: self.delete_video(course_id, video_id))
                video_item_layout.add_widget(video_item)
                video_item_layout.add_widget(delete_button)

                # Add the video item to the MDList
                view_video_list.add_widget(video_item_layout)
        else:
            # If there is no content available, display a message
            no_content_label = MDLabel(
                text="NO CONTENTS AVAILABLE",
                halign="center",
                valign="middle",
                #size_hint_y=None,
                #height=dp(48),  # Set the desired height
                pos_hint={"center_x": 0.5, "center_y": 0.5}  # Adjust the position as needed
            )
            view_video_list.add_widget(no_content_label)

    class ProfileCard(FakeRectangularElevationBehavior, MDFloatLayout):
        pass

    def display_student_details(self):
        ref = db.reference('student')
        result = ref.get()
        det = sm.get_screen("login")
        email = det.ids.email.text
        if result:
            for entry in result.values():
                if entry['email'] == email:
                    # Populate the MDLabel widgets with student details
                    self.root.get_screen("studentprofile").ids.student_id_label.text = f"Student ID: {entry['username']}"
                    self.root.get_screen("studentprofile").ids.email_id.text = f"Email: {entry['email']}"
                    self.root.get_screen("studentprofile").ids.phoneno.text = f"Phone Number: {entry['phone_number']}"
                    # Add other details as needed

                    # Show the "studentprofile" screen
                    sm.current = "studentprofile"
                    return







if __name__ == '__main__':
    LabelBase.register(name='MPoppins', fn_regular=("Poppins Medium 500.ttf"))
    LabelBase.register(name='BPoppins', fn_regular=("Poppins Light 300.ttf"))
    LabelBase.register(name='CPoppins', fn_regular=("Poppins ExtraBold Italic 800.ttf"))
    LabelBase.register(name='DPoppins', fn_regular=("Poppins SemiBold 600.ttf"))
    LabelBase.register(name='EPoppins', fn_regular=("Design-System-C-W01-900R.ttf"))
    RegistrationApp().run()
