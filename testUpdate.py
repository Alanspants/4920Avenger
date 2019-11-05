from modules.database import Database
from modules.user import User

Database.initialize()
User.update_user_email("dolly@321.com", "dolly@123.com")