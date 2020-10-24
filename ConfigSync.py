import os, requests, re, shutil
from bs4 import BeautifulSoup

def findUserdata():
    if os.path.exists("userdata_path.txt"):
        if os.stat("userdata_path.txt").st_size == 0:
            with open("userdata_path.txt", "w") as userdataTXT:
                userdataPath = input("Path to CS:GO Userdata: ")
                userdataPath = userdataPath.replace("'", "").replace("\"","").strip("&").strip(" ")
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

def findMainAccountIndex(usernamesDict):
    for index in usernamesDict:
        for account in usernamesDict[index]:
            print(f'[{index}] {account}')
    mainAccountIndex = int(input("\nSelect your main account: "))
    return mainAccountIndex

def findMainAccountID(usernamesDict, mainAccountIndex):
    mainAccountID = list(usernamesDict[mainAccountIndex].values())[0]
    return mainAccountID

def findMainAccountName(usernamesDict, mainAccountIndex):
    mainAccountName = list(usernamesDict[mainAccountIndex].keys())[0]
    return mainAccountName

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

def main():
    clearTerminal = lambda: os.system('cls')
    listOfUserID = findUserdata()
    print("Loading ... ")
    usernames = findAllAccounts(listOfUserID)
    clearTerminal()
    mainAccountIndex = findMainAccountIndex(usernames)
    mainAccountID = findMainAccountID(usernames, mainAccountIndex)
    mainAccountName = findMainAccountName(usernames, mainAccountIndex)
    otherAccounts = findOtherAccounts(usernames, mainAccountID)
    clearTerminal()
    userpath = findUserPath()
    confirmReplacement(userpath,mainAccountID, mainAccountName, otherAccounts)
    clearTerminal()
    print("Done syncing config files")
    input("Press Enter to QUIT ... ")

if __name__ == '__main__':
    main()
