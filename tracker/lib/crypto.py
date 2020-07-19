from passlib.hash import pbkdf2_sha256


def hash_pass(password):
    return pbkdf2_sha256.using(rounds=200, salt_size=16).hash(password)


def verify_pass(hashed_pass, password):
    return pbkdf2_sha256.verify(hashed_pass, password)
