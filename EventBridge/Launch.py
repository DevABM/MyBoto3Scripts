import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Parameters for the instance
    image_id = 'ami-0ca2e925753ca2fb4'  # Replace with your AMI ID
    instance_type = 't2.micro'
    key_name = 'Doc1'  # Replace with your key pair name
    security_group_id = 'sg-xxxxxxxxxxxx'  # Replace with your security group ID
    subnet_id = 'subnet-xxxxxxxxxxxx'  # Replace with your subnet ID
    
    try:
        # Launch the instance
        response = ec2_client.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            MinCount=2,
            MaxCount=2,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Env',
                            'Value': 'Dev'
                        }
                    ]
                }
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f'Launched EC2 instance {instance_id}')
        
    except Exception as e:
        print(f'Error launching EC2 instance: {e}')

    return {
        'statusCode': 200,
        'body': f'Launched EC2 instance {instance_id}'
    }
