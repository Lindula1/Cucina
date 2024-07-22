from github import Github
import github.InputFileContent
import requests
import re
import json
from cryptography.fernet import Fernet

token = "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"
git = Github(token)
gistKey = "f08ed4ef55b029514b988ef53c4506af"

def ErrorCheck():
    try:
        gist = git.get_gist(gistKey)
        return False
    except github.GithubException:
        return True

def UpdateGist(data):
    gist = git.get_gist(gistKey)
    gist.edit("", {"Accounts.json": github.InputFileContent(data.decode("utf-8"))})

def LoadGist():
    gist = git.get_gist(gistKey)
    raw = requests.get(gist.url)
    data = json.loads(raw.text)
    return data["files"]["Accounts.json"]["content"]
    


if __name__ == "__main__":
    print(ErrorCheck())
    print(LoadGist())