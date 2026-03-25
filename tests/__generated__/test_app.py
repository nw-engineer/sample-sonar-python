def test_check_number_single_digits():
    from app import check_number
    expected = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    for n, word in expected.items():
        assert check_number(n) == word

def test_check_number_other_cases():
    from app import check_number
    for n in (0, 10, -1, None):
        assert check_number(n) == "other"

def test_penalty_normal_no_coupon_returns_zero():
    from app import _penalty_for
    assert _penalty_for("normal", is_campaign=True, coupon_code=None) == 0

def test_penalty_normal_known_and_unknown_coupons():
    from app import _penalty_for
    assert _penalty_for("normal", is_campaign=False, coupon_code="AAA") == 100
    assert _penalty_for("normal", is_campaign=False, coupon_code="BBB") == 200
    assert _penalty_for("normal", is_campaign=False, coupon_code="CCC") == 300
    assert _penalty_for("normal", is_campaign=False, coupon_code="DDD") == 0

def test_penalty_vip_campaign_no_coupon_returns_200():
    from app import _penalty_for
    assert _penalty_for("vip", is_campaign=True, coupon_code=None) == 200

def test_penalty_vip_campaign_known_and_unknown_coupons():
    from app import _penalty_for
    assert _penalty_for("vip", is_campaign=True, coupon_code="AAA") == 500
    assert _penalty_for("vip", is_campaign=True, coupon_code="BBB") == 600
    assert _penalty_for("vip", is_campaign=True, coupon_code="CCC") == 200
    assert _penalty_for("vip", is_campaign=True, coupon_code="UNKNOWN") == 200

def test_penalty_vip_not_campaign_returns_100():
    from app import _penalty_for
    assert _penalty_for("vip", is_campaign=False, coupon_code=None) == 100

def test_penalty_unknown_user_type_returns_0():
    from app import _penalty_for
    assert _penalty_for("other", is_campaign=False, coupon_code="AAA") == 0

def test_read_config_success(monkeypatch, capsys):
    class DummyFile:
        def __init__(self, content):
            self._content = content
        def read(self):
            return self._content
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False
    def fake_open(path, mode="r", *args, **kwargs):
        assert path == "config.txt"
        assert "r" in mode
        return DummyFile("config-data")
    monkeypatch.setattr("builtins.open", fake_open)
    from app import read_config
    result = read_config()
    captured = capsys.readouterr()
    assert result == "config-data"
    assert captured.out == "config loaded\n"

def test_read_config_file_not_found_returns_empty_and_logs(monkeypatch, capsys):
    def fake_open(path, mode="r", *args, **kwargs):
        raise FileNotFoundError
    monkeypatch.setattr("builtins.open", fake_open)
    from app import read_config
    result = read_config()
    captured = capsys.readouterr()
    assert result == ""
    assert captured.out == "config loaded\n"

def test_read_config_oserror_returns_empty_and_logs(monkeypatch, capsys):
    def fake_open(path, mode="r", *args, **kwargs):
        raise OSError
    monkeypatch.setattr("builtins.open", fake_open)
    from app import read_config
    result = read_config()
    captured = capsys.readouterr()
    assert result == ""
    assert captured.out == "config loaded\n"

def test_calc_price_no_penalty_returns_base():
    from app import calc_price
    # normal user during campaign with no coupon -> penalty 0
    price = 100
    tax = 0.1
    discount = 10
    result = calc_price(price, tax, discount, user_type="normal", is_campaign=True, coupon_code=None)
    assert result == 100  # 100 + 10 - 10

def test_calc_price_applies_penalty_for_normal_coupon():
    from app import calc_price
    # normal user not in campaign with coupon "BBB" -> penalty 200
    price = 300
    tax = 0.0
    discount = 0
    result = calc_price(price, tax, discount, user_type="normal", is_campaign=False, coupon_code="BBB")
    assert result == 100  # 300 - 200

def test_calc_price_negative_result_clamped_to_zero():
    from app import calc_price
    # vip campaign with coupon "AAA" -> penalty 500, base less than penalty -> result 0
    price = 100
    tax = 0.0
    discount = 0
    result = calc_price(price, tax, discount, user_type="vip", is_campaign=True, coupon_code="AAA")
    assert result == 0

def test_calc_price_handles_fractional_tax():
    from app import calc_price
    # fractional tax and discount with no penalty
    price = 100
    tax = 0.05
    discount = 2
    result = calc_price(price, tax, discount, user_type="normal", is_campaign=True, coupon_code=None)
    assert result == 103.0  # 100 + 5 - 2
