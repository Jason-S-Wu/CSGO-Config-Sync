import os, requests, re, shutil
from bs4 import BeautifulSoup

clearTerminal = lambda: os.system('cls')

def findUserdata():
    if os.path.exists("userdata_path.txt"):
        if os.stat("userdata_path.txt").st_size == 0:
            with open("userdata_path.txt", "w") as userdataTXT:
                userdataPath = input("Path to CS:GO Userdata: ")
                userdataPath = userdataPath.replace("'", "").strip("&").strip(" ")
                listOfUserID = os.listdir(userdataPath)
                userdataTXT.write(str(userdataPath))
                return listOfUserID
        else:
            with open("userdata_path.txt") as userdataTXT:
                listOfUserID = os.listdir(userdataTXT.read())
                return listOfUserID
    else:
        with open("userdata_path.txt", "w") as userdataTXT:
            userdataPath = input("Path to CS:GO Userdata: ")
            userdataPath = userdataPath.replace("'", "").strip("&").strip(" ")
            listOfUserID = os.listdir(userdataPath)
            userdataTXT.write(userdataPath)
        return listOfUserID

listOfUserID = findUserdata()

print("Loading ... ")

def findAllAccounts(userList):
    usernames = { }
    index = 1
    for userID in userList:
        if re.match("^[0-9]*$", userID) is not None:
            userData = requests.get(f'https://steamidfinder.com/lookup/[U:1:{userID}]').text
            userDataParse = BeautifulSoup(userData, 'html.parser')
            userNameData = userDataParse.find("div", attrs={'class':'panel-body'}).text
            userNameArr = userNameData.split("\n")
            steamUserName = str(userNameArr[9]).replace("name ", "")
            usernames[index] = {steamUserName:userID}
            index += 1
    return usernames

usernames = findAllAccounts(listOfUserID)

clearTerminal()

def findMainAccountIndex(usernamesDict):
    for index in usernamesDict:
        for account in usernamesDict[index]:
            print(f'[{index}] {account}')
    mainAccountIndex = int(input("\nSelect your main account: "))
    return mainAccountIndex

mainAccountIndex = findMainAccountIndex(usernames)


def findMainAccountID(usernamesDict, mainAccountIndex):
    mainAccountID = list(usernamesDict[mainAccountIndex].values())[0]
    return mainAccountID

mainAccountID = findMainAccountID(usernames, mainAccountIndex)

def findMainAccountName(usernamesDict, mainAccountIndex):
    mainAccountName = list(usernamesDict[mainAccountIndex].keys())[0]
    return mainAccountName

mainAccountName = findMainAccountName(usernames, mainAccountIndex)

def findUserPath():
    with open("userdata_path.txt") as userdataTXT:
        userdataPath = userdataTXT.read()
        return userdataPath

def findOtherAccounts(usernames, mainAccountID):
    otherAccountsID = [ ]
    for index in usernames:
        for account in usernames[index]:
            if usernames[index][account] != mainAccountID:
                otherAccounts = usernames[index][account]
                otherAccountsID.append(otherAccounts)
    return otherAccountsID

otherAccounts = findOtherAccounts(usernames, mainAccountID)

clearTerminal()

def confirmReplacement(userdataPath, mainAccountID, mainAccountName, otherAccounts):
    mainDir = f'{userdataPath}\\{mainAccountID}\\730\\local\\cfg'
    confirm = input(f'Are you sure you want to sync config files for \'{mainAccountName}\'? Type \"YES\" to confirm: ')
    if confirm.upper().strip(" ") == "YES":
        for otherAccount in otherAccounts:
            try:
                shutil.rmtree(f'{userdataPath}\\{otherAccount}\\730\\local\\cfg', ignore_errors=False, onerror=None)
            except:
                pass
            shutil.copytree(mainDir, f'{userdataPath}\\{otherAccount}\\730\\local\\cfg')
    return

userpath = findUserPath()

confirmReplacement(userpath,mainAccountID, mainAccountName, otherAccounts)

clearTerminal()

print("Done syncing config files")
input("Press Anything to QUIT ... ")
