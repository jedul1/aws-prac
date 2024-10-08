import boto3
import configparser

'''
In this file, I'm practicing programmatically reading in a file and inserting it into an S3 bucket,
but the requirements are that the bucket must have encryption in place. If not, do not put into the
bucket. If there's a way to add encryption from boto3, do it conditionally in this script, then add.
Otherwise, I will have to manually make it so in the console. Another security feature that I intend 
to practice is to not put my AWS credentials in this script (even though it's going to a private repo),
but rather I intend to read in my credentials from a .config file that is on the .gitignore.

I'll be practicing two Well-Architected Framework Principles:
- Operational Excellence: by logging, allowing for smooth debugging operations
- Security: By ensuring that objects in S3 are encrypted at rest and  in transit (if possible) 
    • found out that new objects are encrypted by defualt, unless I specify my own encryption algorithm
'''
# Global vars - to be used in the full scope of the script
config = configparser.ConfigParser()  # Instantiate a ConfigParse object, and store it in variable named 'config'
config.read('config.ini')  # Read text in from config.ini

KEY_ID = config['AWS Access Key Id']['key_id']
SECRET = config['AWS Secret Key']['secret']
REGION = 'us-east-1'

# Establish an AWS session from boto3. The credentials tell AWS the user for this specific session
session = boto3.session.Session(aws_access_key_id=KEY_ID,
                                aws_secret_access_key=SECRET,
                                region_name=REGION)

# In the current session, request to be a client of AWS' S3 Service
client = session.client('s3')


def put_object(bucket_name: str):
    """
    Puts an object in the specified bucket -> bucket_name.
    bucket_name: the name of the bucket to put the file in
    @:returns None
    """
    file_path = input("What's the path to the file you want to put into the bucket? ")
    key = input("What's a key name to give the object? Make sure to include the file type extension ")

    with open(file_path, "rb") as f:
        file_bytes = f.read()
    try:
        client.put_object(Bucket=bucket_name,
                          Body=file_bytes,
                          Key=key
                          )
    except client.exceptions.ClientError:
        # Try logging this
        print(f"The image at path '{file_path}' failed to be put in bucket '{bucket_name}'")


def add_object(bucket: str):
    object_response = input("\nWould you like to add an object to your bucket?"
                            " Type 'y' for yes, otherwise press any other character to exit. ")
    if object_response.lower() != 'y':
        return
    while True:
        put_object(bucket)
        another = input("\nDo you want to add another object to the bucket?"
                        " Type 'y' for yes or any other character to exit: ")
        if another.lower() != 'y':
            break


def main():
    bucket = ''
    bucket_option = input("\nDo you want to create a new bucket or add an object to an existing bucket?"
                          " Type '1' for a new bucket, '2' for an existing bucket, or any other character to exit: ")
    if bucket_option == '1':

        while True:
            print("\nAWS S3 Bucket Naming Rules: "
                  "\n- Bucket names must be a minimum of 3 chars and a max of 63 chars"
                  "\n- Must only consist of lowercase letters, numbers, dots(.) and hyphens(-)"
                  "\n- Must begin and end with a letter or number"
                  "\n- Must not contain two adjacent periods"
                  "\n- Bucket names cannot be in IP address format i.e.: '192.165.5.4'"
                  "\n- Bucket names cannot start with prefixes: 'sthree-', sthree-configurator', or 'amzn-s3-demo'"
                  "\n- Bucket names cannot end with suffixes: '-s3alias', '--ol-s3','.mrap', or '--x-s3'")
            bucket = input(
                "\nWhat's the name of the S3 bucket that you want to create? (S3 Buckets must be globally unique, "
                "so try to make it specific")
            try:
                response = client.create_bucket(
                    Bucket=bucket,
                )
                print("\nBucket successfully created", response)
                break
            except client.exceptions.BucketAlreadyExists as e:
                print(
                    "\nThe bucket that you want to create already exists. AWS buckets must be globally unique, "
                    "try to make a name that is unique")
                bucket_response = input(
                    "\nWould you like to try again? Type 'y' for yes. Type any other character to exit")
                if bucket_response.lower() != 'y':
                    return

    elif bucket_option == '2':
        buckets = dict()
        existing_bucket = input("What's the exact name of the bucket that you want to use? ")
        try:
            buckets = client.list_buckets()
        except:
            print("API issue when trying to get the S3 buckets in your account.")
            # Add an error log for smooth operations
            return

        # List buckets returns a dict - and the 'Buckets' key is a list of dicts
        for current in buckets.get('Buckets'):
            if current.get('Name') == existing_bucket:
                bucket = existing_bucket
                break

    add_object(bucket)


if __name__ == '__main__':
    main()
