import json

import boto3
import yaml

from open_ai_service import create_swagger_yaml
from s3_service import S3Service


class FileGenerator:

    def __init__(self):
        self.s3_service = S3Service()

    def generate_file(self, github_url, file_type, file_contents):

        match file_type:
            case "swagger":
                return self.generate_swagger(github_url, file_contents)
            case "readme":
                return self.generate_read_me(github_url, file_contents)
            case _:
                print(f"Unsupported file type: {file_type}")
            


        # file_name = f"generated_file.{file_type}"
        # with open(file_name, "w") as file:
        #     file.write(file_contents)
        # print(f"Generated file '{file_name}' with contents:\n{file_contents}")

 

    def generate_read_me(self, github_url, file_contents):


        return ''
        pass

    def generate_swagger(self, github_url, file_contents):
        try:
            swagger_yaml_contents = create_swagger_yaml(file_contents)
            print("Generated Swagger YAML content")

            cleaned_yaml = self.validate_and_correct_yaml(swagger_yaml_contents)
            print("Cleaned Swagger YAML content")

            if cleaned_yaml is None:
                raise Exception("Failed to clean Swagger YAML content")
            
            self.s3_service.upload_file_to_s3("file-genertions", self.__extract_file_name_git_url(github_url, "swagger"), cleaned_yaml)

            print("Uploaded Swagger YAML file to S3")
            
            return self.s3_service.generate_presigned_url("file-genertions", self.__extract_file_name_git_url(github_url, "swagger"))
        except Exception as e:
            raise Exception(f"Failed to generate Swagger YAML file: {e}")
        
    def __extract_file_name_git_url(self, github_url, file_type):
        return github_url.split("/")[-1] + "-" + f"{file_type}"

    def validate_and_correct_yaml(yaml_content):
        print("Validating and correcting YAML content...")

        try:
            # Preprocess the YAML content
            yaml_content = yaml_content.replace("\\n", "\n")  # Replace \n with actual newline characters
            yaml_content = yaml_content.replace("\\t", "  ")  # Replace \t with two spaces for indentation
            yaml_content = yaml_content.replace("\\'", "'")  # Replace \' with single quote
            yaml_content = yaml_content.replace('yaml\n','')

            # Load the YAML content
            data = yaml.safe_load(yaml_content)

            # Dump the YAML data back to a string with proper formatting
            corrected_yaml = yaml.dump(data, default_flow_style=False, indent=2, sort_keys=False)

            return corrected_yaml
        except yaml.YAMLError as exc:
            print("Error in YAML formatting: ", exc)
            return None
                    
