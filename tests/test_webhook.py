import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from webhook.lambda_function import lambda_handler

def test_handler():
  test_event = {
    "body": json.dumps({
        "update_id": 10000,
        "message": {
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