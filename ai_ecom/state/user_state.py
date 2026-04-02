import reflex as rx
import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

class UserState(rx.State):
    """Handles Firebase Authentication + Mapping to Dataset user_id"""

    firebase_uid: str = rx.LocalStorage("")
    user_id: str = rx.LocalStorage("")           # This will store the integer ID from dataset
    email: str = rx.LocalStorage("")
    logged_in: bool = rx.LocalStorage(False)
    user_type: str = rx.LocalStorage("new")      # "new" or "old"
    error_message: str = ""

    # Login Form
    login_email: str = ""
    login_password: str = ""
    signup_name: str = rx.LocalStorage("")
    signup_email: str = ""
    signup_password: str = ""

    @rx.var
    def user_name(self) -> str:
        if self.signup_name:
            return self.signup_name
        if self.email:
            return self.email.split("@")[0]
        return ""

    def set_login_email(self, value: str):
        self.login_email = value

    def set_login_password(self, value: str):
        self.login_password = value

    def set_signup_name(self, value: str):
        self.signup_name = value

    def set_signup_email(self, value: str):
        self.signup_email = value

    def set_signup_password(self, value: str):
        self.signup_password = value

    def _map_firebase_to_dataset(self, is_new: bool = False):
        """Create or find mapping between Firebase UID and dataset user_id"""
        # Get absolute path to mapping file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mapping_dir = os.path.join(os.path.dirname(current_dir), "backend", "data")
        mapping_path = os.path.join(mapping_dir, "user_mapping.csv")

        if not os.path.exists(mapping_dir):
            os.makedirs(mapping_dir, exist_ok=True)

        # Load or create mapping file
        if os.path.exists(mapping_path):
            mapping = pd.read_csv(mapping_path)
        else:
            mapping = pd.DataFrame(columns=["firebase_uid", "dataset_user_id"])

        # Check if this Firebase user already has a dataset ID
        existing = mapping[mapping["firebase_uid"] == self.firebase_uid]

        if not existing.empty:
            # Returning user
            self.user_id = str(existing.iloc[0]["dataset_user_id"])
            self.user_type = "old"
        else:
            # New user - assign next available integer ID
            if len(mapping) == 0:
                new_id = 1
            else:
                new_id = int(mapping["dataset_user_id"].max()) + 1

            # Add new mapping
            new_row = pd.DataFrame([{
                "firebase_uid": self.firebase_uid,
                "dataset_user_id": new_id
            }])
            mapping = pd.concat([mapping, new_row], ignore_index=True)
            mapping.to_csv(mapping_path, index=False)

            self.user_id = str(new_id)
            self.user_type = "new" if is_new else "old"

    def login(self):
        if not self.login_email or not self.login_password:
            self.error_message = "Please enter email and password"
            return

        api_key = os.getenv("FIREBASE_API_KEY", "YOUR_FIREBASE_WEB_API_KEY_HERE")

        if api_key == "YOUR_FIREBASE_WEB_API_KEY_HERE":
            # MOCK LOGIN for local development
            print("Using MOCK LOGIN")
            self.firebase_uid = f"mock_{self.login_email.split('@')[0]}"
            self.email = self.login_email
            self.logged_in = True
            self.error_message = ""
            self._map_firebase_to_dataset(is_new=False)
            return rx.redirect("/")

        try:
            payload = {
                "email": self.login_email,
                "password": self.login_password,
                "returnSecureToken": True
            }

            response = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
                json=payload
            )
            data = response.json()

            if "error" in data:
                self.error_message = data["error"]["message"].replace("_", " ")
                return

            self.firebase_uid = data["localId"]
            self.email = self.login_email
            self.logged_in = True
            self.error_message = ""

            self._map_firebase_to_dataset(is_new=False)
            return rx.redirect("/")

        except Exception as e:
            self.error_message = f"Login failed: {str(e)}"

    def signup(self):
        if not self.signup_email or not self.signup_password or not self.signup_name:
            self.error_message = "Please fill all fields"
            return

        api_key = os.getenv("FIREBASE_API_KEY", "YOUR_FIREBASE_WEB_API_KEY_HERE")

        if api_key == "YOUR_FIREBASE_WEB_API_KEY_HERE":
            # MOCK SIGNUP for local development
            print("Using MOCK SIGNUP")
            self.firebase_uid = f"mock_{self.signup_email.split('@')[0]}"
            self.email = self.signup_email
            self.logged_in = True
            self.error_message = ""
            self._map_firebase_to_dataset(is_new=True)
            return rx.redirect("/")

        try:
            payload = {
                "email": self.signup_email,
                "password": self.signup_password,
                "returnSecureToken": True
            }

            response = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}",
                json=payload
            )
            data = response.json()

            if "error" in data:
                self.error_message = data["error"]["message"].replace("_", " ")
                return

            self.firebase_uid = data["localId"]
            self.email = self.signup_email
            self.logged_in = True
            self.error_message = ""

            self._map_firebase_to_dataset(is_new=True)
            return rx.redirect("/")

        except Exception as e:
            self.error_message = f"Signup failed: {str(e)}"

    def logout(self):
        self.firebase_uid = ""
        self.user_id = ""
        self.email = ""
        self.logged_in = False
        self.user_type = "new"
        self.error_message = ""
        self.login_email = ""
        self.login_password = ""
        self.signup_name = ""
        self.signup_email = ""
        self.signup_password = ""
        return [rx.toast("Logged out successfully"), rx.redirect("/login")]
