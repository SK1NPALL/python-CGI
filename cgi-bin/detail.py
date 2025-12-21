#!/usr/bin/env python3

import sqlite3 # import database ออกมา

conn = sqlite3.connect('mydatabase.db') #ตัวแปร connect เชื่อมกับ database ชื่อ mydatabase.db
cursor = conn.cursor() #ตัวแปร cursor ไว้ใช้ excute query

# function สร้างตาราง
def create_table() :

    # สร้างตาราง questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question_text TEXT NOT NULL
        )
     ''')
        
    # 2. สร้างตาราง Choice พร้อม Foreign Key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            choice_text TEXT NOT NULL,
            votes INTEGER DEFAULT 0,
            FOREIGN KEY (question_id) REFERENCES questions(id)
            )
    ''')
    conn.commit() #ต้องมีทุกครั้งหลังจากเปลี่ยนแปลง database

# ฟังก์ชันเพิ่มคำถาม มี parameter question
def post_questions(question) :
    
    # ใช้ cursor excute และเขียน query ให้ไปเพิมข้อมูลที่ table question
    cursor.execute("INSERT INTO questions (question_text) VALUES (?)" , (question,))
    conn.commit() # ต้องมีทุกครั้งหลังจากเปลี่ยนแปลง database
    
# เอาคอมเม้นออกเพื่อใช้ function เพิ่มคำถาม

# post_questions("What single do you like?") 
# post_questions("How many money in your pocket?")

# ฟังก์ชันเพิ่มช้อยส์ มี parameter question_id และ choice 
def post_choice( question_id , choice ):

    # ใช้ cursor excute และเขียน query ให้ไปเพิมข้อมูลที่ table choice
    cursor.execute("INSERT INTO choices (question_id , choice_text) VALUES (? , ?)" , (question_id, choice,))
    conn.commit()# ต้องมีทุกครั้งหลังจากเปลี่ยนแปลง database

# เอาคอมเม้นออกเพื่อใช้ function เพิ่มคำถาม 
# argument ตัวแรกมีไว้ระบุว่าให้เพิ่ม choice ไปที่คำถามไหน

# post_choice(4 , "15 baht")
# post_choice(4 , "1000 baht")
# post_choice(4 , "0 baht")

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

# ฟังก์ชันลบคำถามโดยใช้ระบุ id เพื่อลบ
def delete_questions(id):
    
    # ใช้ cursor execute เขียน query ให้มันลบข้อมูลตาม argument id
    cursor.execute('DELETE FROM questions WHERE id = ?' , (id,))
    conn.commit() # ต้องมีทุกครั้งหลังจากเปลี่ยนแปลง database
    

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

    # เป็น f string มีคำถามที่... : ตามด้วยคำถามที่ได้จากการ for loop
    print(f"<br> <a href='/cgi-bin/vote.py?id={q[i]['id']}'> Question {i+1} : {q[i]['question']}</a>")

print("</body>")
print("</html>")

conn.close()