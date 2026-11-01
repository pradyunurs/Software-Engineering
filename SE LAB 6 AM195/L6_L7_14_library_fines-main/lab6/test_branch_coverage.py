import pytest

from library_fines import late_fine, can_borrow, renewal_status


# Branch tests for late_fine()

def test_unknown_member_branch():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("unknown", 10, False)


def test_negative_days_branch():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_faculty_loan_period():
    assert late_fine("faculty", 30, False) == 0
    assert late_fine("faculty", 31, False) == 1


def test_non_faculty_loan_period():
    assert late_fine("student", 14, False) == 0
    assert late_fine("student", 15, False) == 2


def test_overdue_and_not_overdue():
    assert late_fine("guest", 14, False) == 0
    assert late_fine("guest", 15, False) == 5


def test_fine_below_cap():
    assert late_fine("guest", 20, False) == 30


def test_fine_above_cap():
    assert late_fine("guest", 100, False) == 200


def test_damage_true():
    assert late_fine("student", 14, True) == 150


def test_damage_false():
    assert late_fine("student", 14, False) == 0


# Branch tests for can_borrow()

def test_pending_fine_above_100():
    assert can_borrow(0, 101, "student") is False


def test_pending_fine_equal_to_100():
    assert can_borrow(0, 100, "student") is True


def test_faculty_borrow_branches():
    assert can_borrow(9, 0, "faculty") is True
    assert can_borrow(10, 0, "faculty") is False


def test_non_faculty_borrow_branches():
    assert can_borrow(2, 0, "student") is True
    assert can_borrow(3, 0, "student") is False


# Branch tests for renewal_status()

def test_reservation_true():
    assert renewal_status(0, True, 5) == "denied"


def test_reservation_false():
    assert renewal_status(0, False, 5) == "renewed"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_below_limit():
    assert renewal_status(1, False, 5) == "renewed"


def test_days_left_negative():
    assert renewal_status(0, False, -1) == "overdue"


def test_days_left_zero():
    assert renewal_status(0, False, 0) == "renewed"