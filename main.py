import json

from github_api_service import get_repo_file_contents
from open_ai_service import call_chatgpt


def lambda_handler(event, context):
    try:
        github_url = event['queryStringParameters']['githubURL']
        question = event['queryStringParameters']['question']

        file_content = get_repo_file_contents(github_url)

        open_ai_response = call_chatgpt(question, file_content)
        
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
            'body': json.dumps(open_ai_response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e),
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
        }
    
# event = {
#     "githubURL": "https://www.github.com/Team-Brewmasters/code-compass-summary-lambda"
# }

# lambda_handler(event, None)