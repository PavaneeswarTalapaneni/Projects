import boto3
import botocore.config
import json
from datetime import datetime

def blog_generate_using_bedrock(blogtopic: str) -> str:
    # Creating the prompt with the topic
    prompt = f"Write a 200-word blog on the topic '{blogtopic}'"

    # Correct body structure based on the provided schema
    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 512,  # Adjust this as per your requirement, or 4096 as max limit
            "stopSequences": [],  # You can specify sequences to stop generation, if needed
            "temperature": 0.5,  # Control randomness
            "topP": 0.9  # Nucleus sampling
        }
    }

    try:
        # Initializing the Bedrock client
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))

        # Making the API call with the correct headers and body
        response = bedrock.invoke_model(
            modelId="amazon.titan-text-lite-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        # Parsing the response content
        response_content = response.get('body').read()
        response_data = json.loads(response_content)

        # Extracting the generated blog text from the response
        blog_details = response_data['results'][0]['outputText']  #  'outputText' contains the blog text
        return blog_details

    except Exception as e:
        print(f"Error generating the blog: {e}")
        return ""

def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Blog saved to S3")

    except Exception as e:
        print(f"Error when saving the blog to S3: {e}")

def lambda_handler(event, context):
    # Parsing the incoming event
    event = json.loads(event['body'])
    blogtopic = event['blog_topic']

    # Generate blog using Bedrock
    generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if generate_blog:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'awsbedrockdemobypavan'

        # Save the generated blog to S3
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    else:
        print("No blog was generated")

    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is completed')
    }
