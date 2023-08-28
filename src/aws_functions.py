import boto3, os

def fetch_secrets_from_aws(secret_name):
   try:
       session = boto3.session.Session(aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"), 
                                       aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"))
       client = session.client(service_name='secretsmanager', region_name='us-west-2')
       get_secret_value_response = client.get_secret_value(SecretId=secret_name)
       return get_secret_value_response['SecretString']
   except Exception as e:
       print(e)
       return None