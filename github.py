from os import mkdir
from time import time
from pathlib import Path
from requests import get
from json import loads, dump
from datetime import datetime

def getrate():
    d = loads(get(str("https://api.github.com/rate_limit"), auth=(optionsd["credentials"]["username"], optionsd["credentials"]["password"])).text)
    pritn("Limit:    ", d["rate"]["limit"])
    pritn("Used:     ", d["rate"]["used"])
    pritn("Remaining:", d["rate"]["remaining"])
    pritn("Resets at:", datetime.fromtimestamp(d["rate"]["reset"]).strftime("%Y-%m-%d %H:%M:%S"))

def saverepo(d):
    try:
        dump(d, open("cache/repos/" + repo + ".json", "w"))
    except:
        mkdir("cache/repos/" + repo.split("/")[0])
        dump(d, open("cache/repos/" + repo + ".json", "x"))

def loadrepo():
    try:
        if(options["cache_enabled"] and time() < Path("cache/repos/" + repo + ".json").stat().st_mtime + optionsd["cache_persistence"]):
            d = loads(open("cache/repos/" + repo + ".json", "r").read())
        else:
            d = loads(get(str("https://api.github.com/repos/" + repo), auth=(optionsd["credentials"]["username"], optionsd["credentials"]["password"])).text)
    except:
        d = loads(get(str("https://api.github.com/repos/" + repo), auth=(optionsd["credentials"]["username"], optionsd["credentials"]["password"])).text)
    return d

def pritn(i, j):
    try:
        print(i, j)
    except:
        print(i, "ERROR")

def getrepodata():
    global repo
    print("Enter repo")
    repo = input(">")
    data = loadrepo()
    if(optionsd["cache_enabled"]):
        saverepo(data)

    pritn("Repo owner:      ", data["owner"]["login"])
    pritn("Repo name:       ", data["name"])
    pritn("Repo description:", data["description"])
    pritn("Private:         ", data["private"])
    pritn("Fork:            ", data["fork"])
    pritn("Repo URL:        ", data["html_url"])
    pritn("Creation date:   ", data["created_at"].replace("T", " ").replace("Z", ""))
    pritn("Language:        ", data["language"])
    pritn("Number of forks: ", data["forks_count"])
    if (data["license"] is None):
        pritn("License:         ", "No license")
    else:
        pritn("License:         ", data["license"]["name"])
    pritn("Default branch:  ", data["default_branch"])
    pritn("Size:            ", data["size"])

def options():
    e = False
    while not e:
        if(optionsd["cache_enabled"]):
            print("1. Cache enabled")
        else:
            print("1. Cache disabled")
        print("2. Cache Persistence", optionsd["cache_persistence"])
        print("3. Back")
        i = int(input(">"))
        if(i==1):
            if(optionsd["cache_enabled"]):
                optionsd["cache_enabled"] = False
            else:
                optionsd["cache_enabled"] = True
        if(i==2):
            print("Enter new persistence")
            optionsd["cache_persistence"] = int(input(">"))
        if(i==3):
            dump(optionsd, open("options.json", "w"))
            e = True

def loaduser():
    try:
        if(options["cache_enabled"] and time() < Path("cache/users/" + user + ".json").stat().st_mtime + optionsd["cache_persistence"]):
            d = loads(open("cache/users/" + user + ".json", "r").read())
        else:
            d = loads(get(str("https://api.github.com/users/" + user), auth=(optionsd["credentials"]["username"], optionsd["credentials"]["password"])).text)
    except:
        d = loads(get(str("https://api.github.com/users/" + user), auth=(optionsd["credentials"]["username"], optionsd["credentials"]["password"])).text)
    return d

def getuserdata():
    global user
    print("Enter user")
    user = input(">")
    data = loaduser()
    if(optionsd["cache_enabled"]):
        saveuser(data)

    pritn("Username:     ", data["login"])
    pritn("Name:         ", data["name"])
    pritn("Bio:          ", data["bio"])
    pritn("ID:           ", data["id"])
    pritn("User page:    ", data["html_url"])
    pritn("Avatar:       ", data["avatar_url"].replace("?v=4", ""))
    pritn("Creation date:", data["created_at"].replace("T", " ").replace("Z", ""))
    pritn("Public repos: ", data["public_repos"])
    pritn("Public gists: ", data["public_gists"])
    pritn("Followers:    ", data["followers"])
    pritn("Following:    ", data["following"])
    pritn("Account type: ", data["type"])
    pritn("Company:      ", data["company"])
    pritn("Location:     ", data["location"])
    pritn("Email:        ", data["email"])
    pritn("Hireable:     ", data["hireable"])
    pritn("Twitter:      ", data["twitter_username"])

def saveuser(d):
    try:
        dump(d, open("cache/users/" + user + ".json", "w"))
    except:
        mkdir("cache/users/" + repo.split("/")[0])
        dump(d, open("cache/users/" + user + ".json", "x"))

try:
    optionsd = loads(open("options.json", "r").read())
except:
    print("Options file not found.")
    print("Generating a new one")
    print()
    print("Enter your github username")
    n = input(">")
    print("Enter you github api key")
    p = input(">")
    d = {
        "cache_enabled": True,
        "cache_persistence": 60,
        "credentials": {
            "username": n,
            "password": p
        }
    }
    dump(d, open('options.json', 'w'))
    optionsd = loads(open("options.json", "r").read())

while True:
    repo = ""
    user = ""
    print("Select mode")
    print("1. Rate Limit")
    print("2. Repo Data")
    print("3. User Data")
    print("4. Options")
    m = int(input(">"))

    if(m==1):
        getrate()
    if(m==2):
        getrepodata()
    if(m==3):
        getuserdata()
    if(m==4):
        options()

    print()
