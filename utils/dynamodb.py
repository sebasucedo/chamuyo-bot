import boto3

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
        try:
            table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(Id)"
            )
        except Exception as e:
            print(f"Error inserting record: {e}")

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

