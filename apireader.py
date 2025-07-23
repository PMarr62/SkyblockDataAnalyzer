import requests

def getAPI():
    resp = requests.get("https://api.hypixel.net/v2/skyblock/bazaar")
    return resp.status_code

if __name__ == "__main__":
    print(getAPI())