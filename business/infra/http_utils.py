import requests


def getFromUrl(url, headers={}):
    response = requests.get(url, headers=headers)
    return (response.status_code, response.json())


def postFromUrl(url, body={}, headers={}):
    response = requests.post(url, data=body, headers=headers)
    return (response.status_code, response.json())


def isSuccessfulResult(statusCode):
    return statusCode >= 200 and statusCode < 300
