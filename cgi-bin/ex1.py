#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

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
    conn.commit()

# ฟังก์ชันเพิ่มคำถาม

def post_questions(question) :
    
    cursor.execute("INSERT INTO questions (question_text) VALUES (?)" , (question,))
    conn.commit()
    
    
# post_questions("What single do you like?")
# post_questions("How many money in your pocket?")

# ฟังก์ชันเพิ่มช้อยส์ 

def post_choice( question_id , choice ):

    cursor.execute("INSERT INTO choices (question_id , choice_text) VALUES (? , ?)" , (question_id, choice,))
    conn.commit()
    

# post_choice(4 , "15 baht")
# post_choice(4 , "1000 baht")
# post_choice(4 , "0 baht")

# ฟังก์ชันขอคำถาม

def get_questions():
    
    questions_list = []

    cursor.execute('SELECT * FROM questions')
    rows = cursor.fetchall()
    
    for i in range(len(rows)) :
        
        questions_list.append({"id" : rows[i][0], "question" : rows[i][1] })
        
        
    return questions_list

# ฟังก์ชันลบคำถาม

def delete_questions(id):
    
    cursor.execute('DELETE FROM questions WHERE id = ?' , (id,))
    conn.commit()
    

# ฟังก์ชันขอช้อยส์
def get_choice() :

    choice_list = []

    cursor.execute('SELECT * FROM choices')
    rows = cursor.fetchall()
    
    for i in range(len(rows)) :
        
        choice_list.append({"id" : rows[i][0] ,"question_id" : rows[i][1], "choice" : rows[i][2] })
        
        
    return choice_list

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

for i in range(len(q)):

    print(f"<br> <h3> Question {i+1} : {q[i]['question']}</h3>")

    print("<form action='/cgi-bin/result.py' method='GET'>")  

    for j in range(len(c)) :
     
        if (q[i]['id'] == c[j]['question_id']):

    
            print(f"""
            
                <input type="radio" id="choice_{c[j]['id']}" name="selected_choice" value="{c[j]['id']}">
                <label for="choice_{c[j]['id']}">{c[j]['choice']}</label><br>
        
            """)
        
    print("<br><input type='submit' value='submit'>")
    print("</form>")  

print("</body>")
print("</html>")

conn.close()
