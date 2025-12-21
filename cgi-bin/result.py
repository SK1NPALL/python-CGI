#!/usr/bin/env python3
import cgi
import sqlite3 # import database ออกมา

form = cgi.FieldStorage()

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
        choice_list.append({"id" : rows[i][0] ,"question_id" : rows[i][1], "choice" : rows[i][2] , "vote" : rows[i][3]})
        
    return choice_list


# ตัวแปรที่จะมาจัดการบวกผลโหวตหลังจากกดโหวตไปแล้ว
# ใช้ id choice ของเราและบวกค่า votes ด้วยการเขียน query
def vote_handle() : 

    cursor.execute("UPDATE choices SET votes = votes + 1 WHERE id = ?",(choice_target_id,))
    conn.commit()

# เก็บค่า choice id ที่ถูกส่งมาในตัวแปร choice_target_id
choice_target_id = int(form.getvalue('selected_choice'))

# รันฟังก์ชันเพื่อทำการบวกค่า votes
vote_handle()

q = get_questions()
c = get_choice()

question_target = ''

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


print("<h1>Vote result</h1>")

# ค่าที่รับมาจาก url มันเป็น id ของ choice แต่เราต้องการหาว่า choice นั้นตรงกับ question id ที่เท่าไหร่ 
# พูดง่ายๆ วนลูปหาว่ามันเป็นช้อยส์ของคำถามไหน ถ้าเจอก็เก็บในตัวแปร question_target 
for i in range(len(c)) :

    if (choice_target_id == c[i]['id']) :

        question_target = c[i]['question_id']


# วนซ้ำใน q ถ้า id ตรงกับ question target ก็ให้แสดงผลออกมา
for i in range(len(q)) :

    if (question_target == q[i]['id']) :
        print(f'<h2> Question : {q[i]['question']}</h2>')

# สร้าง loop j เพื่อวน choice และแสดง value ออกมา
for j in range(len(c)) :

    if (question_target == c[j]['question_id']):

        print(f"""
            
            <p">{c[j]['choice']} ----- vote: {c[j]['vote']}</p> 
    
        """)

# ปุ่ม a เพื่อบอกว่าต้องการโหวตอีกครั้งไหม แล้วเปลี่ยน path ไปยัง vote.py พร้อม id ของคำถามนั้น
print(f"<a href='/cgi-bin/vote.py?id={question_target}'>Vote again?</a>")

print("</body>")
print("</html>")