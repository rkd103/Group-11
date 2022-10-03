import bcrypt

class Credential:
    def __init__(self, salt, hashed_password):
        self.salt = salt
        self.hashed_password = hashed_password

def generate_hash(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return (Credential(salt=salt, hashed_password=hash))
def validate_hash(salt, password, hashed_password):
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    
    if (hash == hashed_password):
        return (True)
    else:
        return (False)

# Exmaple Usage
'''
c = generate_hash(password=password)
print (validate_hash(salt=c.salt, password=password, hashed_password=c.hashed_password))
'''


