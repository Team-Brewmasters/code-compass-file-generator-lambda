import os

from openai import OpenAI

# Set up your OpenAI API credentials

def call_chatgpt(prompt, files):
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    # Call the OpenAI ChatGPT API
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={ "type": "json_object" },
        messages=[{"role": "system", "content": '''You are a master programming engineer designed to analyze a repository and answer questions about that repository. The repo info will be given below.'''}, 
                  {"role": "system", "content": '''Respond in the format of a JSON object with the following structure:{
    "answer": "(The answer to the question (Please respond as detailed as possible. Give step by step guides.))",
    "confidence": "(Your confidence level in how accurate your answer is (0-1) (1 being the most confident)"
}'''},
      {"role": "user", "content": "Repo:" + str(files)},
        {"role": "user", "content": str(prompt)}],
    )

 
    # Extract the generated response from the API response
    generated_response = response.choices[0].message.content

    return generated_response

def create_swagger_yaml(files):
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    # Call the OpenAI ChatGPT API
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a master programming engineer assistant that generates Swagger files for GitHub repositories. You do not need to explain why it may not be fully accurate'},
            {'role': 'user', 'content': f'Please generate a Swagger YAML file for the following repository contents:\n\n{files}\n\nReturn the generated Swagger file content only. Do not provide context or explanations.'}
        ]
    )

 
    # Extract the generated response from the API response
    generated_response = response.choices[0].message.content

    return generated_response

# create_swagger_yaml(['file1', 'file2'])
 