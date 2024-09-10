import boto3
import configparser

'''
In this file, I'm practicing programmatically reading in a file and inserting it into an S3 bucket,
but the requirements are that the bucket must have encryption in place. If not, do not put into the
bucket. If there's a way to add encryption from boto3, do it conditionally in this script, then add.
Otherwise, I will have to manually make it so in the console. Another security feature that I intend 
to practice is to not put my AWS credentials in this script (even though it's going to a private repo),
but rather I intend to read in my credentials from a .config file that is on the .gitignore.
'''

config = configparser.ConfigParser()
config.read('config.ini')

KEY_ID = config['AWS Access Key Id']['key_id']
SECRET = config['AWS Secret Key']['secret']

# Create New Bucket

