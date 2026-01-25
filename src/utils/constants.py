import sys
import os

ROOT_PATH = os.path.abspath(sys.path[0])

# zakeke
ZAKEKE_BASE_URL = "https://admin.zakeke.com/en/Admin/user_login"
ZAKEKE_COOKIES_FILENAME = "zakeke-cookies.pkl"
ZAKEKE_EMAIL = os.environ.get("xyz@gmail.com", "test-username")
