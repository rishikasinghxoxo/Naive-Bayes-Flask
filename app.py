
app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_person():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT
        )
    """)

    cur.execute(
        "INSERT INTO people (name, age, gender) VALUES (%s, %s, %s)",
        (name, age, gender)
    )

    conn.commit()
    cur.close()
    conn.close()

    return "Person added successfully!"

@app.route("/search", methods=["POST"])
def search():
    name = request.form["name"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name, age, gender FROM people WHERE name=%s", (name,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("result.html", person=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
