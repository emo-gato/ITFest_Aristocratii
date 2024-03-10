from UserApp import UserApp
from kivy.app import App
from kivy.uix.widget import Widget
import pymysql
from argon2 import PasswordHasher

from AdminApp import MapManager
from simulation import MapApp


class LoginWindow(Widget):
    def on_kv_post(self, base_widget):
        pass

    def sign_in(self):
        # Get the username and password from the input fields
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        conn = pymysql.Connect(host="db-itfest2024.a.aivencloud.com",
                               user="avnadmin",
                               port=23532,
                               password="AVNS_GcjwTb1VbaBDbhRn24R",
                               database="defaultdb")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `users` WHERE username = %s;", (username,))
        res = cursor.fetchone()
        if res and PasswordHasher().verify(hash=res[2], password=password):
            if res[3] == 1:
                app_instance = MapManager()
                app_instance.run()
            else:
                MapApp().run()
        else:
            print("Login failed")

        # Close the database connection
        conn.close()


class LoginApp(App):
    def build(self):
        return LoginWindow()


if __name__ == '__main__':
    LoginApp().run()