from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


# Home page - Show all students
@app.route("/")
def home():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", students=students)


# Add Student
@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        register_no = request.form["register_no"]
        department = request.form["department"]
        year = request.form["year"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students
            (name, register_no, department, year)
            VALUES (%s, %s, %s, %s)
            """,
            (name, register_no, department, year)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")

    return render_template("add_student.html")


# Mark Attendance
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        student_id = request.form["student_id"]
        date = request.form["date"]
        status = request.form["status"]

        cursor.execute(
            """
            INSERT INTO attendance
            (student_id, date, status)
            VALUES (%s, %s, %s)
            """,
            (student_id, date, status)
        )

        connection.commit()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "attendance.html",
        students=students
    )


# View Attendance
@app.route("/view_attendance")
def view_attendance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "view_attendance.html",
        attendance=attendance
    )


# Attendance Percentage
@app.route("/attendance_percentage")
def attendance_percentage():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            student_id,
            COUNT(*) AS total_classes,
            SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present,
            SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS absent,
            ROUND(
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END)
                * 100.0 / COUNT(*),
                2
            ) AS percentage
        FROM attendance
        GROUP BY student_id
        """
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "attendance_percentage.html",
        results=results
    )


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)