import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="Attendance"
)

mycursor = mydb.cursor()

reader = SimpleMFRC522()


def createDatabase(mycursor):
    print("name of the db")
    name = input()
    mycursor.execute("CREATE DATABASE " + name)
    print("Database created")

#class
def createTable1(mycursor):
    print("name of the table:")
    table = input()
    sql = "CREATE TABLE " + table + " (ClassID VARCHAR(255), ClassName VARCHAR(255), Teacher VARCHAR(255))"
    mycursor.execute(sql)
    print("Table created")

#student
def createTable2(mycursor):
    mycursor.execute("CREATE TABLE student_info (ID VARCHAR(255), FirstName VARCHAR(255), LastName VARCHAR(255), NickName VARCHAR(255))")
    print("Table created")

#Attendance
def createTable3(mycursor):
    mycursor.execute("CREATE TABLE S_attendance (StudentID VARCHAR(255), ClassID VARCHAR(255), DateTime VARCHAR(255))")
    print("Table created")

def showTables(mycursor):
    mycursor.execute("SHOW TABLES")
    for row in mycursor :
        print(row)
    showTables(mycursor)
    
#add into "student_info"    
def insertStudentInfo(mycursor):
    print("Place the card")
    id, text = reader.read()
    print(id)
    FN = input('Firstname: ')
    LN = input('Lastname: ')
    NN = input('Nickname: ')
    val = (id, FN, LN, NN)
    print(val)
    sql = "INSERT INTO student_info (ID, FirstName, LastName, NickName) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, val)
    mydb.commit()
    print("finish")
    
def insertClassInfo(mycursor):
    Cid = input('Class id: ')
    CN = input('Class name: ')
    CT = input('Class teacher: ')
    val = (Cid, CN, CT)
    print(val)
    sql = "INSERT INTO Classandclub (ClassID, ClassName, Teacher) VALUES (%s, %s, %s)"
    mycursor.execute(sql, val)
    mydb.commit()
    print("finish")
    

def insertAttandance(mycursor):
    print("Place the card")
    id, text = reader.read()
    print(id)
    sql = "SELECT FirstName FROM student_info WHERE ID = id"
    mycursor.execute(sql, id)
    FN = FirstName
    print("FN")
    print("finish")
    myresult = mycursor.fetchall()
    if len(myresult) < 1:
        msql = "INSERT INTO S_attendance (StudentID, ClassID, DateTime) VALUES(%s,%s,%s)"
        valu = (StudentID, ClassID, DateTime)
        mycursor.execute(msql, valu)
        mydb.commit()
        print(mycursor.rowcount,"record added.")
    else :
        print("You already Check your Attendence")



'''
def insertVerify(mycursor,name,brand,price,origin): #INSERT WITH NO ADDRESS AND NAME THE SAME AT THE SAME TIME
    sql = "SELECT * FROM clothstore WHERE name = %s AND brand = %s"
    nd = (name, brand)
    mycursor.execute(sql,nd)
    myresult = mycursor.fetchall()
    if len(myresult) < 1:
        msql = "INSERT INTO clothstore (name,brand,price,origin) VALUES(%s,%s,%s,%s)"
        valu = (name, brand, price, origin)
        mycursor.execute(msql, valu)
        mydb.commit()
        print(mycursor.rowcount,"record added.")
    else :
        print("You already have this item")
  


def addStudent(mycursor,fName,lName,nName):
    space = ",' '"
    id,name = reader.read()
    q = "INSERT INTO students(id, firstname, lastname, nickname) VALUES(" + str(id) + ",'" + fName + "', '" + lName + "','" + nName + "')"
    print(q)
    mycursor.execute(q)
    
def showData(mycursor,table):
    mycursor.execute("SELECT * FROM "+table)
    
    myresute = mycursor.fetchall()
    
    for x in myresult:
        print(x)
        
def scanStudent():
    id,name = reader.read_no_block
    while True :
        id,name = reader.read_no_block
        mycursor.execute("SELECT * FROM scanproducts WHERE RFID = " + str(id))
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x[0] + " : "+id)
            
'''
insertAttandance(mycursor)
