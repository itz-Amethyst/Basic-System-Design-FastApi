import random
import string
from datetime import datetime
from typing import List

from app.shared import settings


def find_post( id , source ):
    for p in source:
        if p['id'] == id:
            return p


def find_index_post( id , source ):
    for i , p in enumerate(source):
        if p['id'] == id:
            return i


def generate_generic_id():
    letters = string.ascii_letters
    numbers = string.digits
    random_chars = random.choices(letters + numbers , k = 12)
    random_string = ''.join(random_chars)
    return f"XOM-{random_string}"


def space_to_underscore( input_string ):
    return input_string.replace(" " , "_")

def generate_random_code() -> str:
    return ''.join(random.choices('0123456789' , k = settings.VERIFICATION_CODE_LEN))

def check_is_numeric( text: str ) -> bool:

    if text.isnumeric():
        return True
    return False

def reverse_string( text: str ) -> str:
    return text[::-1]

def capitalize_names( names: List[str] ) -> List[str]:
    """Capitalizes the first letter of each name in a list."""
    return [name.capitalize() for name in names]

def convert_to_utc( as_datetime: bool = False ) -> int | datetime:
    now = datetime.utcnow()

    if as_datetime:
        return now

    return int(now.timestamp())
