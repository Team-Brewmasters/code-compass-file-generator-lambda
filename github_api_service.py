import requests

ignore_list = ['node_modules', 'favicon.ico', '.gitignore', 'package-lock.json', 'angular.json', 'tsconfig.app.json', 'package.json', 'yarn.lock', 'LICENSE', 'Dockerfile', 'docker-compose.yml', 'jest.config.js', 'tsconfig.json', 'tsconfig.build.json', 'tsconfig.spec.json', 'tslint.json', 'README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'PULL_REQUEST_TEMPLATE.md', 'ISSUE_TEMPLATE.md', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js', '.prettierignore', '.vscode', '.travis.yml', '.gitlab-ci.yml', '.circleci', '.github', '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc.js', '.prettierrc.js']

def get_repo_file_contents(repo_url, path=''):
    # Extract the username and repository name from the URL
    _, _, username, repo_name = repo_url.rstrip('/').split('/')[-4:]
    
    # Construct the API URL to get the repository contents
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"
    
    # Send a GET request to the GitHub API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        file_contents = []
        
        # Iterate over each item in the repository
        for item in response.json():
            if item['type'] == 'file':
                file_name = item['name']
                if file_name not in ignore_list:
                    file_url = item['download_url']
                    
                    # Send a GET request to download the file contents
                    file_response = requests.get(file_url)
                    
                    if file_response.status_code == 200:
                        # Get the file contents as text
                        content = file_response.text
                        
                        # Append the file path and contents to the array
                        file_contents.append(f"{path}/{file_name}\n{content}")
                    else:
                        print(f"Error downloading file '{file_name}': {file_response.status_code} - {file_response.text}")
            elif item['type'] == 'dir':
                # Recursively get the contents of the directory
                dir_path = f"{path}/{item['name']}"
                file_contents.extend(get_repo_file_contents(repo_url, dir_path))
        
        return file_contents
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# # Example usage
# repo_link = "https://github.com/Team-Brewmasters/code-compass-webapp"
# file_contents_array = get_repo_file_contents(repo_link)

# # Print the file contents array
# for file_content in file_contents_array:
#     print(file_content)
#     print("---")