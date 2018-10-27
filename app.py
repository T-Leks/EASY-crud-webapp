from flask import Flask, render_template, request, redirect, session
import pyodbc


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xeca]/'
cnxn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=dbPersonal;Trusted_Connection=yes;')
count = 0
 

@app.route("/", methods=['GET', 'POST'])
def homepage():
    global count
    if request.method == 'POST':
        session['username'] = request.form['username']
        count += 1

    cur = cnxn.cursor()
    sql = "SELECT * FROM person"
    cur.execute(sql)
    rows = cur.fetchall()
    person = []
    for row in rows:
        person.append(row)

    sql = "SELECT * FROM city"
    cur.execute(sql)
    rows = cur.fetchall()
    city = []
    for row in rows:
        city.append(row)

    sql = "SELECT p.p_id, p.p_name, p.p_surname,c.city_id, c.c_name, p.phone_number FROM person p, city c WHERE c.city_id = p.city_id"
    cur.execute(sql)
    rows = cur.fetchall()
    person_city = []
    for row in rows:
        person_city.append(row)
    return render_template('home.html', person = person, city = city, person_city = person_city)

@app.route("/create")
def insertpage():
    if count == 0:
        return redirect('/')
    elif count == 1:
        return render_template('insert.html')

@app.route("/insert_person", methods=['POST'])
def insert_person():
    if request.method == 'POST':
        p_name = request.form['name']
        p_surname = request.form['surname']
        city_id = request.form['city_id']
        phone_number = request.form['phone_number']

        cur = cnxn.cursor()
        sql = "INSERT INTO person VALUES ('"+ p_name +"', '"+ p_surname +"', "+ city_id +", '"+ phone_number +"')"
        cur.execute(sql)
        cnxn.commit()
    return redirect('/')

@app.route("/insert_city", methods=['POST'])
def insert_city():
    if request.method == 'POST':
        city_name = request.form['city_name']

        cur = cnxn.cursor()
        sql = "INSERT INTO city VALUES ('"+ city_name +"')"
        cur.execute(sql)
        cnxn.commit()
    return redirect('/')

@app.route("/change")
def updatepage():
    if count == 0:
        return redirect('/')
    elif count == 1:
        cur = cnxn.cursor()
        sql = "SELECT * FROM person"
        cur.execute(sql)
        rows = cur.fetchall()
        person = []
        for row in rows:
            person.append(row)

        sql = "SELECT * FROM city"
        cur.execute(sql)
        rows = cur.fetchall()
        city = []
        for row in rows:
            city.append(row)
        return render_template('update.html', person = person, city = city)

@app.route("/update_person", methods=['POST'])
def update_person():
    if request.method == 'POST':
        p_id = request.form['id']
        p_name = request.form['name']
        p_surname = request.form['surname']
        city_id = request.form['city_id']
        phone_number = request.form['phone_number']

        cur = cnxn.cursor()
        sql = "UPDATE person SET p_name = '"+ p_name +"', p_surname = '"+ p_surname +"', city_id = "+ city_id +", phone_number = '"+ phone_number +"' WHERE p_id = "+ p_id +""
        cur.execute(sql)
        cnxn.commit()
    return redirect('/')

@app.route("/update_city", methods=['POST'])
def update_city():
    if request.method == 'POST':
        city_id = request.form['city_id']
        city_name = request.form['city_name']

        cur = cnxn.cursor()
        sql = "UPDATE city SET  c_name = '"+ city_name +"' WHERE city_id = "+ city_id +""
        cur.execute(sql)
        cnxn.commit()
    return redirect('/')

@app.route('/destroy')
def deletepage():
    if count == 0:
        return redirect('/')
    elif count == 1:
        cur = cnxn.cursor()
        sql = "SELECT * FROM person"
        cur.execute(sql)
        rows = cur.fetchall()
        person = []
        for row in rows:
            person.append(row)

        sql = "SELECT * FROM city"
        cur.execute(sql)
        rows = cur.fetchall()
        city = []
        for row in rows:
            city.append(row)
        return render_template('delete.html', person = person, city = city)

@app.route("/delete_person", methods=['POST'])
def delete_person():
    if request.method == 'POST':
        p_id = request.form['id']

        cur = cnxn.cursor()
        sql = "DELETE FROM person WHERE p_id = "+ p_id +""
        cur.execute(sql)
        cnxn.commit()
    return redirect('/')

@app.route("/delete_city", methods=['POST'])
def delete_city():
    if request.method == 'POST':
        city_id = request.form['city_id']

        cur = cnxn.cursor()
        sql = "DELETE FROM city WHERE city_id = "+ city_id +""
        cur.execute(sql)
        cnxn.commit()
    return redirect('/')

@app.route("/login")
def loginpage():
    return render_template('login.html')

@app.route("/logout")
def logingout():
    global count

    session.pop('username', None)
    count -= 1
    return redirect('/')

 
if __name__ == "__main__":
    app.run(debug=True)