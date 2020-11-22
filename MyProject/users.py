class Users():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        print(self.username)
