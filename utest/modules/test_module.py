import pytest
from RobotFrameworkAI.modules.Module import Module

@pytest.fixture
def module():
    # Initialize an instance of the Module class
    return Module()

def test_validate_input_arguments_given_valid_input_is_true(module):
    # Test valid inputs
    assert module.validate_input_arguments(max_tokens=100, temperature=1.0, top_p=0.5, frequency_penalty=-1.0, presence_penalty=-1.0)

def test_validate_input_arguments_given_invalid_max_tokens_raises_error(module):
    # Test invalid max_tokens
    with pytest.raises(ValueError) as context:
        module.validate_input_arguments(max_tokens=5000, temperature=1.0, top_p=0.5, frequency_penalty=-1.0, presence_penalty=-1.0)
    assert "Invalid value `5000` for `max_tokens`" in str(context.value)

def test_validate_input_arguments_given_invalid_temperature_raises_error(module):
    # Test invalid temperature
    with pytest.raises(ValueError) as context:
        module.validate_input_arguments(max_tokens=100, temperature=-1.0, top_p=0.5, frequency_penalty=-1.0, presence_penalty=-1.0)
    assert "Invalid value `-1.0` for `temperature`" in str(context.value)

def test_validate_input_arguments_given_invalid_top_p_raises_error(module):
    # Test invalid top_p
    with pytest.raises(ValueError) as context:
        module.validate_input_arguments(max_tokens=100, temperature=1.0, top_p=2.5, frequency_penalty=-1.0, presence_penalty=-1.0)
    assert "Invalid value `2.5` for `top_p`" in str(context.value)

def test_validate_input_arguments_given_invalid_frequency_penalty_raises_error(module):
    # Test invalid frequency_penalty
    with pytest.raises(ValueError) as context:
        module.validate_input_arguments(max_tokens=100, temperature=1.0, top_p=0.5, frequency_penalty=-3.0, presence_penalty=-1.0)
    assert "Invalid value `-3.0` for `frequency_penalty`" in str(context.value)

def test_validate_input_arguments_given_invalid_presence_penalty_raises_error(module):
    # Test invalid presence_penalty
    with pytest.raises(ValueError) as context:
        module.validate_input_arguments(max_tokens=100, temperature=1.0, top_p=0.5, frequency_penalty=-1.0, presence_penalty=3.0)
    assert "Invalid value `3.0` for `presence_penalty`" in str(context.value)
