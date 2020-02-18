from datetime import datetime
from LibraryDatabase import DataBaseConnection as db
from LibraryDatabase import DataBaseCursor as dc
import uuid

conn = db()
cursorM = dc(conn)

# cursorM.execute("DROP TABLE members")

cursorM.execute("CREATE TABLE IF NOT EXISTS members(ID TEXT, NAME VARCHAR(255) , AGE INTEGER , ENTER TEXT , BORROWEDBOOK TEXT)")

cursorM.execute("CREATE TABLE IF NOT EXISTS admins(ID TEXT, NAME VARCHAR(255) , AGE INTEGER)")

conn.commit()

class Members():

    def __init__(self , name , age):
        self.name = name 
        self.age = age
        self.iD = None
        self.rentedBook = []
        self.date = datetime.now()

    def idGenerator(self):
        self.iD = uuid.uuid1()


    def expireCheck(self):
        t = self.date
        n = datetime.now()

        if (int(t.strftime("%Y")) + 1 == int(n.strftime("%Y")) and 
        t.strftime("%m") == n.strftime("%m")  and
        t.strftime("%d")  == n.strftime("%d")):
            # print("Expired!!")
            return True
        else:
            # print("Have right membership") 
            return False  

    def addMember(self):
        self.idGenerator()
        info = (str(self.iD) , self.name , self.age , str(self.date))
        # print(info)
        cursorM.execute("INSERT INTO members(ID , NAME , AGE , ENTER) VALUES(? , ? , ? , ?)" , info)   
        conn.commit()

    def addAdmin(self):
        self.idGenerator()
        info = (str(self.iD) , self.name , self.age)
        cursorM.execute("INSERT INTO admins(ID , NAME , AGE) VALUES(? , ? , ?)" , info)   
        conn.commit()


# TEST


if __name__ == "__main__":
    # m = Members('Nasim' , 18)
    # m.addAdmin()
    

    # mm = Members('Negar' , 20)
    # mm.addMember()

    # cursorM.execute("SELECT * FROM members")
    # s = cursorM.fetchall()

    # for i in s:
    #     print(i)

    # print("------------------")

    # a = Members('Hamid' , 30)
    # a.addAdmin()

    cursorM.execute("SELECT * FROM members")
    s = cursorM.fetchall()
    print(s)

    # for i in s:
    #     print(i)

