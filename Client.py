import requests as req
import json

url = "http://localhost:8080/filepath/"

filepath = input("Enter the file path:")
url = url+filepath

response = req.get(url)
print("File size: ",response.json())
