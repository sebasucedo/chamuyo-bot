import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChamuyoBot")

def manage_chats(chats):
    insert_data(chats)
    all_items = get_all_items()
    return all_items

def insert_data(chats):
    for chat in chats:
        item = {
            "Id": chat["id"],
            "Name": chat.get("name"),
            "Type": chat.get("type")
        }
        insert(item)


def insert(item):
    try:
        table.put_item(
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


def get_all_items():
    try:
        response = table.scan()
        items = response["Items"]
        
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response["Items"])
            
        return items
    except Exception as e:
        print(f"Error fetching records: {e}")
        return []

