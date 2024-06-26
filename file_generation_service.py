import json

import boto3
import yaml

from architecture_diagram import get_sequence_diagram
from open_ai_service import (create_architecture_diagram,
                             create_business_rules_csv, create_readme_file,
                             create_swagger_yaml)
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
            case "architecture":
                return self.generate_architecture_diagram(github_url, file_contents)
            case "business_rules":
                return self.generate_business_rules_csv(github_url, file_contents)
            case _:
                print(f"Unsupported file type: {file_type}")
            


        # file_name = f"generated_file.{file_type}"
        # with open(file_name, "w") as file:
        #     file.write(file_contents)
        # print(f"Generated file '{file_name}' with contents:\n{file_contents}")

 

    def generate_read_me(self, github_url, file_contents):
        try:
            readme_file = create_readme_file(file_contents)
            print("Generated Readme file content")
            print(readme_file)
            self.s3_service.upload_file_to_s3("", self.__extract_file_name_git_url(github_url, "readme.md"), readme_file)
            print("Uploaded Readme file to S3")
            return self.s3_service.generate_presigned_url("", self.__extract_file_name_git_url(github_url, "readme.md"))
        except Exception as e:
            raise Exception(f"Failed to generate Readme file: {e}")

    def generate_swagger(self, github_url, file_contents):
        try:
            swagger_yaml_contents = create_swagger_yaml(file_contents)
            print("Generated Swagger YAML content")
            print(swagger_yaml_contents)
            cleaned_yaml = self.validate_and_correct_yaml(swagger_yaml_contents)

            if cleaned_yaml is None:
                raise Exception("Failed to clean Swagger YAML content")
            print("Cleaned Swagger YAML content")
            self.s3_service.upload_file_to_s3("", self.__extract_file_name_git_url(github_url, "swagger.yaml"), cleaned_yaml)

            print("Uploaded Swagger YAML file to S3")

            return self.s3_service.generate_presigned_url("", self.__extract_file_name_git_url(github_url, "swagger.yaml"))
        except Exception as e:
            raise Exception(f"Failed to generate Swagger YAML file: {e}")
        
    def generate_architecture_diagram(self, github_url, file_contents):
        try:
            diagram_code = create_architecture_diagram(file_contents)
            file_name = self.__extract_file_name_git_url(github_url, "diagram.png")
            return get_sequence_diagram(diagram_code, file_name)
        except Exception as e:
            raise Exception(f"Failed to generate architecture diagram: {e}")
    
    def generate_business_rules_csv(self, github_url, file_contents):
        try:
            business_rules_csv = create_business_rules_csv(file_contents)
            print("Generated Business Rules CSV content")
            print(business_rules_csv)
            self.s3_service.upload_file_to_s3("", self.__extract_file_name_git_url(github_url, "business_rules.csv"), business_rules_csv)
            print("Uploaded Business Rules CSV file to S3")
            return self.s3_service.generate_presigned_url("", self.__extract_file_name_git_url(github_url, "business_rules.csv"))
        except Exception as e:
            raise Exception(f"Failed to generate Business Rules CSV file: {e}")
        
    def __extract_file_name_git_url(self, github_url, file_type):
        return github_url.split("/")[-1] + "-" + f"{file_type}"

    def validate_and_correct_yaml(self, yaml_content):
        print("Validating and correcting YAML content...")

        try:
            # Preprocess the YAML content
            yaml_content = yaml_content.replace("\\n", "\n")  # Replace \n with actual newline characters
            yaml_content = yaml_content.replace("\\t", "  ")  # Replace \t with two spaces for indentation
            yaml_content = yaml_content.replace("\\'", "'")  # Replace \' with single quote
            yaml_content = yaml_content.replace('yaml\n','')
            
            yaml_content = yaml_content.replace('```','')
            
            # Load the YAML content
            data = yaml.safe_load(yaml_content)

            # Dump the YAML data back to a string with proper formatting
            corrected_yaml = yaml.dump(data, default_flow_style=False, indent=2, sort_keys=False)

            return corrected_yaml
        except yaml.YAMLError as exc:
            print("Error in YAML formatting: ", exc)
            return None
        
    def retrieve_cached_file(self, github_url, file_type):
        file_name = ""
        match file_type:
            case "swagger":
                file_name = self.__extract_file_name_git_url(github_url, "swagger.yaml")
            case "readme":
                file_name = self.__extract_file_name_git_url(github_url, "readme.md")
            case "architecture":
                file_name = self.__extract_file_name_git_url(github_url, "diagram.png")
            case "business_rules":
                file_name = self.__extract_file_name_git_url(github_url, "business_rules.csv")
            case _:
                print(f"Unsupported file type: {file_type}")
                raise Exception(f"Unsupported file type: {file_type}")

        if self.s3_service.does_file_exist("", file_name):
            return self.s3_service.generate_presigned_url("", file_name)
        return None
                    
