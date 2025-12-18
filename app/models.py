from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # roles: donor | requester | hospital | admin
    role = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # one-to-one (only if role == donor)
    donor_profile = db.relationship(
        "DonorProfile",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    # one-to-many (only if role == requester)
    blood_requests = db.relationship(
        "BloodRequest",
        backref="requester",
        cascade="all, delete"
    )

    # one-to-one (only if role == hospital)
    hospital_profile = db.relationship(
        "HospitalProfile",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class DonorProfile(db.Model):
    __tablename__ = "donor_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    blood_type = db.Column(db.String(5), nullable=False, index=True)
    city = db.Column(db.String(50), nullable=False, index=True)

    age = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True, index=True)


class HospitalProfile(db.Model):
    __tablename__ = "hospital_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    hospital_name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False, index=True)
    state = db.Column(db.String(50), nullable=False, index=True)


class BloodRequest(db.Model):
    __tablename__ = "blood_requests"

    id = db.Column(db.Integer, primary_key=True)

    # requester ownership
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    patient_name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    units_needed = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.String(20), nullable=False)

    hospital = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)

    contact_name = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)

    details = db.Column(db.Text)

    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)