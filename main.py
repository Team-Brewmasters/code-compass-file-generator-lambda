import json

from file_generation_service import FileGenerator
from github_api_service import get_repo_file_contents


def lambda_handler(event, context):
    try:
        github_url = event['queryStringParameters']['githubURL']
        file_type = event['queryStringParameters']['fileType']
        file_content = get_repo_file_contents(github_url)
        print('Retrieved file content from GitHub API. Generating file...')
        file_generator = FileGenerator()

        pre_signed_url = file_generator.generate_file(github_url, file_type, file_content)
        print('File generated successfully.')

        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
            'body': json.dumps({
                'preSignedUrl': pre_signed_url,
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': str(e),
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
        }
    
event = {
    "queryStringParameters": {
    "githubURL": "https://github.com/Team-Brewmasters/code-compass-summary-lambda",
    "fileType": "swagger"
    }
}

lambda_handler(event, None)