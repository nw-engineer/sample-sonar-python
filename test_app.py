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