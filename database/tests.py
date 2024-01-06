from models import User
from configuration import session, Base, engine


new_user = User(usernassme="John Doe", emailing=30, password="asdasdads")
# group = ChatGroup(name="86a4sd5f45sd4f")
session.add(new_user)
# session.add(group)
session.commit()
