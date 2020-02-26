import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from time import sleep

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="Attendance"
)

mycursor = mydb.cursor()

reader = SimpleMFRC522()

from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)



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
    

def insertAttandance(mycursor, StudentID, ClassID):
    Q = "INSERT INTO S_attendance(StudentID, ClassID, DateTime) VALUES('" + str(StudentID) + "' , " + str(ClassID) + ", NOW())"
    print(Q)
    mycursor.execute(Q)
    print("Checked")
    mydb.commit()
    
def findClassClub(mycursor):
    print("Which class? (ID)")
    classclub = input()
    mycursor.execute("SELECT ClassName FROM Classandclub WHERE ClassID = '" + classclub + "'")
    myresult = mycursor.fetchall()
    ClassID = 0
    for x in myresult:
        ClassID = x[0]
    return ClassID
    
def checkAttendance(mycursor):
    print("Scan your card")
    lcd.write_string("Scan your card\n\r")
    ClassID = findClassClub(mycursor)
    while True:
        id, name = reader.read_no_block()
        if id != None:
            mycursor.execute("SELECT * FROM student_info WHERE id = " + str(id))
            
            myresult = mycursor.fetchall()
            
            for x in myresult:
                lcd.clear()
                print(x[0]+ " : " + str(id))
                lcd.write_string(x[0] + "\n\r" + x[2])
                sleep(1)
                print("\nScan Your card")
                lcd.clear()
                insertAttandance(mycursor, StudentID, ClassID)
    
    
#insertStudentInfo(mycursor)

checkAttendance(mycursor)