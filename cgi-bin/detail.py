#!/usr/bin/env python3

import sqlite3 # import database ออกมา

conn = sqlite3.connect('mydatabase.db') #ตัวแปร connect เชื่อมกับ database ชื่อ mydatabase.db
cursor = conn.cursor() #ตัวแปร cursor ไว้ใช้ excute query

# ฟังก์ชันดึงข้อมูลคำถาม และแปลงจาก tuple เป็น list
def get_questions():
    
    # ไว้เก็บค่าจากการ for loopขอช้อยส์
    questions_list = []

    # ใช้ cursor excute ขอข้อมูลจาก table questions
    cursor.execute('SELECT * FROM questions')

    # เก็บขอมูลไว้ในตัวแปร rows ยังเป็น tuple อยู่
    rows = cursor.fetchall()
    
    # วนค่า tuple ภายในตัวแปร rows
    for i in range(len(rows)) :
        
        # เพิ่มค่าที่เป็น dictionary เข้าไปใน list โดยมี key ID และ QUESTION
        questions_list.append({"id" : rows[i][0], "question" : rows[i][1] })
        
    # return list กลับไป
    return questions_list

# ฟังก์ชันดึงข้อมูลช้อยส์มาแปลงจาก tuple เป็น list
def get_choice() :

    # ตัวแปรเก็บค่า choice ที่ถูกวนภายใน for loop
    choice_list = []

    # ใช้ cursor execute ขอข้อมูลจาก table choices
    cursor.execute('SELECT * FROM choices')
    # เก็บค่าที่ได้ไว้ภายในตัวแปร rows
    rows = cursor.fetchall()
    
    # วนค่าที่เป็น tuple ภายในตัวแปร rows
    for i in range(len(rows)) :
        
        # เพิ่มค่าที่เป็น dictionary เข้าโดยมี key ID , question_id และ choice
        choice_list.append({"id" : rows[i][0] ,"question_id" : rows[i][1], "choice" : rows[i][2] })
        
        
    return choice_list

# ตัวแปรที่เก็บค่า q = question และ c = choice
q = get_questions()
c = get_choice()
    
# Required header that tells the browser how to render the output
print("Content-Type: text/html")
print()  # A blank line to end the headers

# Start of the HTML content
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("    <title>Python CGI Example</title>")
print("</head>")
print("<body>")
print("    <h1>List of Questions</h1>")

# ใช้ loop เพื่อวนค่าภายใน q เพื่อดูว่ามี คำถามกี่คำถามและให้ แสดงออกมาที่หน้าเว็บ
for i in range(len(q)):

    # แสดงปุ่มให้เลือกคำถาม แล้วส่ง query string ไปเมื่อไปยัง path อื่น
    print(f"<br> <a href='/cgi-bin/vote.py?id={q[i]['id']}'> Question {i+1} : {q[i]['question']}</a>")

print("</body>")
print("</html>")

conn.close()