from backends.database import Database
from backends.user import User

Database.setup()
User.update_user_email("dolly@321.com", "dolly@123.com")
# User.update_user_email("dolly@11.com", "dolly@22.com")
# User.update_user_email("dolly@22.com", "dolly@33.com")
# User.update_user_email("dolly@33.com", "dolly@44.com")
# User.update_user_email("dolly@44.com", "dolly@55.com")



