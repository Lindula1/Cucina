"""
===CUCINA ONLINE DATABASE MODULE===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 18/05/2024
Last Edited: 06/07/2024
Description:
A failed module that was meant to simulate a pseudo database.
"""
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
    return False
    try:
        gist = git.get_gist(secretGistKey)
        raw = requests.get(gist.url)
        data = json.loads(raw.text)
        try: 
            out = data["files"]["Accounts.json"]["content"]
        except KeyError:
            if Force():
                 return False
            else:
                return True
    except github.GithubException:
        if Force():
            return False
        else:
            return True

def Force():
    try:
        with open("Accounts.json", "rb") as file:
            encrypted = file.read()
        return encrypted
    except FileNotFoundError:
        return []

def UpdateGist(data):
    gist = git.get_gist(secretGistKey)
    gist.edit("", {"Accounts.json": github.InputFileContent(data.decode("utf-8"))})

def LoadGist():
    return Force()
    gist = git.get_gist(secretGistKey)
    raw = requests.get(gist.url)
    data = json.loads(raw.text)
    try: 
        out = data["files"]["Accounts.json"]["content"]
        return out
    except KeyError:
        print("force")
        if Force():
            return Force()
    


if __name__ == "__main__":
    #print(ErrorCheck())
    print(LoadGist())