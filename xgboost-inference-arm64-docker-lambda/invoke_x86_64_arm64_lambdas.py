import boto3
import json
import base64
import re
import sys

client = boto3.client('lambda')

f= open('./events/event.json')
json_input = json.load(f)


def call_XGBoost_x86_64_Lambda():
    response = client.invoke(
        FunctionName='<XGBoost_x86_64_Lambda_ARN>',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(json_input)
    )
    return(find_duration(response))


def call_XGBoost_arm64_Lambda():
    response = client.invoke(
        FunctionName='<XGBoost_arm64_Lambda_ARN>',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(json_input)
    )

    return(find_duration(response))


def find_duration(response):
    log_result = base64.b64decode(response['LogResult']).decode('utf-8')
    result = re.findall(r'Duration: (\d+\.\d+) ms', log_result)
    return (float(result[0]))

# Warm the two Lambda Functions first
print("Warming x86_64 and arm64 Lambda Functions")
call_XGBoost_x86_64_Lambda()
call_XGBoost_arm64_Lambda()

print("Warming x86_64 and arm64 Lambda Functions - Done")
print("Sending events to x86_64 and arm64 Lambda Functions")

counter=1
num_calls=100
total_duration_x86_64=0
total_duration_arm64=0

while counter < num_calls:
    duration_x86_64 = call_XGBoost_x86_64_Lambda()
    # print(f'call_XGBoost_x86_64_Lambda duration: {duration_x86_64}')
    total_duration_x86_64 = total_duration_x86_64 + duration_x86_64

    duration_arm64 = call_XGBoost_arm64_Lambda()
    # print(f'call_XGBoost_arm64_Lambda duration: {duration_arm64}')
    total_duration_arm64 = total_duration_arm64 + duration_arm64

    sys.stdout.write(('=' * counter) + ('' * (num_calls - counter)) + ("\r [ %d" % counter + "% ] "))
    sys.stdout.flush()

    counter = counter + 1

print("\nSending events to x86_64 and arm64 Lambda Functions - Done")

avg_duration_x86_64 = total_duration_x86_64/num_calls
avg_duration_arm64 = total_duration_arm64/num_calls
improvement_percentage= "{:.0%}".format(1 - (avg_duration_arm64 / avg_duration_x86_64))

print('Average duration x86_64: {:.2f} ms'.format(total_duration_x86_64/num_calls))
print('Average duration arm64: {:.2f} ms'.format(total_duration_arm64/num_calls))
print(f'*** Improvement of arm64 (Graviton2) over x86_64: {improvement_percentage} ***')