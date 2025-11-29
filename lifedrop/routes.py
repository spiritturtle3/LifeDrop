from flask import Blueprint, render_template
from .forms import DonorLoginForm, DonorRegisterForm, BloodRequestForm

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

@main_bp.route("/home/dlogin", methods=["GET", "POST"])
def dlogin():
    login_form = DonorLoginForm()
    register_form = DonorRegisterForm()
    
    # Handle login submit
    if login_form.submit_login.data and login_form.validate_on_submit():
        # add authentication logic here
        print("Login:", login_form.email.data, login_form.password.data)
        return render_template("donor-dash.html")

    # Handle register submit
    if register_form.submit_register.data and register_form.validate_on_submit():
        print("Register:", 
              register_form.first_name.data,
              register_form.last_name.data,
              register_form.email.data,
              register_form.phone.data,
              register_form.blood_type.data,
              register_form.age.data,
              register_form.city.data)
        return render_template("donor-dash.html")

    return render_template(
        'donor-login.html',
        login_form=login_form,
        register_form=register_form
    )


@main_bp.route("/home/dlogin/dondb")
def dondb():
    return render_template('donor-dash.html')

@main_bp.route("/home/hosplog")
def hosplog():
    return render_template('hospital-login.html')

@main_bp.route("/home/hosplog/hosdb")
def hosdb():
    return render_template('hospitaldb.html')

@main_bp.route("/blood-request", methods=["GET", "POST"])
def blood_request():
    form = BloodRequestForm()

    if form.validate_on_submit():
        print("=== BLOOD REQUEST RECEIVED ===")
        print("Patient Name:", form.patient_name.data)
        print("Blood Type:", form.blood_type.data)
        print("Units Needed:", form.units.data)
        print("Urgency Level:", form.urgency.data)
        print("Hospital:", form.hospital.data)
        print("City:", form.city.data)
        print("State:", form.state.data)
        print("Contact Name:", form.contact_name.data)
        print("Contact Phone:", form.contact_phone.data)
        print("Contact Email:", form.contact_email.data)
        print("Additional Details:", form.details.data)
        print("================================")

        flash("Blood request submitted successfully!", "success")
        return redirect(url_for("main.blood_request_success"))

    return render_template("request.html", request_form=form)


@main_bp.route("/home/request/reqdb")
def reqdb():
    return render_template('reqdb.html')

