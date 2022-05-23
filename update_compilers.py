#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
import requests as req
import os
from shutil import rmtree
import tarfile as t
from sys import argv

homeDir = "/home/sharpcdf/"
maxComp = 4
currentComp = 0

def updateOdin():
    global maxComp, currentComp
    odinVer = bs(req.get("https://github.com/odin-lang/Odin/releases/latest/").content, 'html.parser').find_all('h1', 'd-inline mr-3')[0].string
    print("Removing current Odin compiler...")
    if os.path.exists(homeDir + "Odin"):
        rmtree(homeDir + "Odin")
    print("Downloading Odin compiler...")
    os.system("git clone https://github.com/odin-lang/Odin " + homeDir + "/Odin")
    print("Building Odin compiler...")
    os.system("cd " + homeDir + "Odin && make")
    print("Done!")
    currentComp += 1
    print(f"Finished updating Odin compiler, version {odinVer} [{currentComp}/{maxComp}]\n")

def updateNim():
    global maxComp, currentComp
    print("Removing current Nim compiler...")
    if os.path.exists(homeDir + "Nim"):
        rmtree(homeDir + "Nim")
    print("Downloading Nim compiler...")
    nimVer = bs(req.get("https://nim-lang.org").content, 'html.parser').find_all('a', 'pure-button pure-button-primary')[0].string.removeprefix("Install Nim ")
    nimComp = req.get("https://nim-lang.org/download/nim-" + nimVer + "-linux_x64.tar.xz")
    if not nimComp.ok:
        print("Error downloading Nim compiler, exiting...")
        exit()
    open(homeDir + "nim.tar.xz", 'wb').write(nimComp.content)
    print("Extracting Nim compiler...")
    tar = t.open(homeDir + "nim.tar.xz")
    tar.extractall(homeDir)
    tar.close()
    print("Cleaning up...")
    os.remove(homeDir + "nim.tar.xz")
    os.rename(homeDir + "nim-" + nimVer, homeDir + "Nim")
    currentComp += 1
    print(f"Finished updating Nim compiler, version {nimVer} [{currentComp}/{maxComp}]\n")


def updateGo():
    global maxComp, currentComp
    print("Removing current Go compiler...")
    if os.path.exists(homeDir + "Go"):
        rmtree(homeDir + "Go")
    print("Downloading Go compiler...")
    goVer = bs(req.get("https://go.dev/dl/").content, 'html.parser').find_all('span', 'filename')[0].string.removeprefix("go").removesuffix(".windows-amd64.msi")
    goComp = req.get("https://go.dev/dl/go" + goVer + ".linux-amd64.tar.gz")
    if not goComp.ok:
        print("Error downloading Go compiler, exiting...")
        exit()
    open(homeDir + "go.tar.gz", 'wb').write(goComp.content)
    print("Extracting Go compiler...")
    tar = t.open(homeDir + "go.tar.gz")
    tar.extractall(homeDir)
    tar.close()
    print("Cleaning up...")
    os.remove(homeDir + "go.tar.gz")
    os.rename(homeDir + "go", homeDir + "Go")
    currentComp += 1
    print(f"Finished updating Go compiler, version {goVer} [{currentComp}/{maxComp}]\n")

def updateD():
    global maxComp, currentComp
    print("Removing current D compiler...")
    if os.path.exists(homeDir + "LDC2"):
        rmtree(homeDir + "LDC2")
    print("Updating script...")
    dVer = bs(req.get("https://github.com/ldc-developers/ldc").content, 'html.parser').find_all('span', 'css-truncate css-truncate-target text-bold mr-2')[0].string.removeprefix("LDC ")
    os.system("./install_dlang.sh update -p .")
    os.remove("d-keyring.gpg")
    os.remove("install_dlang.sh")
    os.rename("install.sh", "install_dlang.sh")
    print("Updating D compiler...")
    os.system("./install_dlang.sh install ldc -p " + homeDir)
    print("Cleaning up...")
    os.remove(homeDir + "d-keyring.gpg")
    os.remove(homeDir + "install.sh")
    os.rename(homeDir + "ldc-" + dVer, homeDir + "LDC2")
    currentComp += 1
    print(f"Finished updating D compiler, version {dVer} [{currentComp}/{maxComp}]\n")
if len(argv) > 1:
    #print(argv[1])
    if argv[1].lower() == "all":
        updateOdin()
        updateNim()
        updateGo()
        updateD()
    elif argv[1].lower() == "odin":
        updateOdin()
    elif argv[1].lower() == "nim":
        updateNim()
    elif argv[1].lower() == "go":
        updateGo()
    elif argv[1].lower() == "d":
        updateD()
else:
    updateOdin()
    updateNim()
    updateGo()
    updateD()
print("Done updating compilers!")
