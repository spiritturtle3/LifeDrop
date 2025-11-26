from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template('index.html')

@main_bp.route("/about")
def about():
    return render_template('about.html')

@main_bp.route("/contact")
def contact():
    return render_template('contact.html')

@main_bp.route("/home/dlogin")
def dlogin():
    return render_template('donor-login.html')

@main_bp.route("/home/dlogin/dondb")
def dondb():
    return render_template('donor-dash.html')

@main_bp.route("/home/hosplog")
def hosplog():
    return render_template('hospital-login.html')

@main_bp.route("/home/hosplog/hosdb")
def hosdb():
    return render_template('hospitaldb.html')

@main_bp.route("/home/request")
def request():
    return render_template('request.html')

@main_bp.route("/home/request/reqdb")
def reqdb():
    return render_template('reqdb.html')

