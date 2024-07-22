from github import Github
import github.InputFileContent
import requests
import re
import json
from cryptography.fernet import Fernet

with open('keyFile.key', 'rb') as filekey:
    key = filekey.read()
    fernet = Fernet(key)
bytekey = b'gAAAAABmnkj_NUTQ3HzZsvc-VFYRuXVhci_yvM-IBSsCx_isEh3jI8AhhcxKZms84KHfsjcKqU7r-NUghxV1YvVY_0z_EZg904LditoRTW31orrBdf4ok3QWWLeWvj4HU9ZOlY663Qjs'

token = str(fernet.decrypt(bytekey).decode("utf-8"))
git = Github(token)

def ErrorCheck():
    try:
        gist = git.get_gist("f08ed4ef55b029514b988ef53c4506af")
        return False
    except github.GithubException:
        return True

def UpdateGist(data):
    gist = git.get_gist("f08ed4ef55b029514b988ef53c4506af")
    gist.edit("", {"Accounts.json": github.InputFileContent(data)})

def LoadGist():
    gist = git.get_gist("f08ed4ef55b029514b988ef53c4506af")
    raw = requests.get(gist.url)
    data = json.loads(raw.text)
    return data["files"]["Accounts.json"]["content"]
    


if __name__ == "__main__":
    print(ErrorCheck())
    print(LoadGist())