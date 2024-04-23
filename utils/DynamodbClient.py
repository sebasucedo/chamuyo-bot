import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class DynamodbClient:
  def __init__(self, table):
    self.table = table


  def get_items_by_id(self, chat_id):
    try:
      response = self.table.get_item(
        Key={"Id": chat_id}
      )
      item = response.get("Item")
      return item
    except ClientError as e:
      print(f"Error fetching record: {e}")
      return None
    except Exception as e:
      print(f"Unexpected error: {e}")
      return None
    

  def manage_chats(self, chats):
    self.insert_data(chats)
    all_items = self.get_all_items()
    return all_items


  def insert_data(self, chats):
    for chat in chats:
      item = {
        "Id": chat["id"],
        "EventTime": chat.get("event_time"),
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


  def update_item(self, chat_id, attribute, new_value):
    try:
      response = self.table.update_item(
        Key={"Id": chat_id},
        UpdateExpression=f"SET {attribute} = :val",
        ExpressionAttributeValues={":val": new_value},
        ReturnValues="UPDATED_NEW"
      )
      print(f"Update successful: {response}")
    except ClientError as e:
      if e.response['Error']['Code']:
        print(f"Error updating record: {e.response['Error']['Message']}")
      else:
        print(f"Error updating record: {e}")
    except Exception as e:
      print(f"Unexpected error: {e}")


  def get_items_by_event_time(self, event_time):
    try:
      response = self.table.query(
        IndexName='EventTime-index',
        KeyConditionExpression=Key('EventTime').eq(event_time)
      )
      items = response['Items']
      print(f"Retrieved {len(items)} items.")
      return items
    except ClientError as e:
      print(f"Error querying items: {e}")
      return []
    except Exception as e:
      print(f"Unexpected error: {e}")
      return []
