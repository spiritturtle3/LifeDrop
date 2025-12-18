from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User, DonorProfile, BloodRequest

from .forms import (
    DonorLoginForm,
    DonorRegisterForm,
    RequesterLoginForm,
    BloodRequestForm
)

main_bp = Blueprint("main", __name__)

# ==================== STATIC PAGES ====================

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


# ==================== HOSPITAL (DUMMY FOR NAV) ====================

@main_bp.route("/home/hosplog")
def hosplog():
    return render_template("hospital-login.html")

@main_bp.route("/home/hosplog/hosdb")
def hosdb():
    return render_template("hospitaldb.html")


# ==================== DONOR LOGIN / REGISTER ====================

@main_bp.route("/home/dlogin", methods=["GET", "POST"])
def dlogin():
    login_form = DonorLoginForm()
    register_form = DonorRegisterForm()

    # ----- LOGIN -----
    if login_form.submit_login.data and login_form.validate_on_submit():
        user = User.query.filter_by(
            email=login_form.email.data,
            role="donor"
        ).first()

        if not user or not check_password_hash(
            user.password_hash,
            login_form.password.data
        ):
            flash("Invalid email or password", "danger")
            return redirect(url_for("main.dlogin"))

        session.clear()
        session["user_id"] = user.id
        session["role"] = "donor"
        return redirect(url_for("main.dondb"))

    # ----- REGISTER -----
    if register_form.submit_register.data and register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data).first():
            flash("Email already registered", "danger")
            return redirect(url_for("main.dlogin"))

        user = User(
            email=register_form.email.data,
            password_hash=generate_password_hash(register_form.password.data),
            role="donor"
        )
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

        session.clear()
        session["user_id"] = user.id
        session["role"] = "donor"
        return redirect(url_for("main.dondb"))

    return render_template(
        "donor-login.html",
        login_form=login_form,
        register_form=register_form
    )


@main_bp.route("/home/dlogin/dondb")
def dondb():
    if session.get("role") != "donor":
        flash("Unauthorized access", "danger")
        return redirect(url_for("main.home"))
    return render_template("donor-dash.html")


# ==================== REQUESTER LOGIN + REQUEST (SINGLE PAGE) ====================

@main_bp.route("/blood-request", methods=["GET", "POST"])
def blood_request():
    login_form = RequesterLoginForm()
    register_form = BloodRequestForm()

    # ---------- LOGIN ----------
    if login_form.submit_login.data and login_form.validate_on_submit():
        user = User.query.filter_by(
            email=login_form.email.data,
            role="requester"
        ).first()

        if not user or not check_password_hash(
            user.password_hash,
            login_form.password.data
        ):
            flash("Invalid email or password", "danger")
            return redirect(url_for("main.blood_request"))

        session.clear()
        session["user_id"] = user.id
        session["role"] = "requester"
        return redirect(url_for("main.reqdb"))

    # ---------- REGISTER + CREATE REQUEST ----------
    if register_form.submit.data and register_form.validate_on_submit():

        user = User.query.filter_by(
            email=register_form.contact_email.data,
            role="requester"
        ).first()

        if not user:
            user = User(
                email=register_form.contact_email.data,
                password_hash=generate_password_hash("temporary"),
                role="requester"
            )
            db.session.add(user)
            db.session.commit()

        session.clear()
        session["user_id"] = user.id
        session["role"] = "requester"

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
        return redirect(url_for("main.view_matches", request_id=req.id))

    return render_template(
        "request.html",
        login_form=login_form,
        register_form=register_form
    )


# ==================== MATCHING ====================

@main_bp.route("/matches/<int:request_id>")
def view_matches(request_id):
    blood_request = BloodRequest.query.get_or_404(request_id)

    donors = DonorProfile.query.filter_by(
        blood_type=blood_request.blood_type,
        city=blood_request.city,
        is_available=True
    ).all()

    return render_template(
        "reqdb.html",
        request=blood_request,
        donors=donors
    )


# ==================== REQUESTER DASHBOARD ====================

@main_bp.route("/home/request/reqdb")
def reqdb():
    if session.get("role") != "requester":
        flash("Unauthorized access", "danger")
        return redirect(url_for("main.home"))

    requests = BloodRequest.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        BloodRequest.created_at.desc()
    ).all()

    return render_template("reqdb.html", requests=requests)
