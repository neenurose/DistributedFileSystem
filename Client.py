import requests as req
import json
from requests.auth import HTTPBasicAuth

url = "http://localhost:8083/login"

'''
filepath = input("Enter the file name:")
url = url+filepath

response = req.post(url)
#print("File: ",response.json())
print("Response: ",response.text)
'''

# HTTP_AUTHORIZATION
username = input("Enter the user name: ")
password = input("Enter password: ")

response = req.get(url, auth=HTTPBasicAuth(username,password))
#print("File: ",response.json())
print("Response: ",response.text)
