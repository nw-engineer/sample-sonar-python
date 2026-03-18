from app import calc_price, divide, find_user, process_items, check_number


def test_calc_price_normal():
    result = calc_price(1000, 0.1, 50, "normal", True, "AAA")
    assert result == 950.0


def test_divide_success():
    assert divide(10, 2) == 5


def test_divide_zero():
    assert divide(10, 0) is None


def test_find_user():
    users = [{"name": "taro"}, {"name": "jiro"}]
    result = find_user(users, "jiro")
    assert result == {"name": "jiro"}


def test_process_items():
    assert process_items([1, 2, 3]) == 6


def test_check_number():
    assert check_number(3) == "three"

def test_check_number_one():
    assert check_number(1) == "one"

def test_check_number_two():
    assert check_number(2) == "two"

def test_check_number_four():
    assert check_number(4) == "four"

def test_check_number_five():
    assert check_number(5) == "five"

def test_check_number_six():
    assert check_number(6) == "six"

def test_check_number_seven():
    assert check_number(7) == "seven"

def test_check_number_eight():
    assert check_number(8) == "eight"

def test_check_number_nine():
    assert check_number(9) == "nine"

def test_check_number_other():
    assert check_number(0) == "other"
    assert check_number(10) == "other"
