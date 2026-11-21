import json
class Database:
    def insert(name, email, password):
        with open("user.json", "r") as f:
            users = json.load(f)

            if email in users:
                return 0
            else:
                users[email] = [password]
        with open("user.json", "w") as f:
            json.dump(users, f, indent=4)
            return 1
    def check_login(email,password):
        with open("user.json","r")as f:
            users=json.load(f)
            if email in users:
                if users[email][0] == password:
                    return 1
                else:
                    return 0
            else:
                return 0