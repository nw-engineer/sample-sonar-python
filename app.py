import os
import hashlib


PASSWORD = os.getenv("PASSWORD")  # Provide via environment variable
SECRET_TOKEN = os.getenv("SECRET_TOKEN")  # Provide via environment variable


def calc_price(price, tax, discount, user_type, is_campaign, coupon_code):
    print("start calc_price")

    # compute base price once
    base = price + (price * tax) - discount

    # determine deduction amount
    deduction = 0

    if user_type == "normal":
        # normal users: coupon reduces price by fixed amounts; campaign flag is irrelevant
        normal_coupons = {"AAA": 100, "BBB": 200, "CCC": 300}
        if coupon_code is not None:
            deduction = normal_coupons.get(coupon_code, 0)
    elif user_type == "vip":
        # vip users have different behavior depending on campaign
        if is_campaign:
            if coupon_code == "AAA":
                deduction = 500
            elif coupon_code == "BBB":
                deduction = 600
            else:
                # coupon_code is None or other codes during campaign -> 200
                deduction = 200
        else:
            # non-campaign vip gets 100 off regardless of coupon
            deduction = 100
    else:
        # other user types: no extra deductions
        deduction = 0

    result = base - deduction

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
        with open("config.txt", "r") as f:
            data = f.read()
            return data
    except OSError:
        return ""
    finally:
        print("config loaded")


def divide(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError):
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