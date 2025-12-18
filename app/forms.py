from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    IntegerField,
    RadioField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Regexp
)

# ===================== DONOR FORMS =====================

class DonorLoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    submit_login = SubmitField("Login")


class DonorRegisterForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=8, max=15),
            Regexp(r'^[0-9]+$', message="Phone Number must contain digits only")
        ]
    )
    blood_type = SelectField(
        "Blood Type",
        choices=[
            ("A+", "A+"), ("A-", "A-"),
            ("B+", "B+"), ("B-", "B-"),
            ("AB+", "AB+"), ("AB-", "AB-"),
            ("O+", "O+"), ("O-", "O-")
        ],
        validators=[DataRequired()]
    )
    age = IntegerField(
        "Age",
        validators=[DataRequired(), NumberRange(min=18, max=65)]
    )
    city = StringField(
        "City",
        validators=[
            DataRequired(),
            Regexp(r'^[A-Za-z\s]+$', message="City can contain letters and spaces only")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    submit_register = SubmitField("Register as Donor")


# ===================== REQUESTER FORMS =====================

class RequesterLoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    submit_login = SubmitField("Login")


class RequesterRegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=8, max=15),
            Regexp(r'^[0-9]+$', message="Phone Number must contain digits only")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    submit_register = SubmitField("Register as Requester")


# ===================== BLOOD REQUEST FORM =====================

class BloodRequestForm(FlaskForm):
    patient_name = StringField(
        "Patient Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )

    blood_type = SelectField(
        "Blood Type Required",
        choices=[
            ("A+", "A+"), ("A-", "A-"),
            ("B+", "B+"), ("B-", "B-"),
            ("AB+", "AB+"), ("AB-", "AB-"),
            ("O+", "O+"), ("O-", "O-")
        ],
        validators=[DataRequired()]
    )

    units = IntegerField(
        "Units Needed",
        validators=[DataRequired(), NumberRange(min=1, max=10)]
    )

    urgency = RadioField(
        "Urgency Level",
        choices=[
            ('urgent', '🔴 URGENT (Within 6 hrs)'),
            ('soon', '🟡 SOON (Within 24 hrs)'),
            ('scheduled', '🟢 SCHEDULED (2–7 days)')
        ],
        validators=[DataRequired()]
    )

    hospital = StringField(
        "Hospital / Medical Facility",
        validators=[DataRequired(), Length(min=2, max=100)]
    )

    city = StringField(
        "City",
        validators=[
            DataRequired(),
            Regexp(r'^[A-Za-z\s]+$', message="City can contain letters and spaces only")
        ]
    )

    state = StringField(
        "State",
        validators=[
            DataRequired(),
            Regexp(r'^[A-Za-z\s]+$', message="State can contain letters and spaces only")
        ]
    )

    contact_name = StringField(
        "Contact Person Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )

    contact_phone = StringField(
        "Contact Phone",
        validators=[
            DataRequired(),
            Length(min=8, max=15),
            Regexp(r'^[0-9]+$', message="Phone Number must contain digits only")
        ]
    )

    contact_email = StringField(
        "Contact Email",
        validators=[DataRequired(), Email()]
    )

    details = StringField(
        "Additional Details",
        validators=[Length(max=500)]
    )

    submit = SubmitField("Submit Blood Request")

