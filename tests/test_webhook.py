import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from webhook.lambda_function import lambda_handler

class TestWebhook:
  def test_handler_correct_body(self):
    test_event = {
        "body": json.dumps({
            "update_id": 10000,
            "message": {
                "from": {
                    "id": 1111,
                    "is_bot": False,
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "johndoe",
                    "language_code": "en"
                },
                "chat": {
                    "id": 1111,
                    "first_name": "John",
                    "last_name": "Doe",
                    "type": "private"
                },
                "date": 1441645532,
                "text": "/settime 10:00"
            }
        })
    }

    response = lambda_handler(test_event, None)

    assert response['statusCode'] == 200


  def test_handler_empty_body(self):
    test_event = {
      "body": None
    }

    response = lambda_handler(test_event, None)

    assert response['statusCode'] == 500
