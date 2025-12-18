from flask import (
    Blueprint, render_template, redirect, url_for,
    session, flash, request
)
from app import db
from app.models import User, DonorProfile, BloodRequest, HospitalProfile
from werkzeug.security import generate_password_hash
from .forms import (
    DonorLoginForm, DonorRegisterForm,
    RequesterLoginForm, BloodRequestForm,
    HospitalRegisterForm, HospitalLoginForm,
    AdminLoginForm
)

main_bp = Blueprint("main", __name__)

def login_user(user):
    session.clear()
    session["user_id"] = user.id
    session["role"] = user.role

def logout_user():
    session.clear()

def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

def login_required(role=None):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login to access this page.", "warning")
                return redirect(url_for("main.home"))
            if role and session.get("role") != role:
                flash("Unauthorized access.", "danger")
                return redirect(url_for("main.home"))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

@main_bp.route("/")
def home():
    active_donors_count = DonorProfile.query.filter_by(is_available=True).count()
    lives_saved_count = 24  # You can replace this with your actual logic or DB query
    partner_hospitals_count = User.query.filter_by(role="hospital").count()

    return render_template(
        "index.html",
        active_donors_count=active_donors_count,
        lives_saved_count=lives_saved_count,
        partner_hospitals_count=partner_hospitals_count
    )

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

@main_bp.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.home"))

@main_bp.route("/home/dlogin", methods=["GET", "POST"])
def dlogin():
    login_form = DonorLoginForm()
    register_form = DonorRegisterForm()
    if login_form.submit_login.data and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data, role="donor").first()
        if not user or not user.check_password(login_form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for("main.donor_login"))
        login_user(user)
        return redirect(url_for("main.donor_dashboard"))
    if register_form.submit_register.data and register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data).first():
            flash("Email already registered", "danger")
            return redirect(url_for("main.donor_login"))
        user = User(email=register_form.email.data, role="donor")
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        donor = DonorProfile(
            user_id=user.id,
            first_name=register_form.first_name.data,
            last_name=register_form.last_name.data,
            phone=register_form.phone.data,
            blood_type=register_form.blood_type.data,
            age=register_form.age.data,
            city=register_form.city.data,
            is_available=True
        )
        db.session.add(donor)
        db.session.commit()
        login_user(user)
        return redirect(url_for("main.donor_dashboard"))
    return render_template("donor-login.html", login_form=login_form, register_form=register_form)

@main_bp.route("/home/dlogin/dondb")
@login_required(role="donor")
def donor_dashboard():
    user = current_user()
    donor = user.donor_profile

    # Dynamic counts (no fake data)
    total_donations = BloodRequest.query.filter_by(
        blood_type=donor.blood_type,
        city=donor.city,
        status="completed"
    ).count()

    lives_saved = total_donations * 3

    days_until_eligible = 0  # No donation history tracked yet

    urgent_requests = BloodRequest.query.filter_by(
        blood_type=donor.blood_type,
        city=donor.city,
        status="pending"
    ).all()

    return render_template(
        "donor-dash.html",
        donor=donor,
        total_donations=total_donations,
        lives_saved=lives_saved,
        days_until_eligible=days_until_eligible,
        urgent_requests=urgent_requests
    )


@main_bp.route("/blood-request", methods=["GET", "POST"])
def blood_request():
    login_form = RequesterLoginForm()
    register_form = BloodRequestForm()
    if login_form.submit_login.data and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data, role="requester").first()
        if not user or not user.check_password(login_form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for("main.blood_request"))
        login_user(user)
        return redirect(url_for("main.requester_dashboard"))
    if register_form.submit.data and register_form.validate_on_submit():
        user = User.query.filter_by(email=register_form.contact_email.data, role="requester").first()
        if not user:
            user = User(email=register_form.contact_email.data, role="requester")
            user.set_password("temporary")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        req = BloodRequest(
            user_id=user.id,
            patient_name=register_form.patient_name.data,
            blood_type=register_form.blood_type.data,
            units_needed=register_form.units.data,
            urgency=register_form.urgency.data,
            hospital=register_form.hospital.data,
            city=register_form.city.data,
            state=register_form.state.data,
            contact_name=register_form.contact_name.data,
            contact_phone=register_form.contact_phone.data,
            contact_email=register_form.contact_email.data,
            details=register_form.details.data,
            status="pending"
        )
        db.session.add(req)
        db.session.commit()
        flash("Blood request submitted successfully!", "success")
        return redirect(url_for("main.requester_dashboard"))
    return render_template("request.html", login_form=login_form, register_form=register_form)

@main_bp.route("/home/request/reqdb")
@login_required(role="requester")
def requester_dashboard():
    user = current_user()
    requests = BloodRequest.query.filter_by(user_id=user.id).order_by(BloodRequest.created_at.desc()).all()
    active_requests = BloodRequest.query.filter_by(user_id=user.id, status="pending").count()
    matched_donors = 0
    for req in requests:
        matched_donors += DonorProfile.query.filter_by(
            blood_type=req.blood_type,
            city=req.city,
            is_available=True
        ).count()
    return render_template("reqdb.html",
                           requests=requests,
                           donors=matched_donors,
                           active_requests=active_requests)

@main_bp.route("/home/hosplog")
def hosplog():
    return render_template("hospital-login.html")

@main_bp.route("/home/hosplog/hosdb")
@login_required(role="hospital")
def hospital_dashboard():
    user = current_user()
    hospital = user.hospital_profile
    return render_template("hospitaldb.html", hospital=hospital)

@main_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, role="admin").first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid admin credentials", "danger")
            return redirect(url_for("main.admin_login"))
        login_user(user)
        return redirect(url_for("main.admin_dashboard"))
    return render_template("admin-login.html", form=form)

@main_bp.route("/admin/dashboard")
@login_required(role="admin")
def admin_dashboard():
    total_users = User.query.count()
    total_requests = BloodRequest.query.count()
    total_donors = DonorProfile.query.count()
    return render_template("admin-dashboard.html",
                           total_users=total_users,
                           total_requests=total_requests,
                           total_donors=total_donors)

# Error Handlers for debugging

@main_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error), 500

@main_bp.app_errorhandler(Exception)
def handle_exception(e):
    if hasattr(e, 'code') and e.code != 500:
        return e
    return render_template('500.html', error=e), 500