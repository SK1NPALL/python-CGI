import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# สร้างตาราง

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
    conn.close()
    
# post_questions("What single do you like?")
# post_questions("How many money in your pocket?")

# ฟังก์ชันแสดงคำถาม

def get_questions():
    
    questions_list = []

    cursor.execute('SELECT * FROM questions')
    rows = cursor.fetchall()
    
    for i in range(len(rows)) :
        
        questions_list.append({"id" : rows[i][0], "question" : rows[i][1] })
        
        
    return questions_list

q = get_questions()

# ฟังก์ชันลบคำถาม
def delete_questions(id):
    
    cursor.execute('DELETE FROM questions WHERE id = ?' , (id,))
    conn.commit()
    conn.close()
    
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
print("    <h1>List of users</h1>")
print(f"    <h2>{q[0]['question']}</h2>")
print("</body>")
print("</html>")
