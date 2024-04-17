import boto3
from botocore.exceptions import ClientError

class DynamodbClient:
  def __init__(self, table):
    self.table = table

  def manage_chats(self, chats):
    self.insert_data(chats)
    all_items = self.get_all_items()
    return all_items

  def insert_data(self, chats):
    for chat in chats:
      item = {
        "Id": chat["id"],
        "Name": chat.get("name"),
        "Type": chat.get("type")
      }
      self.insert(item)

  def insert(self, item):
    try:
      self.table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(Id)"
      )
      print(f"Item inserted successfully: {item}")
    except ClientError as e:
      if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        print("Item already exists, no action taken.")
      else:
        print(f"Error inserting record: {e}")
    except Exception as e:
      print(f"Unexpected error: {e}")

  def get_all_items(self):
    try:
      response = self.table.scan()
      items = response["Items"]
      
      while "LastEvaluatedKey" in response:
        response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])
        
      return items
    except Exception as e:
      print(f"Error fetching records: {e}")
      return []
