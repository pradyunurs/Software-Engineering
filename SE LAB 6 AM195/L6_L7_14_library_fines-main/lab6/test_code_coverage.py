import pytest

from library_fines import late_fine, can_borrow, renewal_status


# Tests for late_fine()

def test_student_on_time():
    assert late_fine("student", 14, False) == 0


def test_student_overdue():
    assert late_fine("student", 20, False) == 12


def test_faculty_overdue():
    assert late_fine("faculty", 35, False) == 5


def test_guest_overdue():
    assert late_fine("guest", 20, False) == 30


def test_fine_capped_at_200():
    assert late_fine("guest", 100, False) == 200


def test_damaged_book():
    assert late_fine("student", 14, True) == 150


def test_overdue_damaged_book():
    assert late_fine("student", 20, True) == 162


def test_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 10, False)


def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


# Tests for can_borrow()

def test_student_can_borrow():
    assert can_borrow(2, 0, "student") is True


def test_student_cannot_borrow_three_books():
    assert can_borrow(3, 0, "student") is False


def test_pending_fine_above_limit():
    assert can_borrow(0, 101, "student") is False


def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True


def test_faculty_cannot_borrow_ten_books():
    assert can_borrow(10, 0, "faculty") is False


def test_guest_can_borrow():
    assert can_borrow(2, 0, "guest") is True


# Tests for renewal_status()

def test_renewal_denied():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"


def test_renewal_successful():
    assert renewal_status(0, False, 5) == "renewed"