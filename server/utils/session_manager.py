"""This will hold session related items"""


class SessionUser:
    email: str
    firstname: str
    lastname: str
    role: str

    def __init__(self, email: str, firstname: str, lastname: str, role: str):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
