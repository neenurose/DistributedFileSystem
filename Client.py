import requests as req
import json

url = "http://localhost:8080/file/"

filepath = input("Enter the file name:")
url = url+filepath

response = req.get(url)
#print("File: ",response.json())
print("Response: ",response.text)
