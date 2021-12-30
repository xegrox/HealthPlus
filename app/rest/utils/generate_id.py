import random
import string


def generate_user_id():
    prefix_type = 'UP'
    middle_rand_num = random.randrange(0, 99999)
    suffix_rand_letter = random.choice(string.ascii_uppercase)
    return f'{prefix_type}{middle_rand_num}{suffix_rand_letter}'
