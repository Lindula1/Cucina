from github import Github
import github.InputFileContent
import requests
import re
import json
from cryptography.fernet import Fernet

with open('keyFile.key', 'rb') as filekey:
    key = filekey.read()
    fernet = Fernet(key)
gistByteKey = b'gAAAAABmnkojGGYz12iuRtPvCKvPPCclP--e9_pV8fD9_D8ah-pQZo5tYmxnwMBjwGtymDSbveHtS-M8yZcaq2YiAM9obAB4M-qhqyGkSLgAid5G1c_04pB3yUF8nzmZjxsoft20i108'
byteKey = b'gAAAAABmnkj_NUTQ3HzZsvc-VFYRuXVhci_yvM-IBSsCx_isEh3jI8AhhcxKZms84KHfsjcKqU7r-NUghxV1YvVY_0z_EZg904LditoRTW31orrBdf4ok3QWWLeWvj4HU9ZOlY663Qjs'

token = str(fernet.decrypt(byteKey).decode("utf-8"))
git = Github(token)
gistKey = str(fernet.decrypt(gistByteKey).decode("utf-8"))

def ErrorCheck():
    try:
        gist = git.get_gist(gistKey)
        return False
    except github.GithubException:
        return True

def UpdateGist(data):
    gist = git.get_gist(gistKey)
    gist.edit("", {"Accounts.json": github.InputFileContent(data)})

def LoadGist():
    gist = git.get_gist(gistKey)
    raw = requests.get(gist.url)
    data = json.loads(raw.text)
    return data["files"]["Accounts.json"]["content"]
    


if __name__ == "__main__":
    print(ErrorCheck())
    print(LoadGist())