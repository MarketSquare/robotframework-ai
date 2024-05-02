import pytest
from ai_interface.modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator

@pytest.fixture
def generator():
    # Initialize an instance of the RealTestDataGenerator class
    return RealTestDataGenerator()

def test_validate_input_valid(generator):
    # Test valid inputs
    assert generator.validate_input("address", 100, 1.0, 0.5, -1.0, -1.0) is None

def test_validate_input_invalid_type(generator):
    # Test invalid type
    with pytest.raises(ValueError) as context:
        generator.validate_input("unknown", 100, 1.0, 0.5, -1.0, -1.0)
    assert "Invalid value 'unknown' for 'type'" in str(context.value)

def test_validate_input_invalid_max_tokens(generator):
    # Test invalid max_tokens
    with pytest.raises(ValueError) as context:
        generator.validate_input("address", 5000, 1.0, 0.5, -1.0, -1.0)
    assert "Invalid value '5000' for 'max_tokens'" in str(context.value)

def test_validate_input_invalid_temperature(generator):
    # Test invalid temperature
    with pytest.raises(ValueError) as context:
        generator.validate_input("address", 100, -1.0, 0.5, -1.0, -1.0)
    assert "Invalid value '-1.0' for 'temperature'" in str(context.value)

def test_validate_input_invalid_top_p(generator):
    # Test invalid top_p
    with pytest.raises(ValueError) as context:
        generator.validate_input("address", 100, 1.0, 2.5, -1.0, -1.0)
    assert "Invalid value '2.5' for 'top_p'" in str(context.value)

def test_validate_input_invalid_frequency_penalty(generator):
    # Test invalid frequency_penalty
    with pytest.raises(ValueError) as context:
        generator.validate_input("address", 100, 1.0, 0.5, -3.0, -1.0)
    assert "Invalid value '-3.0' for 'frequency_penalty'" in str(context.value)

def test_validate_input_invalid_presence_penalty(generator):
    # Test invalid presence_penalty
    with pytest.raises(ValueError) as context:
        generator.validate_input("address", 100, 1.0, 0.5, -1.0, 3.0)
    assert "Invalid value '3.0' for 'presence_penalty'" in str(context.value)

def test_validate_input_multiple_invalid_inputs(generator):
    # Test when multiple inputs are invalid
    with pytest.raises(ValueError) as context:
        generator.validate_input("address", 5000, -1.0, 2.5, -3.0, 3.0)
    assert "Invalid value '5000' for 'max_tokens'" in str(context.value)
    assert "Invalid value '-1.0' for 'temperature'" in str(context.value)
    assert "Invalid value '2.5' for 'top_p'" in str(context.value)
    assert "Invalid value '-3.0' for 'frequency_penalty'" in str(context.value)
    assert "Invalid value '3.0' for 'presence_penalty'" in str(context.value)
