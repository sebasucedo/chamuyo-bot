import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
import boto3
from moto import mock_aws
from utils.DynamodbClient import DynamodbClient

@mock_aws
def test_get_all_items():
  boto3_dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table = boto3_dynamodb.create_table(
    TableName="ChamuyoBot",
    KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
    ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
  )
  table.put_item(Item={'id': '1','name': 'Emilia', 'data': 'direct'})
  table.put_item(Item={'id': '2','name': 'Micaela', 'data': 'direct'})

  dynamodb_client = DynamodbClient(table)
  
  items = dynamodb_client.get_all_items()


  assert items == [{'id': '1','name': 'Emilia', 'data': 'direct'}, {'id': '2','name': 'Micaela', 'data': 'direct'}]

  response = table.scan()
  assert 'LastEvaluatedKey' not in response