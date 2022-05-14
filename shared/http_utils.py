import requests

def getFromUrl(url, headers={}):
    response = requests.get(url, headers=headers)
    return (response.status_code, getResponseValue(response))


def postFromUrl(url, body={}, headers={}):
    response = requests.post(url, data=body, headers=headers)
    return (response.status_code, getResponseValue(response))


def isSuccessfulResult(statusCode):
    return statusCode >= 200 and statusCode < 300


def getResponseValue(response):
    try:
        return response.json()
    except ValueError:
        try:
            return response.text()
        except:
            return None
