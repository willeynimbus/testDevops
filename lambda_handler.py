import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Emp_Master')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    resource_path = event['resource']

    if http_method == 'POST' and resource_path == '/employee':
        return insert_employee(event)
    elif http_method == 'GET' and resource_path == '/employee':
        return get_employee(event)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Resource not found')
        }

def insert_employee(event):
    try:
        item = json.loads(event['body'])
        if all(key in item for key in ['Emp_Id', 'First_Name', 'Last_Name', 'Date_Of_Joining']):
            table.put_item(Item=item)
            return {
                'statusCode': 201,
                'body': json.dumps('Employee record created successfully')
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing one or more required fields')
            }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid JSON payload: {e}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error inserting employee: {e}')
        }

def get_employee(event):
    emp_id = event['queryStringParameters'].get('emp_id')
    
    if not emp_id:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing emp_id query parameter')
        }

    try:
        response = table.get_item(Key={'Emp_Id': emp_id})
        item = response.get('Item')

        if item:
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps(f'Employee with Emp_Id {emp_id} not found')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error retrieving employee: {e}')
        }
