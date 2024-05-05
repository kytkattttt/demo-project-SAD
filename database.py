import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://final-face-recog-attendance-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    "422000351":
        {
            "name": "Gorospe, Bea D.",
            "Program": "BSIT",
            "block&year": "2.1  2nd year",
            "recent_attendance": "2024 5 5 04:16:04"

        },
    "422000547":
        {
            "name": "Victorino, Chandler",
            "Program": "BSIT",
            "block&year": "2.1  2nd year",
            "recent_attendance": "2024 5 5 04:16:04"

        },
    "422002924":
        {
            "name": "Villalino, Clarens",
            "Program": "BSIT",
            "block&year": "2.1 2nd year",
            "recent_attendance": "2024 5 5 04:16:04"

        }


}
for key, value in data.items():
    ref.child(key).set(value)