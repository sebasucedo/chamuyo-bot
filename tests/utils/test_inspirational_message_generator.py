import pytest
from unittest.mock import patch, MagicMock
from utils.InspirationalMessageGenerator import InspirationalMessageGenerator

class TestInspirationalMessageGenerator:
  @patch('utils.InspirationalMessageGenerator.OpenAI')
  def test_get_message_content_success(self, mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Have a great Monday!"))])
    
    generator = InspirationalMessageGenerator()
    result = generator.get_message_content()

    assert result == "Have a great Monday!"
    mock_client.chat.completions.create.assert_called_once()


  @patch('utils.InspirationalMessageGenerator.OpenAI')
  def test_get_message_content_exception(self, mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    
    generator = InspirationalMessageGenerator()
    with pytest.raises(Exception) as exc_info:
      generator.get_message_content()
    
    assert "API Error" in str(exc_info.value)
    mock_client.chat.completions.create.assert_called_once()
