from flask import Flask, render_template, request, redirect, url_for, session
import string
import sqlite3

app = Flask(__name__)
app.secret_key = '123'

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
        src = request.form.get('source').lower().strip()
        dst = request.form.get('destination').lower().strip()
        
        conn = get_db_connection()
        conn.execute('UPDATE users set src = ? , dst = ? , ride_completed = 1 where username =?',  ( src, dst,session['username'] ) )
        conn.commit()
        conn.close()
    return render_template('select_ride_route.html')


        
@app.route('/request_ride',methods=('GET','POST'))
def request_ride():
    output=""
    output2=""
    output3=""
    if request.method=='POST':
        src = request.form.get('source').lower().strip()
        dst = request.form.get('destination').lower().strip()
        # alpha=list(string.ascii_uppercase)
        place=['raidurg','hitech city','durgam Cheruvu','madhapur','peddamma gudi','jubilee hills CheckPost','road no 5 jubilee hills','yusufguda',
               'madhura nagar','ameerpet','begumpet','prakash nagar','rasoolpura','paradise','parade ground','secunderabad east'
               ,'mettuguda','tarnaka','habsiguda','ngri','stadium','uppal','nagole']
        
        d={}
        for i in range(23):
            d[place[i]] = i
        conn = get_db_connection()
        res=conn.execute('SELECT username,src,dst,ride_completed FROM users ').fetchall()
        for row in res:
            source=row['src']
            current=row['username']
            destination=row['dst']
            status = row['ride_completed']
            if status == 1:
                if (source is not None and destination is not None):# and ((d[source] <= d[src] and d[destination] >= d[dst]) or (d[source] >= d[src] and d[destination] <= d[dst]) or (d[source] == src and d[destination] == dst) ):
                    if d[source]<=d[src]<=d[destination]+1 and d[source]<=d[dst]<=d[destination]+1:
                        output='RIDE MATCHED '
                        output2 = ' Your Ride Mate is ' + current
                        output3 = source.upper() +' --> '+ destination.upper()
                        break
            else:
                output='RIDE NOT MATCHED , TRY AGAIN LATER'
        conn.close()
        
    return render_template('request_ride_route.html',output=output,output2=output2,output3=output3)





if __name__ == '__main__':
    app.run(debug=True)