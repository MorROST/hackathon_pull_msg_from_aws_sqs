from datetime import datetime, timedelta

import requests
import json

access_token = ""
base_endpoint_url = ""


def get_token(ip):
    global access_token
    global base_endpoint_url
    base_endpoint_url = 'https://' + ip + ':9443/dlp/rest/v1'
    uri = '/auth/refresh-token'
    print(base_endpoint_url + uri)
    headers = {'Content-Type': 'application/json', 'username': 'USER', 'password': 'PASSWORD'}
    print(headers)
    response = requests.post(base_endpoint_url + uri, headers=headers, verify=False)
    access_token = "Bearer " + json.loads(response.content).get('access_token')
    print('Status code:', response.status_code)
    print('token:', "Bearer " + access_token)


def get_yesterday_incidents():
    get_token("10.0.137.100")
    current_time = datetime.now().date()
    today_date = current_time.strftime("%d/%m/%Y")
    yes_date = (current_time - timedelta(1)).strftime("%d/%m/%Y")
    uri = '/incidents/slack'
    headers = {'Content-Type': 'application/json', 'Authorization': access_token}
    data = {'type': 'INCIDENTS', 'from_date': yes_date + ' 00:00:01', 'to_date': today_date + ' 00:00:01'}
    print(data)
    response = requests.post(base_endpoint_url + uri, headers=headers, json=data, verify=False)
    print('Status code:', response.status_code)
    print(response.text)


def get_today_incidents():
    get_token("10.0.137.100")
    current_time = datetime.now().date()
    today_date = current_time.strftime("%d/%m/%Y")
    tomorrow_date = (current_time + timedelta(1)).strftime("%d/%m/%Y")
    uri = '/incidents/slack'
    headers = {'Content-Type': 'application/json', 'Authorization': access_token}
    data = {'type': 'INCIDENTS', 'from_date': today_date + ' 00:00:01', 'to_date': tomorrow_date + ' 00:00:01'}
    print(data)
    response = requests.post(base_endpoint_url + uri, headers=headers, json=data, verify=False)
    print('Status code:', response.status_code)
    print(response.text)


def update_incident_status(values: dict):
    get_token("10.0.137.100")
    uri = '/incidents/update'
    headers = {'Content-Type': 'application/json', 'Authorization': access_token}
    payload = json.dumps({
        "incident_keys": [
            {
                "incident_id": values["incident_id"],
                "partition_index": values["partition_index"]
            }
        ],
        "type": values["type"],
        "action_type": values["action_type"],
        "value": values["value"]
    })
    response = requests.post(base_endpoint_url + uri, headers=headers, data=payload, verify=False)
    print('Status code:', response.status_code)
    print(response.text)


def get_partition_index_by_incident_id(incident_id):
    get_token("10.0.137.100")
    uri = '/incidents'
    headers = {'Content-Type': 'application/json', 'Authorization': access_token}
    payload = json.dumps({
        "ids": [
            incident_id
        ],
        "type": "INCIDENTS"
    })
    response = requests.post(base_endpoint_url + uri, headers=headers, data=payload, verify=False)
    print('Status code:', response.status_code)
    print(response.text)
    return json.loads(response.content).get("incidents")[0].get("partition_index")


if __name__ == '__main__':
    get_token("10.0.137.100")
    # print(get_incident_by_id('262212'))
