from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from datetime import datetime
import subprocess
import os
from io import BytesIO
import pandas as pd

temp_attendance_data = None
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def submit_form():
    student_id = request.form.get('student_id').upper()
    name = request.form.get('name').upper()
    year = int(request.form.get('year'))
    section = request.form.get('section').upper()

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (student_id,))
    existing_student = cursor.fetchone()
    
    if existing_student:
        conn.close()
        message = "StudentID already exists! Please use a different ID."
        # Assuming you have a mechanism to display this message, or you can log it
        print(message)
        return render_template('register.html', error=message)
    else:
        cursor.execute("INSERT INTO Students (StudentID, Name, Year, Section) VALUES (?, ?, ?, ?)", (student_id, name, year, section))
        conn.commit()
        conn.close()
        
        script_dir = os.path.dirname(__file__)
        get_faces_script = os.path.join(script_dir, 'get_faces_from_camera_tkinter.py')
        subprocess.run(["python", get_faces_script, student_id])
        
        return render_template('register.html', success="Student Registration Successful")

@app.route('/take_attendance')
def take_attendance():
    script_dir = os.path.dirname(__file__)
    take = os.path.join(script_dir, "attendance_taker.py")
    subprocess.run(["python", take])
    return render_template('index.html')

@app.route('/attendance', methods=['GET', 'POST'])
def show_attendance():
    global temp_attendance_data
    if request.method == 'POST':
        student_id = request.form.get('StudentID', '')
        start_date = request.form.get('StartDate', '')
        end_date = request.form.get('EndDate', '')

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        query = "SELECT StudentID, Date, InTime, OutTime FROM Attendance"
        conditions = []
        params = []

        if student_id:
            conditions.append("StudentID = ?")
            params.append(student_id)
        if start_date_obj and end_date_obj:
            conditions.append("Date BETWEEN ? AND ?")
            params.extend([start_date, end_date])
        elif start_date_obj:
            conditions.append("Date = ?")
            params.append(start_date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        attendance_data = cursor.fetchall()

        conn.close()

        if not attendance_data:
            return render_template('attendance.html', no_data=True, attendance_data=[], student_id=student_id, start_date=start_date, end_date=end_date)
        else :
            temp_attendance_data = attendance_data
            return render_template('attendance.html', no_data=False, attendance_data=attendance_data, student_id=student_id, start_date=start_date, end_date=end_date)
    else:
        # Initial page load or navigation to /attendance without POST
        return render_template('attendance.html', no_data=False)



@app.route('/download_excel')
def download_excel():
    global temp_attendance_data
    if temp_attendance_data is None:
        return "No data available", 404  # Or redirect to a different page

    df = pd.DataFrame(temp_attendance_data, columns=['Student ID', 'Date', 'In Time', 'Out Time'])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)

    # Clear the temporary data after generating the file
    temp_attendance_data = None

    return send_file(output,as_attachment=True,download_name='attendance.xlsx',mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/train')
def train():
    script_dir = os.path.dirname(__file__)
    take = os.path.join(script_dir, "features_extraction_to_csv.py")
    subprocess.run(["python", take])
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
