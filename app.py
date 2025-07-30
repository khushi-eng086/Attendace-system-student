from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('student_dashboard'))
    return render_template('login.html')

@app.route('/student_dashboard')
def student_dashboard():
    student_info = {
        'name': 'Khushi Sharma',
        'roll_number': 'STU12345',
        'phone': '9876543210',
        'total_subjects': 4,
        'total_present': 30,
        'total_absent': 5,
        'attendance': {
            'Math': '12/15',
            'Science': '8/10',
            'English': '5/6',
            'Computer': '5/6'
        }
    }
    return render_template('student_dashboard.html', username=student_info['name'], student=student_info)

if __name__ == '__main__':
    app.run(debug=True)    conn = get_db_connection()
    # --- Role-based Dashboard Logic ---
    if session['role'] == 'Faculty':
        students = conn.execute("SELECT id, username FROM users WHERE role = 'Student' ORDER BY username").fetchall()
        conn.close()
        # Pass today's date to pre-fill the date input
        return render_template('dashboard.html', students=students, today=date.today().isoformat())

    elif session['role'] == 'Student':
        attendance_records = conn.execute(
            "SELECT attendance_date, status FROM attendance WHERE student_id = ? ORDER BY attendance_date DESC",
            (session['user_id'],)
        ).fetchall()
        conn.close()
        return render_template('dashboard.html', attendance_records=attendance_records)
    
    # Fallback for any other role or issue
