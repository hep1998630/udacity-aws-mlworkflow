"""
This script contains definitions for lambda functions developed for the project 
"""

## First function: serializeImageData
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"] ## TODO: fill in
    bucket = event["s3_bucket"] ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }



## Second function: classifier-lambda 

import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-endpoint"  # TODO: fill in

runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])  # TODO: fill in)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,
                                       #ContentType='text/csv',
                                       Body=image)

    response_inference = response['Body'].read().decode('utf-8')
    event["body"]["inferences"] = response_inference
    return {
        'statusCode': 200,
        'body': event["body"]
    }


## Third function: Filter-lambda
import json
import ast 


THRESHOLD = .93


def lambda_handler(event, context):
    
    # Grab the inferences from the event, I used eval to parse the string into an array 
    inferences = ast.literal_eval(event["body"]["inferences"]) ## TODO: fill in

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = True if max(inferences) > THRESHOLD else False
    
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event
    }



