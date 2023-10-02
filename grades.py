#Name: Konnor Kobelka
#Date Sep 26th 2023
#Purpose: Use a database to store student information and be able to acess it
import sqlite3,time
options= [0,1,2,3,4,5]
def create_connection(db_file):
    #create a database connection to the SQLite database
    #return: Connection object or None
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn
def create_table(conn,table, columns):
    col = ",".join(columns)
    sql = f'''CREATE TABLE IF NOT EXISTS {table}( id INTEGER PRIMARY KEY, {col});'''
    conn.execute(sql)
def insert_db(conn,table, columns,data):
    sql=f'''INSERT INTO {table} {tuple(columns)} VALUES {tuple(data)};'''
    conn.execute(sql)
    conn.commit()
def select_db(conn,table,columns_and_data=None):
    if not columns_and_data==None:
        col = " AND ".join(columns_and_data)
        sql=f'''SELECT * FROM {table} WHERE {col}'''
        return conn.execute(sql)
    else:
        sql =f"SELECT * from {table}"
        return conn.execute(sql)
def update_db(conn,table,columns_and_data,where_to_update):
    col = ",".join(columns_and_data)
    sql = f"UPDATE {table} set {col} where {where_to_update}"
    conn.execute(sql)
    conn.commit()  
def delete_db(conn,table,column,what_to_remove):
    sql=f'''DELETE FROM {table} WHERE {column} = "{what_to_remove}"'''
    conn.execute(sql)
    conn.commit()  
connection = create_connection('student_data.db')
print("Welcome To The Student Gradebook")
#display main menu
def menu():
    done = False
    while not done:
        print("Pick What You Would Like To Do")
        #try:
        time.sleep(1)
        #users choice
        choice =int(input("\nGradebook Menu:\n0: Add Student\n1: List Students\n2: Calculate Course Averages\n3: Calculate Student Averages\n4. Delete Student\n5. Exit\nEnter your choice: "))
        print("")
        #dictionary to make choices instead of 100 if statements
        menus = dict({0:add_student, 1:list_students, 2:course_average, 3:student_average, 4:delete_student, 5:update_db})
        #if statement to exit
        if choice ==6:
            print("Goodbye") 
            done = True
        elif choice in options:
            menus[choice]()
        time.sleep(1)
def student_average():
    student_name = input("Enter the student's name: ")
    student_id = input("Enter student Id: ")
    result = select_db(connection,"student_grades",[f"name='{student_name}'",f"id ={student_id}"]).fetchall()
    for i in result:
        print(f"{i[1]}'s average is {(i[2]+i[3]+i[4]+i[5])/4}%")        
def course_average():
    result = select_db(connection, "student_grades").fetchall()
    total_score = 0
    for row in result:
        total_score += sum(row[2:])
    course_average = total_score / (len(result)*4)
    print(f"The course average is: {course_average:.2f}%")
def delete_student():
    result = select_db(connection, "student_grades").fetchall()
    delete = input("Enter student Id you wish to delete: ")
    if delete not in result:
        print("Student Unavailible")
    else:
        delete_db(connection,"student_grades","id",delete)
        print("Student deleted successfully")   
def update_():
    studentid = input("Enter Student Id")
    English = float(input("Enter new grade for English: "))
    Physics = float(input("Enter new grade for Physics: "))
    Chemistry = float(input("Enter new grade for Chemistry: "))
    Math = float(input("Enter new grade for Math: "))
    update_db(connection,"student_grades",[f"English='{English}'",f"Physics='{Physics}'",f"Chemistry='{Chemistry}'",f"Math='{Math}'"],f"id={studentid}")
def list_students():
    results = select_db(connection, "student_grades").fetchall()
    for row in results:
        student_id, name, english, physics, chemistry, math = row
        time.sleep(0.5)
        print(f" ID: {student_id}\n Name: {name}\n English: {english}\n Physics: {physics}\n Chemistry: {chemistry}\n Math: {math}\n")
def add_student():
    name = input("Enter student name: ")
    English = float(input("Enter grade for English: "))
    Physics = float(input("Enter grade for Physics: "))
    Chemistry = float(input("Enter grade for Chemistry: "))
    Math = float(input("Enter grade for Math: "))
    if len(English) < 3 or len(Physics) < 3 or len(Chemistry) or len(Math) < 3 or name[1].isdigit():
        print("Invalid Input")
        
        
    insert_db(connection,"student_grades",["name","English","Physics","Chemistry","Math"],[f'{name}',f'{English}',f'{Physics}',f'{Chemistry}',f'{Math}'])
    print("Student data added successfully.")
menu()
