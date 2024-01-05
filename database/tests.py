from models import User, ChatGroup
from configuration import session


new_user = User(username="John Doe", email=30, password="asdasdads")
group = ChatGroup(name="86a4sd5f45sd4f")
session.add(new_user)
session.add(group)
session.commit()
