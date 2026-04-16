import boto3
from moto import mock_aws
import json
import os
from lambda_function import lambda_handler

@mock_aws
def test_count_increments():
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert response['statusCode'] == 200

@mock_aws
def test_count_increment_twice():
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    response = lambda_handler({}, {})
    assert response['statusCode'] == 200
    assert response['body'] == '2'

@mock_aws
def test_response_body_contains_count():
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert response['body'] == '1'

@mock_aws
def test_body_is_int():
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert isinstance(json.loads(response['body']), int)

@mock_aws
def test_CORS_headers():
    ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN')
    table = boto3.resource('dynamodb').create_table(
        TableName = 'resume-visitor-count',
        KeySchema = [{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode = 'PAY_PER_REQUEST'
    )
    table.put_item(Item={'id': 'visitors', 'count': 0})
    response = lambda_handler({}, {})
    assert response['headers']['Access-Control-Allow-Origin'] == ALLOWED_ORIGIN
    assert response['headers']['Access-Control-Allow-Methods'] == 'GET'
    assert response['headers']['Access-Control-Allow-Headers'] == 'Content-Type'

@mock_aws
def test_table_missing():
    response = lambda_handler({}, {})
    assert response['statusCode'] == 500