import re
import time

import boto3

import fpApiClient
import incident_values_enum


def build_dict(msg):
    result_dict = {}
    pattern = r'"([^"]+)"'
    matches = re.findall(pattern, msg)

    for i, match in enumerate(matches):
        key = f"val_{i + 1}"
        result_dict[key] = match
    return result_dict


def set_severity(msg):
    params = build_dict(msg)
    partition_index = fpApiClient.get_partition_index_by_incident_id(params["val_2"])
    values = {"incident_id": params["val_2"],
              "partition_index": partition_index,
              "type": incident_values_enum.Incident_type.INCIDENTS.name,
              "action_type": incident_values_enum.Action_type.SEVERITY.name,
              "value": incident_values_enum.Severity[params["val_1"].upper()].name
              }
    fpApiClient.update_incident_status(values)


def set_status(msg):
    params = build_dict(msg)
    partition_index = fpApiClient.get_partition_index_by_incident_id(params["val_2"])
    values = {"incident_id": params["val_2"],
              "partition_index": partition_index,
              "type": incident_values_enum.Incident_type.INCIDENTS.name,
              "action_type": incident_values_enum.Action_type.STATUS.name,
              "value": incident_values_enum.Incident_status[params["val_1"].upper()].name
              }
    fpApiClient.update_incident_status(values)


def convert_msg_to_action(msg):
    if "get yesterday incidents" in msg:
        fpApiClient.get_yesterday_incidents()
    elif "set severity to" in msg:
        set_severity(msg)
    elif "set status incident to" in msg:
        set_status(msg)
    elif "get incidents from today" in msg:
        fpApiClient.get_today_incidents()


aws_access_key_id = 'YOUR KEYS'
aws_secret_access_key = 'YOUR SECRET'

# Create an SQS client
sqs = boto3.client('sqs', region_name='eu-central-1',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)

# Get the URL for the queue you want to pull messages from
queue_url = 'https://sqs.eu-central-1.amazonaws.com/326435602945/SlackQue'

# Continuously pull messages from the queue
while True:
    # Receive messages from the queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # maximum number of messages to pull at a time
        WaitTimeSeconds=20  # long polling wait time
    )

    # If there are messages in the response
    if 'Messages' in response:
        # Process each message
        for message in response['Messages']:
            # Print the message body
            print(message['Body'])
            body = message['Body']
            if not body:
                print("body empty")
            else:
                print("body with content")
                convert_msg_to_action(body)

            # Delete the message from the queue so it's not processed again
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    else:
        # There are no messages in the queue, so sleep for a while
        time.sleep(10)
