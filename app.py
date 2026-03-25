import os
import hashlib


# Secrets should be provided via environment variables and not stored in code.
# Defaults are empty strings to keep the module importable in CI/test environments.
PASSWORD = os.getenv("PASSWORD", "")
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")


def _penalty_for(user_type, is_campaign, coupon_code):
    """Return numeric penalty to subtract from the base price.

    Behavior mirrors the original nested logic in calc_price.
    """
    if user_type == "normal":
        if coupon_code is None:
            return 0
        return {"AAA": 100, "BBB": 200, "CCC": 300}.get(coupon_code, 0)

    if user_type == "vip":
        if is_campaign:
            if coupon_code is None:
                return 200
            return {"AAA": 500, "BBB": 600}.get(coupon_code, 200)
        return 100

    return 0


def calc_price(price, tax, discount, user_type, is_campaign, coupon_code):
    print("start calc_price")

    # base price computed once
    base = price + (price * tax) - discount

    penalty = _penalty_for(user_type, is_campaign, coupon_code)
    result = base - penalty

    if result < 0:
        result = 0

    return result


def save_user(name, age):
    print("saving user...")
    user = {}
    user["name"] = name
    user["age"] = age
    user["hash"] = hashlib.md5(name.encode()).hexdigest()
    return user


def read_config():
    try:
        # use context manager to ensure file is closed; catch specific I/O errors
        with open("config.txt", "r") as f:
            data = f.read()
            return data
    except OSError:
        # Return empty string when the config file is missing or cannot be read
        return ""
    finally:
        # keep the original logging side effect
        print("config loaded")


def divide(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError):
        # Return None for division-by-zero and for invalid (non-numeric) inputs
        return None


def find_user(users, target_name):
    result = None
    for u in users:
        if u["name"] == target_name:
            result = u
    return result


def run_shell():
    cmd = "echo hello"
    os.system(cmd)


def check_number(n):
    if n == 1:
        return "one"
    elif n == 2:
        return "two"
    elif n == 3:
        return "three"
    elif n == 4:
        return "four"
    elif n == 5:
        return "five"
    elif n == 6:
        return "six"
    elif n == 7:
        return "seven"
    elif n == 8:
        return "eight"
    elif n == 9:
        return "nine"
    else:
        return "other"


def process_items(items):
    total = 0
    for i in range(0, len(items)):
        total = total + items[i]
    return total


if __name__ == "__main__":
    print(calc_price(1000, 0.1, 50, "normal", True, "AAA"))
    print(save_user("taro", 20))
    print(read_config())
    print(divide(10, 0))
    print(find_user([{"name": "taro"}, {"name": "jiro"}], "jiro"))
    run_shell()
    print(check_number(3))
    print(process_items([1, 2, 3, 4]))