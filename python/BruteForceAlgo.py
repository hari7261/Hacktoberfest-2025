import itertools

def brute_force(password_length, charset):
    for attempt in itertools.product(charset, repeat=password_length):
        password = ''.join(attempt)
        # Check if password matches
        # print(attempt)
        if password == target_password:
            return password

target_password = "secret"
password_length = 6
charset = "abcdefghijklmnopqrstuvwxyz"

result = brute_force(password_length, charset)
print("Password found:", result)
