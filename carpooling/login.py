from flask import Flask, render_template, request, redirect, url_for, session
import string
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/loginhome', methods=['GET', 'POST'])
def loginhome():
    if 'username' in session:
        return render_template('loginhome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                            (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('loginhome'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/offer_ride',methods=('GET','POST'))
def offer_ride():
    if request.method=='POST':
        src = request.form.get('source')
        dst = request.form.get('destination')
        
        conn = get_db_connection()
        conn.execute('UPDATE users set src = ? , dst = ? where username =?',  ( src, dst,session['username'] ) )
        conn.commit()
        conn.close()
    return render_template('select_ride_route.html')

    
        
@app.route('/request_ride',methods=('GET','POST'))
def request_ride():
    output=""
    if request.method=='POST':
        src = request.form.get('source')
        dst = request.form.get('destination')
        alpha=list(string.ascii_uppercase)
        place=['jubilee hills','ameerpet','JNTU','GRIET']
        d={}
        for i in range(4):
            d[alpha[i]] = place[i]
        conn = get_db_connection()
        res=conn.execute('SELECT src,dst FROM users ').fetchall()
        for row in res:
            source=row['src']
            destination=row['dst']
            if source<=src and destination>=dst:
                output='RIDE MATCHED WITH '+session['username']+' FROM '+d[source]+' TO '+d[destination]
                break
        conn.close()
        
    return render_template('request_ride_route.html',output=output)
if __name__ == '__main__':
    app.run(debug=True)