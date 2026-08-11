from database.database import SessionLocal
from models.user import User
from models.file import File
from utils.security import hash_password


db = SessionLocal()


users_data = [
    {
        "email": "securitytest@gmail.com",
        "password": "mypassword123",
        "files": [
            ("resume.pdf", "/uploads/resume.pdf"),
            ("project.pdf", "/uploads/project.pdf")
        ]
    },
    {
        "email": "user2@example.com",
        "password": "Test@12345",
        "files": [
            ("notes.pdf", "/uploads/notes.pdf"),
            ("assignment.pdf", "/uploads/assignment.pdf")
        ]
    },
    {
        "email": "user3@example.com",
        "password": "Test@12345",
        "files": [
            ("certificate.pdf", "/uploads/certificate.pdf"),
            ("project.zip", "/uploads/project.zip")
        ]
    }
]


for user_data in users_data:

    user = db.query(User).filter(
        User.email == user_data["email"]
    ).first()

    if not user:
        user = User(
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"])
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Created user: {user.email}")

    else:
        print(f"User already exists: {user.email}")

    for filename, filepath in user_data["files"]:

        existing_file = db.query(File).filter(
            File.filename == filename,
            File.user_id == user.id
        ).first()

        if not existing_file:
            new_file = File(
                filename=filename,
                filepath=filepath,
                user_id=user.id
            )

            db.add(new_file)

            print(
                f"Created file: {filename} for {user.email}"
            )

db.commit()
db.close()

print("Seed completed successfully!")