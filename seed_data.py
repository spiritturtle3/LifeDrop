from app import create_app, db
from app.models import User, DonorProfile, HospitalProfile, BloodRequest

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    print("📦 Database reset")

    # ---------------- ADMIN ----------------
    admin = User(email="admin@lifedrop.com", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)

    # ---------------- HOSPITALS ----------------
    h1_user = User(email="cityhospital@lifedrop.com", role="hospital")
    h1_user.set_password("hospital123")
    db.session.add(h1_user)
    db.session.commit()

    hospital1 = HospitalProfile(
        user_id=h1_user.id,
        hospital_name="City General Hospital",
        registration_number="HOSP1001",
        phone="9876543210",
        address="MG Road",
        city="Mumbai",
        state="Maharashtra"
    )

    h2_user = User(email="metrohospital@lifedrop.com", role="hospital")
    h2_user.set_password("hospital123")
    db.session.add(h2_user)
    db.session.commit()

    hospital2 = HospitalProfile(
        user_id=h2_user.id,
        hospital_name="Metro Medical Center",
        registration_number="HOSP2002",
        phone="9123456789",
        address="Ring Road",
        city="Delhi",
        state="Delhi"
    )

    db.session.add_all([hospital1, hospital2])

    # ---------------- DONORS ----------------
    donors = [
        ("rahul@gmail.com", "Rahul", "Sharma", "O+", "Mumbai"),
        ("anita@gmail.com", "Anita", "Verma", "A+", "Mumbai"),
        ("rohit@gmail.com", "Rohit", "Singh", "B+", "Delhi"),
        ("neha@gmail.com", "Neha", "Kapoor", "O-", "Delhi"),
    ]

    for email, fname, lname, blood, city in donors:
        user = User(email=email, role="donor")
        user.set_password("donor123")
        db.session.add(user)
        db.session.commit()

        donor = DonorProfile(
            user_id=user.id,
            first_name=fname,
            last_name=lname,
            phone="9999999999",
            blood_type=blood,
            city=city,
            age=25,
            is_available=True
        )
        db.session.add(donor)

    # ---------------- REQUESTERS ----------------
    r1 = User(email="requester1@gmail.com", role="requester")
    r1.set_password("request123")
    r2 = User(email="requester2@gmail.com", role="requester")
    r2.set_password("request123")
    db.session.add_all([r1, r2])
    db.session.commit()

    # ---------------- BLOOD REQUESTS ----------------
    req1 = BloodRequest(
        user_id=r1.id,
        patient_name="Patient Alpha",
        blood_type="O+",
        units_needed=2,
        urgency="urgent",
        hospital="City General Hospital",
        city="Mumbai",
        state="Maharashtra",
        contact_name="Raj",
        contact_phone="8888888888",
        contact_email="raj@gmail.com",
        details="Emergency surgery",
        status="pending"
    )

    req2 = BloodRequest(
        user_id=r2.id,
        patient_name="Patient Beta",
        blood_type="B+",
        units_needed=1,
        urgency="soon",
        hospital="Metro Medical Center",
        city="Delhi",
        state="Delhi",
        contact_name="Amit",
        contact_phone="7777777777",
        contact_email="amit@gmail.com",
        details="Accident case",
        status="completed"
    )

    req3 = BloodRequest(
        user_id=r1.id,
        patient_name="Patient Gamma",
        blood_type="O-",
        units_needed=3,
        urgency="scheduled",
        hospital="City General Hospital",
        city="Mumbai",
        state="Maharashtra",
        contact_name="Suresh",
        contact_phone="6666666666",
        contact_email="suresh@gmail.com",
        details="Planned surgery",
        status="pending"
    )

    db.session.add_all([req1, req2, req3])

    db.session.commit()

    print("✅ Sample data inserted successfully")
