from github import Github
import github.InputFileContent
import requests
import re
import json
from cryptography.fernet import Fernet

token = "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"
git = Github(token)
gistKey = "f08ed4ef55b029514b988ef53c4506af"
secretGistKey = "35ac08ae2142858815ceebff88b30462"

def ErrorCheck():
    try:
        gist = git.get_gist(gistKey)
        raw = requests.get(gist.url)
        data = json.loads(raw.text)
        try: 
            out = data["files"]["Accounts.json"]["content"]
            try:
                with open("Accounts.json", "rb") as file:
                    encrypted = file.read()
            except FileNotFoundError:
                return False
        except KeyError:
            return True
    except github.GithubException:
        return True

def UpdateGist(data):
    gist = git.get_gist(gistKey)
    gist.edit("", {"Accounts.json": github.InputFileContent(data.decode("utf-8"))})

def LoadGist():
    gist = git.get_gist(gistKey)
    raw = requests.get(gist.url)
    data = json.loads(raw.text)
    try: 
        out = data["files"]["Accounts.json"]["content"]
    except KeyError:
        with open("Accounts.json", "rb") as file:
            out = file.read()
        return out

    


if __name__ == "__main__":
    print(ErrorCheck())
    print(LoadGist())