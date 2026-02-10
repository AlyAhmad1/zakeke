import sys
import os

ROOT_PATH = os.path.abspath(sys.path[0])

# zakeke
ZAKEKE_LOGIN_URL = "https://admin.zakeke.com/en/Admin/user_login"
ZAKEKE_DASHBOARD_URL = "https://admin.zakeke.com/en/Admin/Dashboard"
ZAKEKE_ORDER_URL = "https://admin.zakeke.com/en/Admin/Orders"
ZAKEKE_COOKIES_FILENAME = "zakeke-cookies.pkl"
ZAKEKE_EMAIL = os.environ.get("ZAKEKE_EMAIL", "test-username")
