import requests as req
import json

url = "http://localhost:8082/file/lock/"

filepath = input("Enter the file name:")
url = url+filepath

response = req.post(url)
#print("File: ",response.json())
print("Response: ",response.text)
