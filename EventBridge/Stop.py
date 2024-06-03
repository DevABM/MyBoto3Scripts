import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Extract query parameters
    key = event.get('queryStringParameters', {}).get('key')
    value = event.get('queryStringParameters', {}).get('value')
    
    if key and value:
        # Get a list of all running instances with the specified tag
        response = ec2.describe_instances(Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': f'tag:{key}', 'Values': [value]}
        ])
    else:
        # Get a list of all running instances if no tag is specified
        response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    
    # Collect all instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if instance_ids:
        print(f"Stopping instances: {instance_ids}")
        ec2.stop_instances(InstanceIds=instance_ids)
        return {
            'statusCode': 200,
            'body': f'Stopped instances: {instance_ids}'
        }
    else:
        print("No running instances to stop.")
        return {
            'statusCode': 200,
            'body': 'No running instances to stop.'
        }

if __name__ == "__main__":
    stop_all_instances()

