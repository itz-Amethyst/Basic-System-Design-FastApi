import random
import string


def find_post(id , source):
    for p in source:
        if p['id'] == id:
            return p

def find_index_post(id, source):
    for i,p in enumerate(source):
        if p['id'] == id:
            return i


def generate_generic_id():
    letters = string.ascii_letters
    numbers = string.digits
    random_chars = random.choices(letters + numbers , k = 12)
    random_string = ''.join(random_chars)
    return f"XOM-{random_string}"