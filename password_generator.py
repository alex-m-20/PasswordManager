import secrets
import string

# Generates random passwords
def generate_password(length=16):
    # The pool of characters we're allowed to pick from which include letters, digits, and some punctuation.
    characters = string.ascii_letters + string.digits + string.punctuation

    # Picks one random character from that pool, "length" number of times(length=16) 
    # and joins them all into a single string.
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password