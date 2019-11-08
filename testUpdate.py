from backends.database import Database
from backends.user import User

Database.initialize()
User.update_user_email("dolly@321.com", "dolly@123.com")