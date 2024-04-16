import boto3
import secrets

class Config(object):
    """Base configuration."""

    DEBUG = True
    BUCKET_NAME = 'source-photo'
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:351528229736:photo_processing_complete"
    AWS_DEFAULT_REGION="us-east-1"
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    


    # Generate a secure secret key
    SECRET_KEY = secrets.token_urlsafe(32)  

    # Define allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'svg', 'webp', 'heic', 'heif', 'raw', 'psd', 'eps'}

    # Use default region configuration for AWS SDK
    AWS_DEFAULT_REGION = 'us-east-1'

    # Set up AWS credentials securely using IAM roles or AWS configuration files
    session = boto3.Session()

    # Get AWS credentials from the session
    credentials = session.get_credentials()
    if credentials is None or credentials.access_key is None or credentials.secret_key is None:
        raise ValueError("AWS credentials not found or expired")

    AWS_ACCESS_KEY_ID = credentials.access_key
    AWS_SECRET_ACCESS_KEY = credentials.secret_key
    AWS_SESSION_TOKEN = credentials.token

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

# Choose the appropriate configuration for your environment
app_config = DevelopmentConfig  # Change to ProductionConfig for production
