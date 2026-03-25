def test_check_number_values():
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
        0: "other",
        10: "other",
        -1: "other",
        "1": "other",
        None: "other",
    }
    for inp, out in expected.items():
        assert check_number(inp) == out

def test_normal_user_with_known_coupon_AAA():
    from app import calc_price
    result = calc_price(price=1000, tax=0.1, discount=0, user_type="normal", is_campaign=False, coupon_code="AAA")
    assert result == 1000  # base 1100 - 100

def test_normal_user_no_coupon_and_unknown_coupon():
    from app import calc_price
    # no coupon
    result_none = calc_price(price=100, tax=0.0, discount=10, user_type="normal", is_campaign=False, coupon_code=None)
    assert result_none == 90  # base 100 - 0
    # unknown coupon code
    result_unknown = calc_price(price=100, tax=0.0, discount=10, user_type="normal", is_campaign=False, coupon_code="ZZZ")
    assert result_unknown == 90  # unknown coupon yields no deduction

def test_vip_user_campaign_coupon_AAA():
    from app import calc_price
    result = calc_price(price=1000, tax=0.1, discount=0, user_type="vip", is_campaign=True, coupon_code="AAA")
    assert result == 600  # base 1100 - 500

def test_vip_user_campaign_unknown_or_none_coupon_uses_200():
    from app import calc_price
    result_unknown = calc_price(price=500, tax=0.0, discount=0, user_type="vip", is_campaign=True, coupon_code="CCC")
    assert result_unknown == 300  # base 500 - 200
    result_none = calc_price(price=500, tax=0.0, discount=0, user_type="vip", is_campaign=True, coupon_code=None)
    assert result_none == 300  # None treated as "other" -> 200 deduction

def test_vip_user_non_campaign_ignores_coupon_and_gives_100():
    from app import calc_price
    result = calc_price(price=200, tax=0.0, discount=0, user_type="vip", is_campaign=False, coupon_code="AAA")
    assert result == 100  # base 200 - 100 regardless of coupon

def test_other_user_types_receive_no_extra_deduction_and_negative_results_clamped():
    from app import calc_price
    # other user type: no deduction
    result_other = calc_price(price=50, tax=0.0, discount=5, user_type="guest", is_campaign=False, coupon_code="AAA")
    assert result_other == 45  # base 45 - 0
    # negative final result clamped to zero
    result_clamped = calc_price(price=0, tax=0.0, discount=0, user_type="normal", is_campaign=False, coupon_code="AAA")
    assert result_clamped == 0  # base 0 - 100 -> clamped to 0

def test_read_config_reads_file(monkeypatch, capsys):
    import io
    from app import read_config
    def fake_open(*args, **kwargs):
        return io.StringIO("my-config")
    monkeypatch.setattr("builtins.open", fake_open)
    result = read_config()
    captured = capsys.readouterr()
    assert result == "my-config"
    assert "config loaded" in captured.out

def test_read_config_handles_oserror(monkeypatch, capsys):
    from app import read_config
    def raise_oserror(*args, **kwargs):
        raise OSError("cannot open")
    monkeypatch.setattr("builtins.open", raise_oserror)
    result = read_config()
    captured = capsys.readouterr()
    assert result == ""
    assert "config loaded" in captured.out

def test_find_user_empty_list_returns_none():
    from app import find_user
    assert find_user([], "any") is None

def test_find_user_single_match_returns_user():
    from app import find_user
    user = {"name": "alice", "id": 1}
    assert find_user([user], "alice") == user

def test_find_user_multiple_matches_returns_last():
    from app import find_user
    u1 = {"name": "alice", "id": 1}
    u2 = {"name": "bob", "id": 2}
    u3 = {"name": "alice", "id": 3}
    users = [u1, u2, u3]
    result = find_user(users, "alice")
    assert result == u3
    assert result is users[2]

def test_find_user_no_match_returns_none():
    from app import find_user
    users = [{"name": "bob"}, {"name": "carol"}]
    assert find_user(users, "alice") is None

def test_find_user_is_case_sensitive():
    from app import find_user
    users = [{"name": "Alice"}]
    assert find_user(users, "alice") is None
    assert find_user(users, "Alice") == users[0]
