import DbInterface as dbi
from GCUser import GCUser
db = dbi.DbInterface()
db.deleteUser("q")
db.deleteUser("Maurice")
db.deleteUser("Joe")
db.insertUser(GCUser("q", "q"))
db.insertUser(GCUser("Maurice", "qwerty"))
db.insertUser(GCUser("Joe", "Biden"))
# ["Name", "PW Hash", "Private Key", "Public Key"]
users=db.getAllUsers()
new = []
for user in users:
    new.append(GCUser(user[0], user[1], user[2], user[3]))
pass