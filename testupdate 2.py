from modles.database import Database
from modles.user import User

Database.initialize()
User.update_user_email("Alan@test.com","Alan@gmail.com")
