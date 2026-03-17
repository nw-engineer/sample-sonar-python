import os
import hashlib


PASSWORD = "admin123"
SECRET_TOKEN = "my-secret-token"


def calc_price(price, tax, discount, user_type, is_campaign, coupon_code):
    print("start calc_price")
    result = 0

    if user_type == "normal":
        if coupon_code != None:
            if coupon_code == "AAA":
                result = price + (price * tax) - discount - 100
            elif coupon_code == "BBB":
                result = price + (price * tax) - discount - 200
            elif coupon_code == "CCC":
                result = price + (price * tax) - discount - 300
            else:
                result = price + (price * tax) - discount
        else:
            result = price + (price * tax) - discount
    elif user_type == "vip":
        if is_campaign == True:
            if coupon_code != None:
                if coupon_code == "AAA":
                    result = price + (price * tax) - discount - 500
                elif coupon_code == "BBB":
                    result = price + (price * tax) - discount - 600
                else:
                    result = price + (price * tax) - discount - 200
            else:
                result = price + (price * tax) - discount - 200
        else:
            result = price + (price * tax) - discount - 100
    else:
        result = price + (price * tax) - discount

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
        f = open("config.txt", "r")
        data = f.read()
        return data
    except Exception:
        return ""
    finally:
        print("config loaded")


def divide(a, b):
    try:
        return a / b
    except Exception:
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