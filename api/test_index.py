from index import *
import pytest

def test_text_to_number():
    # Basic single digits
    assert text_to_number("one") == 1
    assert text_to_number("two") == 2
    assert text_to_number("three") == 3
    assert text_to_number("four") == 4
    assert text_to_number("five") == 5
    assert text_to_number("six") == 6
    assert text_to_number("seven") == 7
    assert text_to_number("eight") == 8
    assert text_to_number("nine") == 9
    assert text_to_number("ten") == 10
    
    # Zero and nil
    assert text_to_number("zero") == 0
    assert text_to_number("nil") == 0
    
    # Case insensitive
    assert text_to_number("ONE") == 1
    assert text_to_number("Two") == 2
    assert text_to_number("ZERO") == 0
    
    # Special characters (function strips them)
    assert text_to_number("one!") == 1
    assert text_to_number("two-") == 2
    assert text_to_number("three ") == 3
    
    # Complex text numbers
    assert text_to_number("eleven") == 11
    assert text_to_number("twelve") == 12
    assert text_to_number("thirteen") == 13
    assert text_to_number("fourteen") == 14
    assert text_to_number("fifteen") == 15
    assert text_to_number("sixteen") == 16
    assert text_to_number("seventeen") == 17
    assert text_to_number("eighteen") == 18
    assert text_to_number("nineteen") == 19
    assert text_to_number("twenty") == 20
    assert text_to_number("twenty one") == 21
    assert text_to_number("twenty two") == 22
    assert text_to_number("thirty") == 30
    assert text_to_number("forty") == 40
    assert text_to_number("fifty") == 50
    assert text_to_number("sixty") == 60
    assert text_to_number("seventy") == 70
    assert text_to_number("eighty") == 80
    assert text_to_number("ninety") == 90
    assert text_to_number("one hundred") == 100
    assert text_to_number("one hundred and one") == 101
    assert text_to_number("one hundred and twenty three") == 123
    assert text_to_number("two hundred") == 200
    assert text_to_number("three hundred and forty five") == 345
    assert text_to_number("one thousand") == 1000
    assert text_to_number("one thousand and one") == 1001
    assert text_to_number("two thousand and fifty six") == 2056
    
    # Invalid inputs (should raise ValueError)
    with pytest.raises(ValueError):
        text_to_number("abc")
    with pytest.raises(ValueError):
        text_to_number("")
    with pytest.raises(ValueError):
        text_to_number("123")
    with pytest.raises(ValueError):
        text_to_number("not a number")

def test_number_to_text():
    assert number_to_text(0) == "zero"
    assert number_to_text(1) == "one"
    assert number_to_text(5) == "five"
    assert number_to_text(10) == "ten"
    assert number_to_text(100) == "one hundred"
    assert number_to_text(1000) == "one thousand"
    
    # Edge cases
    with pytest.raises(ValueError):
        number_to_text(-1)
    with pytest.raises(ValueError):
        number_to_text("not_a_number")

def test_base64_to_number():
    # Test with actual base64 values that the function produces
    assert base64_to_number(number_to_base64(0)) == 0
    assert base64_to_number(number_to_base64(1)) == 1
    assert base64_to_number(number_to_base64(5)) == 5
    assert base64_to_number(number_to_base64(10)) == 10
    
    # Invalid base64
    with pytest.raises(ValueError):
        base64_to_number("invalid")
    with pytest.raises(ValueError):
        base64_to_number("")
    with pytest.raises(ValueError):
        base64_to_number("M@==")

def test_number_to_base64():
    # Test that the function produces valid base64 that can be decoded back
    result_0 = number_to_base64(0)
    assert base64_to_number(result_0) == 0
    
    result_1 = number_to_base64(1)
    assert base64_to_number(result_1) == 1
    
    result_5 = number_to_base64(5)
    assert base64_to_number(result_5) == 5
    
    result_10 = number_to_base64(10)
    assert base64_to_number(result_10) == 10
    
    result_255 = number_to_base64(255)
    assert base64_to_number(result_255) == 255
    
    # Edge cases
    with pytest.raises(ValueError):
        number_to_base64(-1)
    with pytest.raises(ValueError):
        number_to_base64("not_a_number")

def test_index_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Numeric Converter' in response.data

