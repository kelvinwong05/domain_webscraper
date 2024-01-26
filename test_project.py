from project import check_postcode, next_page, is_valid_page, parse_page
import pytest


def test_check_postcode():
    with pytest.raises(SystemExit):
        check_postcode("abcd")
    with pytest.raises(SystemExit):
        check_postcode("a123")
    with pytest.raises(SystemExit):
        check_postcode("12345")
    with pytest.raises(SystemExit):
        check_postcode("123")
    assert check_postcode("1234") == "1234"
    assert check_postcode("1235") == "1235"
    assert check_postcode("9999") == "9999"
    assert check_postcode("0000") == "0000"


def test_next_page():
    assert next_page("https://www.domain.com.au/rent/?postcode=2000&page=1", 1) == True
    assert next_page("https://www.domain.com.au/rent/?postcode=2000&page=1", 4) == True
    assert next_page("https://www.domain.com.au/rent/?postcode=2000&page=1", 5) == False
    assert (
        next_page("https://www.domain.com.au/rent/?postcode=2000&page=15", 15) == True
    )
    assert (
        next_page("https://www.domain.com.au/rent/?postcode=2000&page=25", 25) == False
    )


def test_is_valid_page():
    assert (
        is_valid_page("https://www.domain.com.au/rent/?postcode=2000&page=0") == False
    )
    assert is_valid_page("https://www.domain.com.au/rent/?postcode=2000&page=1") == True
    assert (
        is_valid_page("https://www.domain.com.au/rent/?postcode=2000&page=10") == True
    )
    assert (
        is_valid_page("https://www.domain.com.au/rent/?postcode=00000&page=1") == False
    )
    assert is_valid_page("https://www.domain.com.au/rent/?postcode=0000&page=4") == True


def test_parse_page():
    test = parse_page("https://www.domain.com.au/rent/?postcode=2069&page=1", [])
    assert len(test) > 1
    assert test[0] is not None
    assert test[0]["Price/week"] is not None
    assert test[0]["Url"] is not None
