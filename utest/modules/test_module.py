import pytest
from modules.Module import Module

@pytest.fixture
def module():
    # Initialize an instance of the RealTestDataGenerator class
    return Module()

def test_validate_default_input_parameters_valid(module):
    # Test valid inputs
    assert module.validate_default_input_parameters(100, 1.0, 0.5, -1.0, -1.0) is None

def test_validate_default_input_parameters_invalid_max_tokens(module):
    # Test invalid max_tokens
    with pytest.raises(ValueError) as context:
        module.validate_default_input_parameters(5000, 1.0, 0.5, -1.0, -1.0)
    assert "Invalid value '5000' for 'max_tokens'" in str(context.value)

def test_validate_default_input_parameters_invalid_temperature(module):
    # Test invalid temperature
    with pytest.raises(ValueError) as context:
        module.validate_default_input_parameters(100, -1.0, 0.5, -1.0, -1.0)
    assert "Invalid value '-1.0' for 'temperature'" in str(context.value)

def test_validate_default_input_parameters_invalid_top_p(module):
    # Test invalid top_p
    with pytest.raises(ValueError) as context:
        module.validate_default_input_parameters(100, 1.0, 2.5, -1.0, -1.0)
    assert "Invalid value '2.5' for 'top_p'" in str(context.value)

def test_validate_default_input_parameters_invalid_frequency_penalty(module):
    # Test invalid frequency_penalty
    with pytest.raises(ValueError) as context:
        module.validate_default_input_parameters(100, 1.0, 0.5, -3.0, -1.0)
    assert "Invalid value '-3.0' for 'frequency_penalty'" in str(context.value)

def test_validate_default_input_parameters_invalid_presence_penalty(module):
    # Test invalid presence_penalty
    with pytest.raises(ValueError) as context:
        module.validate_default_input_parameters(100, 1.0, 0.5, -1.0, 3.0)
    assert "Invalid value '3.0' for 'presence_penalty'" in str(context.value)

def test_validate_default_input_parameters_multiple_invalid_inputs(module):
    # Test when multiple inputs are invalid
    with pytest.raises(ValueError) as context:
        module.validate_default_input_parameters(5000, -1.0, 2.5, -3.0, 3.0)
    assert "Invalid value '5000' for 'max_tokens'" in str(context.value)
    assert "Invalid value '-1.0' for 'temperature'" in str(context.value)
    assert "Invalid value '2.5' for 'top_p'" in str(context.value)
    assert "Invalid value '-3.0' for 'frequency_penalty'" in str(context.value)
    assert "Invalid value '3.0' for 'presence_penalty'" in str(context.value)
