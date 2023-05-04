from app import app
from models import db, User, Feedback


db.drop_all()
db.create_all()


# user1 = User(
#   username = "dogbestfriend",
#   password = "doglover123",
#   email = "dog@lover.com",
#   first_name = "Jay",
#   last_name = "Blanchett"
# )
user1 = User.register("dogbestfriend", "doglover123", "dog@lover.com", "Jay", "Blanchett")


user2 = User.register("catbestfriend", "catlover123", "cat@lover.com", "Sam", "Blanchett")


db.session.add_all([user1, user2])
db.session.commit()


feedback1 = Feedback(
  title = "Title 1",  
  content = "Body content of feedback. ",
  username = "catbestfriend"

)

feedback2 = Feedback(
  title = "Title 2",  
  content = "Body 2 content of feedback. ",
  username = "dogbestfriend"

)

db.session.add_all([feedback1, feedback2])
db.session.commit()
