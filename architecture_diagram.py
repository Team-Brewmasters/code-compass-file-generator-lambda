import re

import boto3
import requests

from s3_service import S3Service


def get_sequence_diagram(text, file_name, style='default'):
    
    s3_service = S3Service()

    request = {
        "message": text,
        "style": style,
        "apiVersion": "1"
    }

    response = requests.post("https://www.websequencediagrams.com/", data=request)

    expr = re.compile("(\\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
    m = expr.search(response.text)

    if m is None:
        print("Invalid response from server.")
        return None

    diagram_url = "https://www.websequencediagrams.com/" + m.group(0)
    diagram_response = requests.get(diagram_url)

    diagram_data = diagram_response.content

    if diagram_data:
        s3_service.upload_file_to_s3('', file_name, diagram_data)
        presigned_url = s3_service.generate_presigned_url('', file_name)
        print("Presigned URL:", presigned_url)
        return presigned_url
    else:
        print("Failed to generate the sequence diagram.")

# style = "default"
# text = """
# Title: Architecture Diagram

# participant User
# participant Frontend
# participant Backend
# participant Database

# User->Frontend: Send Request
# Frontend->Backend: Forward Request
# Backend->Database: Query Data
# Database->Backend: Return Data
# Backend->Frontend: Send Response
# Frontend->User: Display Response
# """

# s3_service = S3Service()
# bucket_name = "your-bucket-name"
# file_name = "architecture_diagram.png"

# diagram_data = get_sequence_diagram(text, style)

