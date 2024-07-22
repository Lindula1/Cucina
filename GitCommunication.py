from github import Github
import github.InputFileContent
import requests
import re
import json

token = "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"
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