from models import User
from configuration import session, Base, engine


new_user = User(name="John Doe", age=30)
Base.metadata.create_all(engine)
session.add(new_user)
session.commit()
