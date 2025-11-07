from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            return redirect(url_for('success', username=username))
        else:
            return "Invalid Credentials. Please try again."
    else:
        return render_template('login.html')
    
@app.route('/success/<username>')
def success(username):
    return render_template('success.html', username=username)

USERS = {"port": "port123",
         "kazman": "kazman123"
      }

if __name__ == '__main__':
    app.run(debug=True)