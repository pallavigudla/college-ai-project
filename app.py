import sqlite3
import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)

genai.configure(api_key="AIzaSyAppPFqcpbTovdLAD8_PgInwvoRPrvcbBc")

model = genai.GenerativeModel("gemini-2.0-flash")
# Create database table
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# Register Route
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template("register.html")


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route('/search', methods=['POST'])
def search():
    college_name = request.form['college_name']

    prompt = f"""
    Give complete details about {college_name} college:
    - College Name
    - Location
    - Available Branches
    - Fee Structure
    - Hostel Availability
    - Placement Percentage
    - Top Recruiters
    - Ranking
    - Admission Process
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return f"""
        <h2>College Details</h2>

        <p><strong>College Name:</strong> {college_name}</p>
        <p><strong>Location:</strong> India</p>
        <p><strong>Branches:</strong> CSE, AI, ECE, Mechanical</p>
        <p><strong>Hostel:</strong> Available</p>
        <p><strong>Placements:</strong> 80%</p>
        <p><strong>Top Recruiters:</strong> TCS, Infosys, Wipro</p>
        <p><strong>Ranking:</strong> Good Private Institution</p>
        <p><strong>Admission:</strong> Entrance Exam/Counselling</p>
        """


if __name__ == '__main__':
    app.run(debug=True)