from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
import requests
import webbrowser
from plyer import filechooser
# from android.permissions import request_permissions, Permission

# KV = Builder.load_file("main.kv")

class WindowManager(ScreenManager):
    pass

class Login(Screen):
    def login(self, username, password):
        url = "https://jobboard.pythonanywhere.com/api/accounts/login"
        payload={'username': username,
        'password': password}
        banner = self.manager.get_screen("login_screen").ids.banner
        try:
            response = requests.request("POST", url, data=payload)
        except Exception:
            banner.text = ["Server Connection Failed, Check your internet connection please."]
            banner.show()
            return False
        response_data = response.json()
        if response.ok:
            token = response_data["token"]
            self.manager.get_screen("profile_screen").profile(token)
            return token
        banner.text = ["Incorrect Username or Password"]
        banner.show()
        return False

class Signup(Screen):
    def signup(self, un,fn, ln, em, pw1, pw2):
        url = "https://jobboard.pythonanywhere.com/api/accounts/sign_up"
        
        payload={'username': un,
        'first_name': fn,
        'last_name': ln,
        'email': em,
        'password1': pw1,
        'password2': pw2}
        banner = self.manager.get_screen("signup_screen").ids.banner
        try:
            response = requests.request("POST", url, data=payload)
        except Exception:
            banner.text = ["Server Connection Failed, Check your internet connection please."]
            banner.show()
            return False
        response_data = response.json()
        if response.ok:
            self.manager.get_screen("login_screen").login(un, pw2)
            return True
        
        error = ""
        for i in response_data.values():
            error += "\n" + "".join(i)
        
        banner.text = [error] if not error.__contains__("This field is required.") else ["All fields are required"]
        banner.show()
        
        return False

class Profile(Screen):
    def profile(self, token):
        url = "https://jobboard.pythonanywhere.com/api/accounts/profile/"
        headers = {
            'Authorization': f'token {token}'
        }
        banner = self.manager.get_screen("profile_screen").ids.banner
        try:
            response = requests.request("GET", url, headers=headers)
        except Exception:
            banner.text = ["Server Connection Failed, Check your internet connection please."]
            banner.show()
            return False
        response_data = response.json()
        profile_data = response_data["profile"]
        screen_ids = self.manager.get_screen("profile_screen").ids
        screen_ids.image.source = f'https://jobboard.pythonanywhere.com{profile_data["image"]}' if profile_data["image"] else "imgs/profile.png"
        screen_ids.username_label.text = profile_data["username"]
        screen_ids.name_label.text = f'{profile_data["first_name"]} {profile_data["last_name"]}'
        screen_ids.email_label.text = profile_data["email"]
        screen_ids.phone_label.text = profile_data["phone_number"] if profile_data["phone_number"] else "Edit your profile to enter your phone number"
        screen_ids.city_label.text = profile_data["city"] if profile_data["city"] else "Edit your profile to enter your city"
        screen_ids.token_label.text = response_data["token"]
    
    def default_val(self, token):  # default values for the inputs of the edit_profile_screen
        url = "https://jobboard.pythonanywhere.com/api/accounts/profile/"
        headers = {
            'Authorization': f'token {token}'
        }
        banner = self.manager.get_screen("profile_screen").ids.banner
        try:
            response = requests.request("GET", url, headers=headers)
        except Exception:
            banner.text = ["Server Connection Failed, Check your internet connection please."]
            banner.show()
            return False
        response_data = response.json()
        profile_data = response_data["profile"]
        screen_ids = self.manager.get_screen("edit_profile_screen").ids
        screen_ids.image.source = f'https://jobboard.pythonanywhere.com{profile_data["image"]}' if profile_data["image"] else "imgs/profile.png"
        screen_ids.username_input.text = profile_data["username"]
        screen_ids.fname_input.text = profile_data["first_name"]
        screen_ids.lname_input.text = profile_data["last_name"]
        screen_ids.email_input.text = profile_data["email"]
        screen_ids.phone_input.text = profile_data["phone_number"] if profile_data["phone_number"] else ""
        screen_ids.city_input.text = profile_data["city"] if profile_data["city"] else ""
        return True
    
    def open_web(self):
        webbrowser.open('https://jobboard.pythonanywhere.com')

class ChangePass(Screen):
    def change_pass(self, op, np, npc):
        url = "https://jobboard.pythonanywhere.com/api/accounts/profile/password_change"
        
        payload={'old_password': op,
        'new_password1': np,
        'new_password2': npc}
        token = self.manager.get_screen("profile_screen").ids.token_label.text
        headers = {
            'Authorization': f'token {token}'
        }
        banner = self.manager.get_screen("change_password_screen").ids.banner
        try:
            response = requests.request("PUT", url, headers=headers, data=payload)
        except Exception:
            banner.text = ["Server Connection Failed, Check your internet connection please."]
            banner.show()
            return False
        response_data = response.json()
        if response.ok:
            banner = self.manager.get_screen("profile_screen").ids.banner
            banner.text = ["Password Changed Successfully"]
            banner.show()
            return True
        
        error = ""
        for i in response_data.values():
            error += "\n" + "".join(i)
        
        banner.text = [error] if not error.__contains__("This field is required.") else ["All fields are required"]
        banner.show()
        
        return False

class EditProfile(Screen):
    def open_file_manager(self):
        # request_permissions([Permission.READ_EXTERNAL_STORAGE])
        filechooser.open_file(on_selection=self.select_path)
    
    def select_path(self, path):
        if path:
            self.manager.get_screen("edit_profile_screen").ids.image.source = str(path[0])
    
    def edit_profile(self, un, fn, ln, em, pn, ci, img):
        url = "https://jobboard.pythonanywhere.com/api/accounts/profile/edit"
        
        payload={'username': un,
        'first_name': fn,
        'last_name': ln,
        'email': em,
        'phone_number': pn,
        'city': ci}
        files = {}
        current_image = self.manager.get_screen("profile_screen").ids.image.source
        banner = self.manager.get_screen("edit_profile_screen").ids.banner
        if img != current_image:
            try:
                files=files={'image': open(img,'rb')}
            except Exception:
                banner.text = ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."]
                banner.show()
                return False
        token = self.manager.get_screen("profile_screen").ids.token_label.text
        headers = {
            'Authorization': f'token {token}'
        }
        
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, files=files)
        except Exception:
            banner.text = ["Server Connection Failed, Check your internet connection please."]
            banner.show()
            return False
        response_data = response.json()
        if response.ok:
            banner = self.manager.get_screen("profile_screen").ids.banner
            banner.text = ["Profile Edited Successfully"]
            self.manager.get_screen("profile_screen").profile(token)
            banner.show()
            return True
        
        error = ""
        for i in response_data.values():
            error += "\n" + "".join(i)
        
        banner.text = [error] if not error.__contains__("This field is required.") else ["All fields are required except Image, City and Phone Number fields"]
        banner.show()
        
        return False


class Main(MDApp):
    def portfolio(self):
        webbrowser.open('https://m074med.github.io/My_Portfolio/')
    
    def build(self):
        self.title = "Job Board App"
        return WindowManager()

if __name__ == '__main__':
    Main().run()
