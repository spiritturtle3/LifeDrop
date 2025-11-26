from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home/dlogin')
def dlogin():
    return render_template('donor-login.html')

@app.route('/home/dlogin/dondb')
def dondb():
    return render_template('donor-dash.html')

@app.route('/home/hosplog')
def hosplog():
    return render_template('hospital-login.html')

@app.route('/home/hosplog/hosdb')
def hosdb():
    return render_template('hospitaldb.html')

@app.route('/home/request')
def request():
    return render_template('request.html')

@app.route('/home/request/rqdb')
def reqdb():
    return render_template('reqdb.html')

if __name__ == "__main__":
    app.run(debug=True)