def test_convert_route_valid_conversions():
    with app.test_client() as client:
        # Text to decimal
        response = client.post('/convert', 
            json={'input': 'five', 'inputType': 'text', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == '5'
        assert data['error'] is None
        
        # Binary to hex
        response = client.post('/convert',
            json={'input': '1010', 'inputType': 'binary', 'outputType': 'hexadecimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 'a'
        
        # Decimal to text
        response = client.post('/convert',
            json={'input': '7', 'inputType': 'decimal', 'outputType': 'text'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 'seven'

def test_convert_route_error_handling():
    with app.test_client() as client:
        # Invalid input type
        response = client.post('/convert',
            json={'input': 'five', 'inputType': 'invalid', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'Invalid input type' in data['error']
        
        # Invalid output type
        response = client.post('/convert',
            json={'input': '5', 'inputType': 'decimal', 'outputType': 'invalid'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'Invalid output type' in data['error']
        
        # Invalid binary input
        response = client.post('/convert',
            json={'input': '102', 'inputType': 'binary', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert data['error'] is not None

def test_convert_route_all_combinations():
    with app.test_client() as client:
        # Test a few key combinations
        test_cases = [
            ('one', 'text', 'decimal', '1'),
            ('1010', 'binary', 'hexadecimal', 'a'),
            ('7', 'decimal', 'text', 'seven'),
            ('10', 'decimal', 'binary', '1010'),
            ('a', 'hexadecimal', 'decimal', '10'),
            ('12', 'octal', 'decimal', '10'),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert',
                json={'input': input_val, 'inputType': input_type, 'outputType': output_type})
            assert response.status_code == 200
            data = response.get_json()
            assert data['result'] == expected
            assert data['error'] is None

def test_edge_cases():
    # Zero handling
    assert text_to_number("zero") == 0
    assert number_to_text(0) == "zero"
    assert base64_to_number(number_to_base64(0)) == 0
    
    # Large numbers
    large_num = 1000000
    assert number_to_text(large_num) == "one million"
    assert number_to_base64(large_num) is not None
    assert base64_to_number(number_to_base64(large_num)) == large_num

def test_invalid_inputs():
    # Test various invalid inputs that should raise errors
    invalid_texts = ["abc", "", "123", "not a number", "invalid text"]
    for text in invalid_texts:
        with pytest.raises(ValueError):
            text_to_number(text)
    
    # Test invalid number types
    with pytest.raises(ValueError):
        number_to_text("not_a_number")
    
    with pytest.raises(ValueError):
        base64_to_number("invalid_base64")

def test_round_trip_conversions():
    # Test that converting A->B->A gives the same result
    original = 5
    
    # Decimal -> Text -> Decimal
    text_result = number_to_text(original)
    back_to_number = text_to_number(text_result)
    assert back_to_number == original
    
    # Decimal -> Base64 -> Decimal
    b64_result = number_to_base64(original)
    back_to_number = base64_to_number(b64_result)
    assert back_to_number == original

def test_cross_format_consistency():
    # Same number in different formats should convert to same result
    number = 10
    
    # All should convert to same decimal
    assert int("1010", 2) == number  # binary
    assert int("12", 8) == number    # octal
    assert int("a", 16) == number    # hex
    assert base64_to_number(number_to_base64(number)) == number  # base64

def test_complex_text_to_number():
    """Test complex text numbers that should work with text2digits library"""
    # Test if the text2digits library is being used properly
    # These tests will reveal if your function can handle complex text
    
    # Basic teens
    assert text_to_number("eleven") == 11
    assert text_to_number("twelve") == 12
    assert text_to_number("thirteen") == 13
    assert text_to_number("fourteen") == 14
    assert text_to_number("fifteen") == 15
    assert text_to_number("sixteen") == 16
    assert text_to_number("seventeen") == 17
    assert text_to_number("eighteen") == 18
    assert text_to_number("nineteen") == 19
    
    # Tens
    assert text_to_number("twenty") == 20
    assert text_to_number("thirty") == 30
    assert text_to_number("forty") == 40
    assert text_to_number("fifty") == 50
    assert text_to_number("sixty") == 60
    assert text_to_number("seventy") == 70
    assert text_to_number("eighty") == 80
    assert text_to_number("ninety") == 90
    
    # Compound numbers
    assert text_to_number("twenty one") == 21
    assert text_to_number("twenty two") == 22
    assert text_to_number("thirty three") == 33
    assert text_to_number("forty four") == 44
    assert text_to_number("fifty five") == 55
    assert text_to_number("sixty six") == 66
    assert text_to_number("seventy seven") == 77
    assert text_to_number("eighty eight") == 88
    assert text_to_number("ninety nine") == 99
    
    # Hundreds
    assert text_to_number("one hundred") == 100
    assert text_to_number("one hundred and one") == 101
    assert text_to_number("one hundred and twenty three") == 123
    assert text_to_number("two hundred") == 200
    assert text_to_number("three hundred and forty five") == 345
    assert text_to_number("nine hundred and ninety nine") == 999
    
    # Thousands
    assert text_to_number("one thousand") == 1000
    assert text_to_number("one thousand and one") == 1001
    assert text_to_number("two thousand and fifty six") == 2056
    assert text_to_number("ten thousand") == 10000
    
    # Edge cases with "and"
    assert text_to_number("one hundred and one") == 101
    assert text_to_number("one thousand and one") == 1001
    assert text_to_number("two thousand and fifty six") == 2056

def test_text_to_number_integration():
    """Test text-to-number conversion in the full conversion pipeline"""
    with app.test_client() as client:
        # Test complex text numbers through the API
        test_cases = [
            ("one hundred and twenty three", "text", "decimal", "123"),
            ("one thousand and one", "text", "binary", "1111101001"),
            ("two hundred", "text", "hexadecimal", "c8"),
            ("fifty five", "text", "octal", "67"),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert',
                json={'input': input_val, 'inputType': input_type, 'outputType': output_type})
            assert response.status_code == 200
            data = response.get_json()
            assert data['result'] == expected
            assert data['error'] is None
    