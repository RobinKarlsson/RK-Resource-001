# -*- coding: utf-8 -*-
# RK resource 001
# developed by Robin Karlsson
# contact chess.com profile: "https://www.chess.com/members/view/SudoRoot"
# version 0.9.1.4 Alfa

import os
from os.path import isfile, join
import sys
import subprocess

try:
    import mechanize
except:
    sys.exit("\n\n\tCouln't import the mechanize library, shutting down\n\n")
mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 100

import gc
import csv
import urlparse
import cookielib
import random
import base64
import stat
import re
import time
import pickle
import platform as _platform
from time import strftime, gmtime
from datetime import datetime, date, timedelta

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.support.ui import Select
except:
    sys.exit("\n\n\tCouln't import the selenium library, shutting down\n\n")

try:
    from bs4 import BeautifulSoup
except:
    sys.exit("\n\n\tCouln't import the BeautifulSoup4 library, shutting down\n\n")

from operator import itemgetter
from collections import OrderedDict
from collections import Counter
from string import punctuation

def csvsoworker(memlist, choicepath):
    colwidth = max(len(element.decode("UTF-8")) for row in memlist for element in row) + 2

    choice = ""
    while choice not in (["1", "2"]):
        choice = raw_input("\n\noptions\n 1. Get data from the csv-file\n 2. get all the usernames in an invites friendly format\nYour choice: ")

    if choice == "1":
        cdone = "y"
        choicelist = (["0"])
        while cdone != "n":
            choice = ""
            print "\n\nwhat would you like to include?"
            for counter in range(len(memlist[0])):
                print " %i. %s" %(counter, memlist[0][counter])

            choice = raw_input("Your choice: ")
            if choice not in choicelist:
                choicelist.append(choice)

            cdone = ""
            while cdone not in (["y", "n"]):
                cdone = raw_input("include more data? (y/n) ")

        memlist2 = list()
        choicelist = sorted(choicelist)
        for cpointer in memlist:
            nlist = list()
            for pospointer in choicelist:
                try:
                    nlist.append(float(cpointer[int(pospointer)]))
                except ValueError:
                    nlist.append(cpointer[int(pospointer)])
            memlist2.append(nlist)

        ltitle = memlist2[0]
        del memlist2[0]

        if choicepath == "1":
            print "\n\nsort by\n 1. most valuable tm participant"
            counter = 2
            coulist = (["1"])
        elif choicepath == "2":
            print "\n\nsort by"
            counter = 1
            coulist = list()

        for pointer in ltitle:
            count2id = str(counter)
            coulist.append(count2id)
            print " %s. %s" %(count2id, pointer)
            counter += 1

        choice2 = ""
        while choice2 not in coulist:
            choice2 = raw_input("Your choice: ")
        choice2 = int(choice2)

        if choice2 == 1 and choicepath == "1":
            "none"
        else:
            if choicepath == "1":
                choice2 -= 2
            elif choicepath == "2":
                choice2 -= 1

            for element in memlist2:
                if type(element[choice2]) is str and element[choice2][0] == "[":
                    element[choice2] = element[choice2].replace("[", "").replace("]", "").split(", ")
                    element[choice2] = [int(subelem) for subelem in element[choice2]]

            if type(memlist2[0][choice2]) is str:
                try:
                    memlist2 = sorted(memlist2, key = lambda tup: tup[0].lower())
                except AttributeError:
                    memlist2 = sorted(memlist2, reverse = False, key = lambda tup: tup[choice2])
            elif type(memlist2[0][choice2]) is float or type(memlist2[0][choice2]) is list:
                memlist2 = sorted(memlist2, reverse = True, key = lambda tup: tup[choice2])

        print "\n\n%s\n" %"".join(element.ljust(colwidth) for element in ltitle)
        llength = len(memlist2[0])

        for cpointer in memlist2:
            for counter in range(llength):
                cpointer[counter] = str(cpointer[counter])
            print "".join(element.ljust(colwidth) for element in cpointer)

        choice2 = raw_input("\n\nGet the same list in an invites friendly format? (y/n): ")

        if choice2 == "y":
            print "\n\n%s\n" %", ".join([x[0] for x in memlist2])

    elif choice == "2":
        del memlist[0]
        memlist2 = list()

        for cpointer in memlist:
            memlist2.append(cpointer[0])

        print "\n\n%s" %", ".join(memlist2)

def getOldTimeouts(groupname):
    timeoutsDictOld = {}
    timeoutsList = []
    fname = "Data/.TimeoutsCheck/%s" %groupname

    if os.path.isfile(fname):
        with open(fname, "rb") as placeholder:
                for line in placeholder.readlines():
                    line = line[0: -1].split(",")
                    timeoutsList.append(line)

                    if line[1] in timeoutsDictOld:
                        timeoutsDictOld[line[1]] += int(line[2])
                    else:
                        timeoutsDictOld[line[1]] = int(line[2])

    return timeoutsList, timeoutsDictOld

def debugout():
    if usrsys != "Windows":
        try:
            print "\tRAM usage (script): %.2f MB" %ramusage()
        except Exception, errormsg:
            print "\tWARNING: Couldn't access RAM usage"
            print repr(errormsg)

    try:
        print "\tCPU usage (system): %.1f%%" %psutil.cpu_percent()
    except Exception, errormsg:
        print "\tWARNING: Couldn't access CPU usage"
        print repr(errormsg)

    try:
        if usrsys == "Linux":
            template = "|{0:6}|{1:9}|{2:20}|{3:7}|{4:7}|{5:8}|{6:9}|"
            print "\n%s\n%s" %(template.format(" Time", "Interface", "ESSID".center(20), "Sig Str", "Quality", "Sig lvl", "Frequency"), template.format("-" * 6, "-" * 9, "-" * 20, "-" * 7, "-" * 7, "-" * 8, "-" * 9))

        elif usrsys == "Windows":
            template = "|{0:6}|{1:15}|"
            print "\n%s\n%s" %(template.format(" Time", "Signal Strength"), template.format("-" * 6, "-" * 15))

        sigstrength(template)
    except Exception, errormsg:
        print "\tWARNING: Couldn't access network strength"
        print repr(errormsg)

    print "\n\n"

def getmeminfo(target, filename):
    browser = mecbrowser("")

    memlist = list()
    outputfile = open("%s %s.mem.csv" %(filename, time.strftime("%Y-%m-%d %H:%M")), "wb")
    csvwriter = csv.writer(outputfile, delimiter = " ", quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(("Username", "Real name", "Live Standard rating", "Live Blitz rating", "Live Bullet rating", "Online rating", "960 rating", "Tactics rating", "Timeout-ratio", "Last online", "Member since", "Time/move", "Groups", "Points", "Total games", "Games won", "Games lost", "Games drawn", "Win ratio", "Nation", "Custom avatar", "Site Awards", "Tournament Trophies", "Game Trophies", "Fun Trophies"))

    for mem in target:
        print "%sProcessing %s" %(ltime(), mem)

        if supusr:
            debugout()

        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %mem)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)
        if "://www.chess.com/members/view/" not in browser.geturl():
            continue

        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/members/trophy_room/%s" %mem)
                awardsoup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        sawards, tourneytrophy, gametrophy, funtrophy = getawards(awardsoup)
        timemove = TimeMoveChecker(soup)
        memsinlastonl = memsin(soup)
        gamestat = gamestats(soup)
        if gamestat[0] != 0.0:
            winratm = gamestat[1] / gamestat[0]
        else:
            winratm = 0

        csvwriter.writerow((mem, namechecker(soup).encode("utf-8"), lstanratingchecker(soup), lblitzratingchecker(soup), lbulratingchecker(soup), onlratingchecker(soup), ranratingchecker(soup), tacratingchecker(soup), timeoutchecker(soup), memsinlastonl[1], memsinlastonl[0], timemove, groupmemlister(soup), ptscheck(soup), gamestat[0], gamestat[1], gamestat[2], gamestat[3], winratm, nationlister(soup).encode("utf-8"), AvatarCheck(soup), sawards, tourneytrophy, gametrophy, funtrophy))

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

def getplatform():
    return _platform.platform(), _platform.system(), _platform.release(), _platform.architecture()

def mecbrowser(logincookie):
    browser = mechanize.Browser()
    cookie = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookie)

    if logincookie != "":
        for tempcookie in logincookie:
            try:
                cookie.set_cookie(cookielib.Cookie(version = 0, name = tempcookie["name"], value = tempcookie["value"], port = '80', port_specified = False, domain = tempcookie["domain"], domain_specified = True, domain_initial_dot = False, path = tempcookie["path"], path_specified = True, secure = tempcookie["secure"], expires = tempcookie["expiry"], discard = False, comment = None, comment_url = None, rest = None, rfc2109 = False))
            except KeyError:
                continue

    browser.set_handle_equiv(True)
    browser.set_handle_redirect(True)
    browser.set_handle_gzip(False)
    browser.set_handle_referer(True)
    browser.set_handle_refresh(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    return browser

def pickbrowser(browserchoice, adext):
    handle = False
    while True:
        if browserchoice == "1":
            fopt = webdriver.FirefoxProfile()
            if adext:
                for fname in os.listdir("Data/Webdriver/Extensions/Firefox"):
                    if fname.endswith(".xpi"):
                        try:
                            fopt.add_extension(os.path.abspath("Data/Webdriver/Extensions/Firefox/%s" %fname))
                            if "adblock" in fname:
                                handle = True
                        except Exception, errormsg:
                            if supusr:
                                print repr(errormsg)
                            print "%sFailed to load %s" %(ltime(), os.path.abspath("Data/Webdriver/Extensions/Firefox/%s" %fname))

            try:
                browser = webdriver.Firefox(fopt)

            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                print "\n\n%sFailed to initiate Firefox with addons, reverting to standard\n\n" %ltime()
                browser = webdriver.Firefox()
            break

        elif browserchoice == "2":
            copt = Options()
            if adext:
                for fname in os.listdir("Data/Webdriver/Extensions/Chrome"):
                    if fname.endswith(".crx"):
                        try:
                            copt.add_extension(os.path.abspath("Data/Webdriver/Extensions/Chrome/%s" %fname))
                            if "adblock" in fname:
                                handle = True
                        except Exception, errormsg:
                            if supusr:
                                print repr(errormsg)
                            print "%sFailed to load %s" %(ltime(), os.path.abspath("Data/Webdriver/Extensions/Chrome/%s" %fname))

            if usrsys == "Linux":
                chromepath32 = os.path.abspath("Data/Webdriver/Linux/86/chromedriver")
                chromepath64 = os.path.abspath("Data/Webdriver/Linux/64/chromedriver")
                os.environ["webdriver.chrome.driver"] = chromepath32
                try:
                    browser = webdriver.Chrome(chromepath32, chrome_options = copt)
                except Exception:
                    try:
                        os.environ["webdriver.chrome.driver"] = chromepath64
                        browser = webdriver.Chrome(chromepath64, chrome_options = copt)
                    except Exception:
                        print "\n\n%sFailed to initiate Chrome with extensions, reverting to standard\n\n" %ltime()
                        try:
                            browser = webdriver.Chrome(chromepath64)
                        except Exception:
                            os.environ["webdriver.chrome.driver"] = chromepath32
                            browser = webdriver.Chrome(chromepath32)
                break

            elif usrsys == "Windows":
                chromepath = os.path.abspath("Data/Webdriver/Windows/86/chromedriver.exe")
                os.environ["webdriver.chrome.driver"] = chromepath
                browser = webdriver.Chrome(chromepath, chrome_options = copt)
                break

            elif usrsys == "Darwin":
                chromepath = os.path.abspath("Data/Webdriver/Mac/86/chromedriver")
                os.environ["webdriver.chrome.driver"] = chromepath
                browser = webdriver.Chrome(chromepath, chrome_options = copt)
                break

        elif browserchoice == "3":
            if usrsys == "Linux":
                browser = webdriver.PhantomJS(os.path.abspath("Data/Webdriver/Linux/86/phantomjs"))
                break

            elif usrsys == "Windows":
                browser = webdriver.PhantomJS(os.path.abspath("Data/Webdriver/Windows/86/phantomjs.exe"))
                break

            elif usrsys == "Darwin":
                browser = webdriver.PhantomJS(os.path.abspath("Data/Webdriver/Mac/86/phantomjs"))
                break

        elif browserchoice == "4":
            if usrsys == "Windows":
                browser = webdriver.Ie(os.path.abspath("Data/Webdriver/Windows/86/IEDriverServer.exe"))
                break

        browserchoice = raw_input("\nSomething went wrong, please send this to the developer: %s   %s\n\nTry and pick another browser\n 1. Firefox\n 2. Chrome\nEnter choice: " %(browserchoice, getplatform()))

    if handle:
        time.sleep(2)
        browser.switch_to_window(browser.window_handles[-1])
    return browser, handle

def com2(xxxxxxxxxxxxxx, xxxxxxxxxxxxx, xxxxxxxxxxxxxxxx, xxxxxxxxxxxxxxxxxxx):
    for xxxxxxxxxxxxxxxxx in xrange(len(xxxxxxxxxxxxx)):
        xxxxxxxxxxxxxxxxxxx.append(chr(ord(xxxxxxxxxxxxx[xxxxxxxxxxxxxxxxx]) + ord(xxxxxxxxxxxxxx[xxxxxxxxxxxxxxxxx % len(xxxxxxxxxxxxxx)]) % xxxxxxxxxxxxxxxx))
    return base64.urlsafe_b64encode("".join(xxxxxxxxxxxxxxxxxxx))

def com3(xxxxxxxxxxxxxx, xxxxxxxxxxxxx, xxxxxxxxxxxxxxxx, xxxxxxxxxxxxxxxxxxx):
    xxxxxxxxxxxxx = base64.urlsafe_b64decode(xxxxxxxxxxxxx)
    for xxxxxxxxxxxxxxxxx in xrange(len(xxxxxxxxxxxxx)):
        xxxxxxxxxxxxxxxxxxx.append(chr(abs(ord(xxxxxxxxxxxxx[xxxxxxxxxxxxxxxxx]) - ord(xxxxxxxxxxxxxx[xxxxxxxxxxxxxxxxx % len(xxxxxxxxxxxxxx)]) % xxxxxxxxxxxxxxxx)))
    return "".join(xxxxxxxxxxxxxxxxxxx)

def gettmopdata(targetname):
    browser = mecbrowser("")
    linklist = gettmlinklist(targetname, browser)

    linkarchive = linklist.pop(-1)
    mtchlist = list()
    pointer = 1

    while True:
        while True:
            try:
                browser, response = mecopner(browser, "%s&page=%i" %(linkarchive, pointer))

                if supusr:
                    debugout()

                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)
        soupbrake = str(soup.find_all(class_ = "next-on"))

        evenmtch = soup.find_all(class_ = "even")
        mtchlist = resource01(evenmtch, mtchlist)

        oddmtch = soup.find_all(class_ = "odd")
        mtchlist = resource01(oddmtch, mtchlist)

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

        if soupbrake == "[]":
            break
        pointer += 1
    return mtchlist

def turnofcomp():
    if usrsys == "Linux":
        import dbus
        try:
            dbus.Interface(dbus.SystemBus().get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager"), "org.freedesktop.ConsoleKit.Manager").get_dbus_method("Stop")() #ConsoleKit
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)

        try:
            dbus.Interface(dbus.SystemBus().sys_bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/devices/computer"), "org.freedesktop.Hal.Device.SystemPowerManagement")() #HAL
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)

    #elif usrsys == "Windows":
     #   os.system("shutdown -h now")

    elif usrsys == "Darwin":
        try:
            subprocess.call(["osascript", "-e", 'tell app "System Events" to shut down'])
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)

    os.system("shutdown -h now")

def ramusage():
    placeholder = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())], stdout = subprocess.PIPE).communicate()[0].split(b'\n')
    return float(placeholder[1].split()[placeholder[0].split().index(b'RSS')]) / 1024

def resource01(evenmtch, mtchlist):
    ctrl = False
    for element in evenmtch:
        if ctrl:
            mtchlist.append(str(element.text.encode("utf8")).split("\n"))
        ctrl = True
    return mtchlist

def gettmlinks(browser, targetname, stopAt):
    linklist = gettmlinklist(targetname, browser)

    linkarchive = linklist.pop(-1)
    pointer = 1

    while True:
        while True:
            try:
                browser, response = mecopner(browser, "%s&page=%i" %(linkarchive, pointer))

                if supusr:
                    debugout()

                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        soupbrake = str(soup.find_all(class_ = "next-on"))
        souplinks = re.findall("/groups/team_match(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]i|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))

        for link in souplinks:
            if stopAt == str(link):
                soup.decompose()
                response.close()
                browser.clear_history()
                gc.collect()

                return linklist

            linklist.append("https://www.chess.com%s" %link)

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

        if soupbrake == "[]":
            break
        pointer += 1

    return linklist

def birthdsorter(birthdaylist):
    choice = "1"
    while choice not in (["1"]):
        choice = raw_input("\n\nOptions:\n 1. print the collected information sorted by birthday\nYour choice: ")

    if choice == "1":
        birthdaylist = sorted(birthdaylist)
        for element in birthdaylist:
            print "%i/%i - %s, born %i" %(element[1], element[0], element[3], element[2])

def getvclinks(yourside):
    linklist = list()
    yourside = re.sub(r"[^a-z A-Z 0-9 -]","", yourside)
    yourside = yourside.replace(" ", "-").lower()
    browser = mecbrowser("")

    for pagenum in range(1, 101):
        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/groups/votechess_diagrams/%s/?sortby=completed&page=%i" %(yourside, pagenum))
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)
        souplinks = re.findall("/votechess/game(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))
        for link in souplinks:
            linklist.append("https://www.chess.com%s" %link)

        soupbrake = str(soup.find_all(class_ = "next-on"))

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

        if soupbrake == "[]":
            break

    linklist = list(OrderedDict.fromkeys(linklist))
    return linklist

def streplacer(text, rplst):
    for rptup in rplst:
        text = text.replace(rptup[0], rptup[1])
    return text

def fnamenot(nlst, fdir):
    flist = list()
    for fname in os.listdir(fdir):
        if os.path.isfile(fname):
            cont = True

            for nfname in nlst:
                if fname.endswith(nfname):
                    cont = False

            if cont != False:
                print fname
                flist.append(fname)
    return flist

def noteposter(target, msg, interval, nationalt, shutdown):
    while "" in target:
        target.remove("")

    browserchoice = selbrowch()
    Username, Password = usrPas()
    browser2, handle = pickbrowser(browserchoice, True)
    browser2 = sellogin(Username, Password, browser2)
    logincookie = browser2.get_cookies()
    browser = mecbrowser(logincookie)
    skipped = list()
    print "\n\n"

    for mem in target:
        if supusr:
            debugout()

        print "%sprocessing: %s" %(ltime(), mem)
        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %mem)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        for placeholder in soup.find_all(class_ = "flag"):
            country = placeholder["title"]

        if country == "International":
            country = nationalt

        name = namechecker(soup)
        if name == " ":
            name = mem

            if "_" in name:
                if isint(name.split("_")[1]):
                    name = name.split("_")[0]

        browser2 = selopner(browser2, "https://www.chess.com/members/view/%s#usernotes_post" %mem)
        time.sleep(interval)
        counter = 1

        while True:
            try:
                browser2.find_element_by_name("c23").send_keys(streplacer(msg, (["/name", name.strip()], ["/firstname", name.split(" ")[0]], ["/nation", country.strip()])))
                browser2.find_element_by_name("c24").click()
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                    debugout()
                if counter == 20:
                    print "\n\n%sSkipped %s\n\n" %(ltime(), mem)
                    skipped.append(mem)
                    break
                counter += 1
                time.sleep(2)

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

    if len(skipped) != 0:
        print "skipped the following members:"
        for name in skipped:
            print name,
        print "\n"
    browser2.quit()

    if shutdown == "y":
        turnofcomp()

def msgcomfix(msg):
    msg = msg.split(" ")
    for i in range(len(msg)):
        if "/" in msg[i]:
            if "/name" in msg[i] or "/firstname" in msg[i] or "/nation" in msg[i] or "/newline" in msg[i] or "http://" in msg[i] or "https://" in msg[i]:
                continue

            unsupCmd = ""
            while unsupCmd not in (["y", "n"]):
                unsupCmd = raw_input("\n\n\n%s is not a recognised command, do you wish to replace it? (y/n) " %msg[i])

            if unsupCmd == "y":
                while unsupCmd not in ([1, 2, 3, 4]):
                    unsupCmd = enterint("\nWhat would you like to replace it with?\n 1. /name - members name or username (if name is unavailable)\n 2. /firstname - member first name or username (if no name is available)\n 3. /nation - members nation of origin\n 4. /newline - pagebreak\nYour choice: ")

                if unsupCmd == 1:
                    print "\n\nReplaced %s with /name\n\n" %msg[i]
                    msg[i] = "/name"
                elif unsupCmd == 2:
                    print "\n\nReplaced %s with /firstname\n\n" %msg[i]
                    msg[i] = "/firstname"
                elif unsupCmd == 3:
                    print "\n\nReplaced %s with /nation\n\n" %msg[i]
                    msg[i] = "/nation"
                elif unsupCmd == 4:
                    print "\n\nReplaced %s with /newline\n\n" %msg[i]
                    msg[i] = "/newline"

    return " ".join(msg)

def pmdriver(target, choice):
    while "" in target:
        target.remove("")
    print "\n\n\n\nsupported commands, will be replaced with each members respective info\n /name - members name or username (if name is unavailable)\n /firstname - member first name or username (if no name is available)\n /nation - members nation of origin\n /newline - pagebreak\n\n\n"
    subjectorg = raw_input("subject line: ")
    msglist = list()

    msgchoice = ""
    while msgchoice not in (["1", "2"]):
        msgchoice = raw_input("\nGet the message from\n 1. File in the Data/Messages folder\n 2. Input\nEnter choice: ")

    if msgchoice == "1":
        msgfile = raw_input("\nName of the file containing your invites message: ")
        msglist = fileopen("Data/Messages/%s" %msgfile, True)

    elif msgchoice == "2":
        choicepm = "y"
        while choicepm == "y":
            while choicepm not in(["1", "2", "3"]):
                choicepm = raw_input("\n\nAdd a snippet containing\n 1. Text\n 2. Image\n 3. Youtube Video\nYour choice: ")
            if choicepm == "1":
                text = msgcomfix(raw_input("Enter the text: "))
            elif choicepm == "2":
                text = raw_input("Enter url of the image: ")
            elif choicepm == "3":
                text = raw_input("Enter url of the video: ")
            msglist.append((choicepm, text))

            while choicepm not in (["y", "n"]):
                choicepm = raw_input("add another snippet? (y/n) ")

    msgstr = u""
    msglistold = list()
    for content in msglist:
        if content[0] == "1":
            msglistold.append(content)
            msgstr = "%s%s" %(msgstr, content[1])
        elif content[0] == "2":
            msglistold.append(content)
            msgstr = '%s<img src="%s" />' %(msgstr, content[1])
        elif content[0] == "3":
            cont = content[1]
            msgstr = '%s<iframe width="640" height="360" src="//www.youtube.com/embed/%s?rel=0" frameborder="0" allowfullscreen></iframe>' %(msgstr, cont[cont.index("atch?v=") + 7:])

    msglist = msglistold
    del msglistold

    nnation = raw_input("If member nation is International, use this instead: ")

    while True:
        sleeptime = raw_input("\n\nSeconds to wait between pm's: ")
        try:
            sleeptime = int(sleeptime)
            break
        except ValueError:
            None

    browserchoice = selbrowch()

    shutdown = ""
    while shutdown not in (["y", "n"]):
        shutdown = raw_input("\n\nShut down computer when complete (might require elevated privileges)? (y/n) ")

    choice2 = ""
    while choice2 not in (["y", "n"]):
        choice2 = raw_input("\nSort out those who dont fill a few requirements? (y/n) ")

    noadmins = ""
    if choice == "1":
        while noadmins not in (["y", "n"]):
            noadmins = raw_input("\nInclude admins? (y/n) ")

    Username, Password = usrPas()

    browser0, handle = pickbrowser(browserchoice, True)
    browser0 = sellogin(Username, Password, browser0)

    logincookie = browser0.get_cookies()
    browser1 = mecbrowser(logincookie)

    if choice == "1":
        memtpm = memspider(target, False, browser1)
        if noadmins == "n":
            superadmins, admins = getadmins(getgrouphome(target, browser1), browser1)
            memtpm = memtpm.difference(superadmins + admins)

    elif choice == "2":
        memtpm = target

    if choice2 == "y":
        minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat = memprmenu()

    print "\n\n"

    counter = 1
    for membername2 in memtpm:
        if membername2 == "":
            continue
        membername = "https://www.chess.com/members/view/%s" %membername2

        while True:
            try:
                browser1, response = mecopner(browser1, membername)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        if supusr:
            debugout()

        if choice2 == "y":
            if not memberprocesser(soup, membername2, minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat):
                if supusr:
                    print "\t%s Didnt pass filter" %membername2
                continue

        else:
            if membername2 not in str(soup):
                if supusr:
                    print "\t%s doesnt exist" %membername2
                continue

        if browserchoice == "1":
            counter += 1
            if counter > 90:
                browser0.quit()
                browser0, handle = pickbrowser(browserchoice, True)
                browser0 = sellogin(Username, Password, browser0)
                counter = 1

        print "%ssending pm to %s" %(ltime(), membername2)

        if not membername2 in str(soup):
            print "\n\n%sFailed to open page and skipped, %s\n\n" %(ltime(), membername)
            continue

        for placeholder in soup.find_all(class_ = "flag"):
            country = placeholder["title"]

        if country == "International":
            country = nnation

        name = namechecker(soup)
        if name == " ":
            name = membername2

            if "_" in name:
                if isint(name.split("_")[1]):
                    name = name.split("_")[0]

        subject = streplacer(subjectorg, (["/name", name.strip()], ["/firstname", name.split(" ")[0]], ["/nation", country.strip()], ["/newline", "\n"]))

        for link in soup.find_all("a", href = True):
            if link.text == "Send a Message":
                memlink = link["href"]
                browser0 = selopner(browser0, "https://www.chess.com%s" %memlink)
                time.sleep(2)

        try:
            WebDriverWait(browser0, 10).until(EC.presence_of_element_located((By.ID, "c15")))
            browser0.find_element_by_name("c15").send_keys(subject)

        except Exception, errormsg:
            if supusr:
                print repr(errormsg)
                debugout()
            continue

        while True:
            try:
                browser0.switch_to_frame("tinymcewindow_ifr")
                browser0.find_element_by_id("tinymce").clear()
                browser0.switch_to_default_content()

                try:
                    filtmcemsg(msgstr, browser0, name, country, browserchoice)
                except:
                    filtmcemsgold(msglist, browser0, name, country, browserchoice)

                browser0.find_element_by_id("c16").click()
                break

            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                    debugout()
                print "\n\n%sRetrying %s" %(ltime(), membername2)

                while True:
                    browser0 = selopner(browser0, "https://www.chess.com%s" %memlink)

                    try:
                        WebDriverWait(browser0, 10).until(EC.presence_of_element_located((By.ID, "c15")))
                        browser0.find_element_by_name("c15").send_keys(subject)
                        break
                    except Exception, errormsg:
                        if supusr:
                            print repr(errormsg)
                            debugout()
                        print "%sretrying" %ltime()

        soup.decompose()
        response.close()
        browser1.clear_history()
        gc.collect()
        time.sleep(sleeptime)

    browser0.quit()

    if shutdown == "y":
        turnofcomp()

def mecopner(browser, pointl):
    while True:
        try:
            if supusr:
                print "\tAttemting to open '%s'" %pointl

            response = browser.open(pointl, timeout = 12.0)

            if supusr:
                print "\tSuccessfully opened page"

            return browser, response

        except Exception, errormsg:
            if supusr:
                print repr(errormsg)
                debugout()

            print "%ssomething went wrong, reopening %s" %(ltime(), pointl)
            time.sleep(1.5)

def nineworker(infile, inid, browser, key):
    memlist = list()
    target = list()
    memlistorg = memfiop(infile, key)

    for counter in range(1, 101):
        target.append("https://www.chess.com/groups/managemembers?id=%s&page=%i" %(inid, counter))

    un = sorted(memspider([target], True, browser))

    for member in memlistorg:
        if member not in un:
            memlist.append(member)

    if len(memlist) != 0:
        memlist = notclosedcheck(memlist, browser)

    with open(infile, "wb") as placeholder:
        placeholder.write(com2(key, str(un).replace("'", "").replace("[", "").replace("]", ""), 256, []))
    return memlist, len(un), len(memlistorg)

def getTmTimouts(browser, groupname, tmpage):
    while True:
        try:
            browser, response = mecopner(browser, tmpage)
            soup = BeautifulSoup(response)
            break
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)
            time.sleep(1)

    soupgroup = re.findall("/groups/home/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all(class_ = "default border-top alternate")))

    soup = soup.find_all("tr")
    timeouters = []

    try:
        if groupname == str(soupgroup[0]).replace("/groups/home/", ""):
            for placeholder in soup:
                placeholder = str(placeholder)

                if "menu-icons timeline right-8" in placeholder:
                    timeouts = placeholder.count('class="menu-icons timeline right-8" title="Timeout"')
                    timeouter = str(re.findall("https://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)[0]).replace("https://www.chess.com/members/view/", "")
                    timeouters.append([tmpage, timeouter, str(timeouts)])

        elif groupname == str(soupgroup[1]).replace("/groups/home/", ""):
            for placeholder in soup:
                placeholder = str(placeholder)

                if "menu-icons timeline left-8" in placeholder:
                    timeouts = placeholder.count('class="menu-icons timeline left-8" title="Timeout"')
                    timeouter = str(re.findall("https://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)[3]).replace("https://www.chess.com/members/view/", "")
                    timeouters.append([tmpage, timeouter, str(timeouts)])

        else:
            sys.exit("\n\n%sfailed to find your group!!!\n" %ltime())
    except IndexError, errormsg:
        if supusr:
            print repr(errormsg)
    return timeouters

def getTmParticipants(browser, targetURL):
    lineup1 = list()
    lineup2 = list()

    team1 = True
    team2 = False

    count = 0

    while True:
        try:
            browser, response = mecopner(browser, targetURL)
            soup = BeautifulSoup(response)
            break
        except Exception, errormsg:
            if supusr:
                    print repr(errormsg)
            time.sleep(1)
    souppar = soup.find_all(class_ = "align-left")

    group1, group2 = re.findall("/groups/home/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all(class_ = "default border-top alternate")))
    group1 = group1[13:].replace("-", " ")
    group2 = group2[13:].replace("-", " ")

    for x in souppar:
        x = x.text
        if x == "":
            continue
        if "Waiting" in x or "Ready!" in x:
            break

        if x.strip() == "":
            count += 1
            continue

        if count >= 2:
            team2 = True
            team1 = False

        if x == "vs.":
            team1 = False
            continue

        x = streplacer(x, (["(", ""], [")", ""])).split(" ")[1:]
        if x[1] == "Unrated":
            x[1] = 1200

        if team1:
            lineup1.append(x)
            count = 0
            if supusr:
                print "%s added to %s's lineup" %(x[0], group1)
        else:
            lineup2.append(x)
            if supusr:
                print "%s added to %s's lineup" %(x[0], group2)
            if not team2:
                team1 = True

    return group1, lineup1, group2, lineup2

def tmparchecker(browser, pagelist, targetname):
    tmyear = enterint("\nOnly check tm's that has been open for registration since year, leave empty to skip (YYYY) ")
    if tmyear != "":
        tmmonth = enterint("\nOnly check tm's that has been open for registration since month (MM) ")
        tmday = enterint("\nOnly check tm's that has been open for registration since day (DD) ")

    tmpar = list()
    timeoutlist = list()
    winssdic = dict()
    losedic = dict()
    print "\n\n"

    for page in pagelist:
        if "https://www.chess.com/groups/team_match?id=" not in page:
            continue
        print "%sprocessing: %s" %(ltime(), page)

        if supusr:
            debugout()

        alltmresults = list()
        counter2 = 0
        while True:
            try:
                browser, response = mecopner(browser, page)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        if tmyear != "":
            regopen = soup.find_all(class_ = "simple border-top clearfix alternate")
            for x in regopen:
                regopen = x.text
            regopen = regopen.strip().split("\n")
            regopen = regopen[regopen.index("Registration Open:") + 1]
            regopen = regopen.replace("Jan", "01").replace("Feb", "02").replace("Mar", "03").replace("Apr", "04").replace("May", "05").replace("Jun", "06").replace("Jul", "07").replace("Aug", "08").replace("Sep", "09").replace("Oct", "10").replace("Nov", "11").replace("Dec", "12").replace(",", "").split(" ")
            regopen = ([int(regopen[2]), int(regopen[0]), int(regopen[1])])
            print regopen
            if datetime(regopen[0], regopen[1], regopen[2]) < datetime(tmyear, tmmonth, tmday):
                print "%s%s didn't pass the timecheck" %(ltime(), page)
                continue

        soupgroup = str(soup.find_all(class_ = "default border-top alternate"))
        soupgroup = re.findall("/groups/home/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", soupgroup)

        souppar = soup.find_all(class_ = "align-left")
        souppar1 = soup.find_all("tr")
        souppar2 = soup.find_all("strong")

        for placeholder in souppar2:
            try:
                alltmresults.append(float(placeholder.text))
            except ValueError:
                alltmresults = alltmresults

        try:
            if targetname == str(soupgroup[0]).replace("/groups/home/", ""):
                for placeholder in souppar[0::4]:
                    placeholder = str(placeholder)
                    placeholder = re.findall("https://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)
                    try:
                        placeholder = str(placeholder[0]).replace("https://www.chess.com/members/view/", "")
                        tmpar.append(placeholder)

                        if placeholder in winssdic:
                            winssdic[placeholder] += alltmresults[1 + counter2]
                        else:
                            winssdic[placeholder] = alltmresults[1 + counter2]

                        if placeholder in losedic:
                            losedic[placeholder] += alltmresults[2 + counter2]
                        else:
                            losedic[placeholder] = alltmresults[2 + counter2]

                        counter2 += 2
                    except IndexError:
                        placeholder = list()

                for placeholder in souppar1:
                    placeholder = str(placeholder)

                    if "menu-icons timeline right-8" in placeholder:
                        timeouts = placeholder.count('class="menu-icons timeline right-8" title="Timeout"')
                        counter = 0
                        while counter < timeouts:
                            timeouters1 = str(re.findall("https://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)[0]).replace("https://www.chess.com/members/view/", "")
                            timeoutlist.append(timeouters1)
                            counter += 1

            elif targetname == str(soupgroup[1]).replace("/groups/home/", ""):
                for placeholder in souppar[3::4]:
                    placeholder = str(placeholder)
                    placeholder = re.findall("https://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)
                    try:
                        placeholder = str(placeholder[0]).replace("https://www.chess.com/members/view/", "")
                        tmpar.append(placeholder)

                        if placeholder in winssdic:
                            winssdic[placeholder] += alltmresults[2 + counter2]
                        else:
                            winssdic[placeholder] = alltmresults[2 + counter2]

                        if placeholder in losedic:
                            losedic[placeholder] += alltmresults[1 + counter2]
                        else:
                            losedic[placeholder] = alltmresults[1 + counter2]

                        counter2 += 2
                    except IndexError:
                        placeholder = list()

                for placeholder in souppar1:
                    placeholder = str(placeholder)

                    if "menu-icons timeline left-8" in placeholder:
                        timeouts = placeholder.count('class="menu-icons timeline left-8" title="Timeout"')
                        counter = 0

                        while counter < timeouts:
                            timeouters1 = str(re.findall("https://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)[3]).replace("https://www.chess.com/members/view/", "")
                            timeoutlist.append(timeouters1)
                            counter += 1

            else:
                print "\n\n%sfailed to find your group in this match: %s!!!\n" %(ltime(), page)

        except IndexError:
            None

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

    return tmpar, timeoutlist, winssdic, losedic

def latestTMsOnsite(browser):
    targetlst = []

    for x in xrange(1, 101):
        targetpage = "https://www.chess.com/groups/team_matches?page=%i" %x
        print "%schecking: %s" %(ltime(), targetpage)

        while True:
            try:
                browser, response = mecopner(browser, targetpage)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        counter = 1
        for content in soup.find_all("td"):
            if not '<td style="padding: 0' in str(content):
                if counter <= 4:
                    content = content.text.strip()
                    if counter == 3:
                        content = int(content)
                    counter += 1

                else:
                    content = str(content.contents[0])
                    content = "https://www.chess.com%s" %content[9: content.index('"><')]
                    counter = 1

                targetlst.append(content)

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

    return sorted(zip(*[iter(targetlst)] * 5), key = itemgetter(2), reverse = True)

def memspider(target, silent, browser):
    if not silent:
        print "\n\nTime      Page\n"
    usrlist = list()
    for tlst in target:
        for pointer in tlst:
            while True:
                try:
                    browser, response = mecopner(browser, pointer)
                    soup = BeautifulSoup(response)
                    break
                except Exception, errormsg:
                    if supusr:
                        print repr(errormsg)
                    time.sleep(1)

            if "https://www.chess.com/groups/view/" in browser.geturl():
                break

            p2 = str(soup.find_all(class_ = "next-on"))

            if not silent:
                print "%s    %s" %(ltime(), pointer)
                if supusr:
                    debugout()

            if "chess.com/tournaments/players" in pointer:
                for link in browser.links(url_regex="chess.com/tournaments/player_summary"):
                    ltext = link.text

                    if ltext != "View Profile":
                        usrlist.append(ltext.replace("[IMG]", ""))

            else:
                for link in browser.links(url_regex="chess.com/members/view/"):
                    ltext = link.text

                    if ltext != "View Profile":
                        usrlist.append(ltext.replace("[IMG]", ""))

            if "next-on" not in p2:
                break

            soup.decompose()
            response.close()
            browser.clear_history()
            gc.collect()

    return list(set(usrlist))

def ageproc(target):
    while "" in target:
        target.remove("")
    browser = mecbrowser("")

    flist = []
    for targetx in target:
        print "%schecking: %s" %(ltime(), targetx)

        if supusr:
            debugout()

        tlst = [targetx]

        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %targetx)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        if "://www.chess.com/members/view/" not in browser.geturl():
            continue

        birthdate = birthlister(soup)
        if birthdate == "":
            continue
        while "" in birthdate:
            birthdate.remove("")

        birthdate = map(int, [element.replace(",", "") for element in birthdate])
        flist.append(birthdate + tlst)

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()
    return flist

def selbrowch():
    browserchoice = ""
    while browserchoice not in (["1", "2"]):
        browserchoice = raw_input("\nWhich browser do you want to use\n 1. Firefox\n 2. Chrome\nYour choice: ")
    return browserchoice

def createfileifmissing(filename, ismsg):
    if not os.path.isfile(filename):
        if not ismsg:
            open(filename, "wb").close()
        else:
            with open(filename, "wb") as mfile:
                mfile.write("<Text>\nHello this is an example message\n<Image>\nhttp://images.chesscomfiles.com/uploads/user/10117446.a001a3bf.600x450i.a24be423b414.jpeg\n<Video>\nhttp://www.youtube.com/watch?v=GY8YBF8dHQo")

def createconfig(name, ID):
    invconpath = ".Config/Member Lists/%s.ini" %name
    if os.path.isfile(invconpath):
        membersleftinvfile = configopen(invconpath)["Members who has left invites file (optional)"]
    else:
        membersleftinvfile = "%s members who has left" %name

    with open(".Config/Invites/%s.ini" %name, "wb") as setupfile:
        setupfile.write("What to use if members nation is set to International==\nMin online chess rating==\nMax online chess rating==\nMin 960 chess rating==\nMax 960 chess rating==\nMin online chess games plaid==\nMin current online chess games==\nMin online chess win-ratio==\nLast logged in within days==\nMember on chess.com for days==\nBorn after date (YYYY-MM-DD)==\nBorn before date (YYYY-MM-DD)==\nMax timeout-ratio allowed==\nMax number of groups member can be in==\nMin number of groups member can be in==\nMin number of activity points allowed==\nMin time/move (days-hours-minutes)==\nMax time/move (days-hours-minutes)==\nOnly invite those with a custom avatar (y/n)==\nMember should be from nation==\nGender (m/f)==\nLink to groups invite members page==https://www.chess.com/groups/invite_members?id=%i\nFile containing the main invites list==Data/Invite Lists/%s\nFile containing those who should receive priority invites (circumvents filter)==Data/Invite Lists/%s priority\nInvites file for those who has left the group==Data/Invite Lists/%s\nFile containing those who has received an invite==Data/Invite Lists/%s already invited\nFile containing your invites message for members who has left your group==Data/Messages/Invite Messages/%s Deserter message\nFile containing your invites message for standard and priority invites lists==Data/Messages/Invite Messages/%s Standard Message\nComma seperated list of usernames that should not be invited==" %(ID, name, name, membersleftinvfile, name, name, name))
    createfileifmissing("Data/Messages/Invite Messages/%s Standard Message" %name, True)
    createfileifmissing("Data/Messages/Invite Messages/%s Deserter message" %name, True)
    createfileifmissing("Data/Invite Lists/%s already invited" %name, False)
    createfileifmissing("Data/Invite Lists/%s members who has left" %name, False)
    createfileifmissing("Data/Invite Lists/%s priority" %name, False)
    createfileifmissing("Data/Invite Lists/%s" %name, False)

def configopen(filename):
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as rowlist:
                condic = {}

                for line in rowlist:
                    data = line.split("==")
                    value = data[1].replace("\n", "")

                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            None

                    condic[data[0]] = value
                return condic
        else:
            sys.exit("\n\nThe file %s is empty!!!\n\n" %filename)
    else:
        sys.exit("\n\n%s doesn't exist!!!\n\n" %filename)

def getawards(soup):
    results = {"Site Awards": 0, "Tournament Trophies": 0, "Game Trophies": 0, "Fun Trophies": 0}
    awards = soup.find_all(class_ = "top-16 clear")

    for award in awards:
        award = str(award.text).strip()[0: -1].split("(")
        results[award[0][0: -1]] = int(award[1])

    return results["Site Awards"], results["Tournament Trophies"], results["Game Trophies"], results["Fun Trophies"]

def getfilelist(path, endswith):
    lst = list()
    counter = 1
    for files in os.walk(path):
        for flst in files:
            if type(flst) is list and len(flst) != 0:
                for fname in flst:
                    if fname.endswith(endswith):
                        lst.append([counter, fname])
                        counter += 1
    return lst

def usrPas():
    if os.path.isfile(".Config/.LoginCred/data.dll"):
        with open(".Config/.LoginCred/data.dll", "rb") as txt:
            Username, Password = com3("Uni2D", txt.read(), 256, []).split(" ")

        if supusr:
            print "\n\tUsername: %s\n\tPassword: %s\n" %(Username, Password)
    else:
        Username = raw_input("\n\nUsername: ")
        Password = raw_input("Password: ")

        if Username == "" or Password == "":
            return None, None

        saveData = ""
        while saveData not in (["y", "n"]):
            saveData = raw_input("\nSave login credentials for faster login on later runs? (y/n) ")

        if saveData == "y":
            with open(".Config/.LoginCred/data.dll", "wb") as txt:
                txt.write(com2("Uni2D", "%s %s" %(Username, Password), 256, []))

    return Username, Password

def filtmcemsg(msgstr, browser, name, country, browserchoice):
    msgstr = streplacer(msgstr, (["/name", name.strip()], ["/firstname", name.split(" ")[0]], ["/nation", country.strip()], ["/newline", "<br/>"]))
    
    browser.execute_script("tinyMCE.get('{0}').focus()".format("tinymcewindow"))
    browser.execute_script("tinyMCE.activeEditor.setContent('{0}')".format(msgstr))

def login():
    Username, Password = usrPas()

    if Username == None:
        return ""

    browserchoice = selbrowch()
    browser, handle = pickbrowser(browserchoice, True)
    browser = sellogin(Username, Password, browser)

    logincookie = browser.get_cookies()
    browser.quit()
    return logincookie

def readFile(filename):
    target = ""
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as placeholder:
                target = placeholder.read()
    else:
        open(filename, "wb").close()
        return []

    target = target.replace(" ", "").split(",")

    return target

def readFile2(filename):
    target = []
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as placeholder:
                for line in placeholder.readlines():
                    if line != "\n":
                        target.append(streplacer(line, (["\n", ""], [" ", ""])))
    else:
        open(filename, "wb").close()

    return list(set(target))

def balancetm(lineup1, lineup2, ratingrange):
    mem_i = 0
    offset = 0
    pairs = []

    for player in lineup1:
        oldif = 4000

        for i in range(mem_i, len(lineup2)):
            ratingdif = abs(int(player[1]) - int(lineup2[i][1]))
            if ratingrange >= ratingdif:

                if i != len(lineup2) - 1:
                    if ratingrange < abs(int(player[1]) - int(lineup2[i + 1][1])):

                        pairs.append([player, lineup2[i]])
                        del lineup2[i]
                        offset += ratingdif
                        mem_i = i
                        break

                if ratingdif >= oldif:
                    pairs.append([player, lineup2[i - 1]])
                    del lineup2[i-1]
                    oldif = ratingdif
                    offset += ratingdif
                    mem_i = i
                    break

                else:
                    oldif = ratingdif

    return pairs, offset

def evenpairing(lst1, lst2):
    playlst = list()
    for player1 in lst1[:]:
        player2 = min(lst2, key=lambda x: abs(x[1] - player1[1]))
        playlst.append([player1, player2])

        lst1.remove(player1)
        lst2.remove(player2)
    return playlst

def remcomelem(lst1, lst2):
    for elem in lst1[:]:
        if elem in lst2:
            lst1.remove(elem)
            lst2.remove(elem)
    return lst1, lst2

def pairsorter(browser, target, choice):
    partup = list()
    for mem in target:
        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %mem)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        if supusr:
            debugout()

        if "://www.chess.com/members/view/" not in browser.geturl():
            continue

        if choice == "1":
            rating = lstanratingchecker(soup)
        elif choice == "2":
            rating = lbulratingchecker(soup)
        elif choice == "3":
            rating = lblitzratingchecker(soup)
        elif choice == "4":
            rating = onlratingchecker(soup)
        elif choice == "5":
            rating = ranratingchecker(soup)
        elif choice == "6":
            rating = tacratingchecker(soup)

        partup.append([mem, int(rating)])

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()
    return sorted(partup, reverse = True, key = lambda tup: tup[1])

def olprint(startc, endc, inchar, endn, nline):
    sys.stdout.write(startc)
    for x in range(endn):
        sys.stdout.write(inchar)
    sys.stdout.write(endc)
    sys.stdout.flush()
    if nline:
        print ""

def enterint(text):
    while True:
        number = raw_input(text)
        if number == "":
            return number
        try:
            number = int(number)
            return number
        except ValueError:
            print "\n\nInvalid input, try again\n\n"

def notesfriendscheck(tocheck, checkfor, choice):
    present = list()
    notpresent = list()
    targetdic = dict()

    for member in tocheck:
        templst = list()
        if choice == "1":
            for count in xrange(1, 101):
                templst.append("https://www.chess.com/members/notes/%s?page=%i" %(member, count))
        elif choice == "2":
            for count in xrange(1, 101):
                templst.append("https://www.chess.com/home/friends?username=%s&general=&name=&country=&sortby=alphabetical&page=%i" %(member, count))

        targetdic[member] = templst

    logincookie = login()
    browser = mecbrowser(logincookie)

    for member, target in targetdic.items():
        notfriends = True
        friends = memspider([target], False, browser)

        for mem in friends:
            if mem.lower() == checkfor:
                present.append(member)
                notfriends = False
                break

        if notfriends:
            notpresent.append(member)

    return present, notpresent

def memprmenu():
    minrat = enterint("\n\nMin (online chess) rating allowed. leave empty to skip: ")
    maxrat = enterint("Max (online chess) rating allowed. leave empty to skip: ")
    minranrat = enterint("Min (960) rating allowed. leave empty to skip: ")
    maxranrat = enterint("Max (960) rating allowed. leave empty to skip: ")
    mingames = enterint("\nMin number of games played (online chess). leave empty to skip : ")
    mincurrent = enterint("Min number of currently ongoing games (online chess). leave empty to skip : ")
    minwinrat = raw_input("Min win-ratio (online chess). leave empty to skip : ")

    lastloginyear = enterint("\nLast logged in year. leave empty to skip (YYYY): ")
    if lastloginyear != "":
        lastloginmonth = enterint("Last logged in month (MM): ")
        lastloginday = enterint("Last logged in day (DD): ")
    else:
        lastloginmonth = ""
        lastloginday = ""

    membersinceyear = enterint("\nMember since before year. leave empty to skip (YYYY): ")
    if membersinceyear != "":
        membersincemonth = enterint("Member since before month (MM): ")
        membersinceday = enterint("Member since before day (DD): ")
    else:
        membersincemonth = ""
        membersinceday = ""

    youngeryear = enterint("\nBorn after year. leave empty to skip (YYYY): ")
    if youngeryear != "":
        youngermonth = enterint("Born after month (MM): ")
        youngerday = enterint("Born after day (DD): ")
    else:
        youngermonth = ""
        youngerday = ""

    olderyear = enterint("\nBorn before year. leave empty to skip (YYYY): ")
    if olderyear != "":
        oldermonth = enterint("Born before month (MM): ")
        olderday = enterint("Born before day (DD): ")
    else:
        oldermonth = ""
        olderday = ""

    timemax = enterint("\nMax timeoutratio allowed. leave empty to skip: ")
    timemin = enterint("\nMin timeoutratio allowed. leave empty to skip: ")
    maxgroup = enterint("\nMax number of groups member may be in. leave empty to skip: ")
    mingroup = enterint("Min number of groups member may be in. leave empty to skip: ")
    minpoints = enterint("Min number of activity points member may have. leave empty to skip: ")

    timovchoicemin = raw_input("\nTime/move higher than (format: days - hours - minutes, leave empty to skip) ")
    timovchoicemax = raw_input("Time/move lower than (format: days - hours - minutes, leave empty to skip) ")
    if timovchoicemax != "":
        timovchoicemax = [int(elem) for elem in timovchoicemax.split("-")]
    if timovchoicemin != "":
        timovchoicemin = [int(elem) for elem in timovchoicemin.split("-")]

    avatarch = ""
    while avatarch not in (["y", "n"]):
        avatarch = raw_input("\nSort out those who don't have a custom avatar? (y/n) ")

    heritage = raw_input("\nMember should be from. leave empty to skip: ")

    memgender = "a"
    while memgender not in (["m", "f", ""]):
        memgender = raw_input("\nMember should be gender (determined by comparing member name to a list of male and female names). leave empty to skip (m/f): ")
    return minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat

def makefolder(flst):
    for folder in flst:
        if not os.path.exists(folder):
            os.makedirs(folder)

def gettmlinklist(targetname, browser):
    linklist = list()

    while True:
        try:
            browser, response = mecopner(browser, "https://www.chess.com/groups/matches/%s?show_all_current=1" %targetname)
            soup = BeautifulSoup(response)
            break
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)
            time.sleep(1)

    souplinks = re.findall("/groups/team_match(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))
    for link in souplinks:
        linklist.append("https://www.chess.com%s" %link)

    if len(linklist) == 0:
        print "\n\n\t Invalid group name!!!\n\n"
        sys.exit()

    for pointer in range(3):
        del linklist[-1]

    soup.decompose()
    response.close()
    browser.clear_history()
    gc.collect()

    return linklist

def selopner(browser, pointl):
    while True:
        try:
            browser.get(pointl)
            return browser
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)
                debugout()

            print "%ssomething went wrong, reopening %s" %(ltime(), pointl)
            time.sleep(2)

def sellogin(Username, Password, browser):
    while True:
        browser = selopner(browser, "https://www.chess.com/login")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "btnLogin")))

        browser.find_element_by_name("c1").send_keys(Username)
        browser.find_element_by_name("loginpassword").send_keys(Password)

        browser.find_element_by_id("btnLogin").click()
        time.sleep(4)

        if "https://www.chess.com/home/" in browser.current_url:
            return browser

def olprint2(tlen, middle, right, left):
    print right,
    print tlen.format(middle),
    print left

def isint(number):
    try:
        number = int(number)
        return True
    except ValueError:
        return False

def ingroupcheck(browser, member, group):
    for pagenum in range(1, 101, 1):
        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/groups/mygroups?username=%s&page=%i" %(member, pagenum))
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        for x in soup.find_all(class_ = "bottom-8"):
            if group == x.text:
                return True

        if "next-on" not in str(soup.find_all(class_ = "next-on")):
            break

    return False

def inviter(targetlist, endless):
    invitenum = 140
    browserchoice = selbrowch()
    Username, Password = usrPas()
    browser2, handle = pickbrowser(browserchoice, True)
    browser2 = sellogin(Username, Password, browser2)
    logincookie = browser2.get_cookies()
    browser1 = mecbrowser(logincookie)

    redo = True
    counter = 1
    while redo == True:
        if not endless:
            redo = False

        for target in targetlist:
            target = target[1]

            invgroup = target[0:-4]
            if browserchoice == "1":
                counter += 1
                counted = "y"
                if counter > 90:
                    browser2.quit()
                    browser2, handle = pickbrowser(browserchoice, True)
                    browser2 = sellogin(Username, Password, browser2)
                    counter = 1

            condic = configopen(".Config/Invites/%s" %target)
            invitenum2 = invitenum
            memint = list()

            countryalt = condic["What to use if members nation is set to International"]
            if countryalt == "":
                countryalt = "International territory"
            minrat = condic["Min online chess rating"]
            maxrat = condic["Max online chess rating"]
            minranrat = condic["Min 960 chess rating"]
            maxranrat = condic["Max 960 chess rating"]
            mingames = condic["Min online chess games plaid"]
            try:
                mincurrent = condic["Min current online chess games=="]
            except:
                if supusr:
                    print "\n\nPlease add the line 'Min current online chess games==' to your invites config file(s)\n\n"
                mincurrent = ""
            minwinrat = condic["Min online chess win-ratio"]
            lastlogin = condic["Last logged in within days"]
            if lastlogin != "":
                lonl = [int(elem) for elem in str(date.today() - timedelta(days = lastlogin)).split("-")]
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
            else:
                lastloginyear = ""
                lastloginmonth = ""
                lastloginday = ""
            membersince = condic["Member on chess.com for days"]
            if membersince != "":
                msin = [int(elem) for elem in str(date.today() - timedelta(days = membersince)).split("-")]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
            else:
                membersinceyear = ""
                membersincemonth = ""
                membersinceday = ""
            youngerthan = condic["Born after date (YYYY-MM-DD)"]
            if youngerthan != "":
                youngerthan = youngerthan.split("-")
                youngeryear = int(youngerthan[0])
                youngermonth = int(youngerthan[1])
                youngerday = int(youngerthan[2])
            else:
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
            olderthan = condic["Born before date (YYYY-MM-DD)"]
            if olderthan != "":
                olderthan = olderthan.split("-")
                olderyear = int(olderthan[0])
                oldermonth = int(olderthan[1])
                olderday = int(olderthan[2])
            else:
                olderyear = ""
                oldermonth = ""
                olderday = ""
            timemax = condic["Max timeout-ratio allowed"]
            timemin = ""
            maxgroup = condic["Max number of groups member can be in"]
            mingroup = condic["Min number of groups member can be in"]
            minpoints = condic["Min number of activity points allowed"]
            timovchoicemin = condic["Min time/move (days-hours-minutes)"]
            timovchoicemax = condic["Max time/move (days-hours-minutes)"]
            avatarch = condic["Only invite those with a custom avatar (y/n)"]
            heritage = condic["Member should be from nation"]
            memgender = condic["Gender (m/f)"]
            groupinv = condic["Link to groups invite members page"]
            infile = condic["File containing the main invites list"]
            priofile = condic["File containing those who should receive priority invites (circumvents filter)"]
            leftfile = condic["Invites file for those who has left the group"]
            alrfile = condic["File containing those who has received an invite"]
            msglistleft = condic["File containing your invites message for members who has left your group"]
            msgliststand = condic["File containing your invites message for standard and priority invites lists"]

            notToInvite = condic["Comma seperated list of usernames that should not be invited"].replace(" ", "").split(",")

            memalrinv = readFile2(alrfile)

            usedfile = priofile
            memtinv = readFile2(priofile)
            priolst = True
            deserterlst = False
            standardlst = False

            if len(memtinv) == 0:
                memtinv = readFile2(leftfile)
                deserterlst = True
                priolst = False
                usedfile = leftfile

            if len(memtinv) == 0:
                memtinv = readFile2(infile)
                usedfile = infile
                memtinv = [x for x in memtinv if x not in memalrinv]
                standardlst = True
                invfilter = True
                deserterlst = False

            if len(memtinv) == 0:
                print "\n\n%sWarning, empty invites list: %s" %(ltime(), infile)
                continue

            if priolst == True or standardlst == True:
                msglist = fileopen(msgliststand, True)
            elif deserterlst:
                msglist = fileopen(msglistleft, True)

            msgstr = u""
            for content in msglist:
                if content[0] == "1":
                    msgstr = "%s%s" %(msgstr, content[1])
                elif content[0] == "2":
                    msgstr = '%s<img src="%s" />' %(msgstr, content[1])
                elif content[0] == "3":
                    cont = content[1]
                    msgstr = '%s<iframe width="640" height="360" src="//www.youtube.com/embed/%s?rel=0" frameborder="0" allowfullscreen></iframe>' %(msgstr, cont[cont.index("atch?v=") + 7:])

            already_picked = list()
            if invitenum2 > len(memtinv):
                invitenum2 = len(memtinv)

            while len(already_picked) < invitenum2:
                picked = random.choice(memtinv)

                if not picked in already_picked:
                    already_picked.append(picked)

            if supusr:
                print "\n\nMembers to invite for %s: %s\n\n" %(invgroup, ", ".join(already_picked))

            for member in already_picked:
                if supusr:
                    print "\n\tMember: '%s' for '%s'" %(member, invgroup)
                if member in notToInvite:
                    memtinv.remove(member)
                    if supusr:
                        print "\tRemoved as per config file"
                    continue

                while True:
                    try:
                        browser1, response = mecopner(browser1, "https://www.chess.com/members/view/%s" %member)
                        soup = BeautifulSoup(response)
                        break
                    except Exception, errormsg:
                        if supusr:
                            print repr(errormsg)
                        time.sleep(1)

                if supusr:
                    debugout()

                if standardlst:
                    try:
                        if not memberprocesser(soup, member, minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat):
                            try:
                                memtinv.remove(member)
                                if supusr:
                                    print "\tDidnt pass filter"

                            except Exception, errormsg:
                                print repr(errormsg)
                                print "member: '%s'" %member
                                print ([member])
                                print "passmem: '%s'" %passmemfil
                                sys.exit("Send above to the developer!!!")
                            continue

                    except UnboundLocalError:
                        if supusr:
                            print "\tFailed filter check"
                        continue

                    if supusr:
                        print "\tPassed filter"

                else:
                    if member not in str(soup):
                        memtinv.remove(member)
                        continue

                if browserchoice == "1":
                    if counted == "y":
                        counted = ""

                    else:
                        counter += 1

                    if counter > 90:
                        browser2.quit()
                        browser2, handle = pickbrowser(browserchoice, True)
                        browser2 = sellogin(Username, Password, browser2)
                        counter = 1

                for placeholder in soup.find_all(class_ = "flag"):
                    country = placeholder["title"]
                if country == "International":
                    country = countryalt

                name = namechecker(soup)

                soup.decompose()
                response.close()
                browser1.clear_history()
                gc.collect()

                if name == " ":
                    name = member

                    if "_" in name:
                        if isint(name.split("_")[1]):
                            name = name.split("_")[0]

                browser2 = selopner(browser2, groupinv)

                try:
                    WebDriverWait(browser2, 5).until(EC.presence_of_element_located((By.ID, "c15")))
                    browser2.find_element_by_name("c15").send_keys(member)
                except:
                    if supusr:
                        print "No invites available, continuing to next group"
                    break

                while True:
                    try:
                        print "\n%sInviting %s to %s" %(ltime(), member, invgroup)

                        browser2.switch_to_frame("tinymcewindow_ifr")
                        browser2.find_element_by_id("tinymce").clear()
                        browser2.switch_to_default_content()

                        try:
                            if supusr:
                                print "attempting to fill out invites message"
                            filtmcemsg(msgstr, browser2, name, country, browserchoice)
                        except:
                            if supusr:
                                print "failed to set content, reversing to back up method"
                            filtmcemsgold(msglist, browser2, name, country, browserchoice)

                        browser2.find_element_by_id("c18").click()
                        if supusr:
                            print "Invite sent!"
                        memint.append(member)
                        time.sleep(0.1)
                        break

                    except Exception, errormsg:
                        if supusr:
                            print repr(errormsg)
                            debugout()

                        print "\n\n%sRetrying %s to %s!!!\n\n" %(ltime(), member, invgroup)

                        browser2 = selopner(browser2, groupinv)

                        try:
                            WebDriverWait(browser2, 5).until(EC.presence_of_element_located((By.ID, "c15")))
                            browser2.find_element_by_name("c15").send_keys(member)

                        except Exception, errormsg:
                            if supusr:
                                print repr(errormsg)
                                debugout()
                            break

            updinvlist = set(memtinv).difference(set(memint))

            with open(usedfile, "wb") as placeholder2:
                placeholder2.write("\n".join(updinvlist))

            if len(memint) != 0:
                with open(alrfile, "ab") as placeholder3:
                    placeholder3.write("\n%s" %"\n".join(memint))

    browser2.quit()

def filtmcemsgold(msglist, browser, name, country, browserchoice):
    for content in msglist:
        if content[0] == "1":
            browser.switch_to_frame("tinymcewindow_ifr")

            browser.find_element_by_id("tinymce").send_keys(streplacer(content[1], (["/name", name.strip()], ["/firstname", name.split(" ")[0]], ["/nation", country.strip()], ["/newline", "\n"])))
            browser.switch_to_default_content()

        elif content[0] == "2":
            browser.find_element_by_id("tinymcewindow_imageuploader").click()
            time.sleep(1)
            browser.switch_to_window(browser.window_handles[1])

            while True:
                try:
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "photourl")))
                    browser.find_element_by_id("photourl").send_keys(content[1])
                    browser.find_element_by_id("insert").click()
                    break

                except Exception, errormsg:
                    if supusr:
                        print repr(errormsg)
                        debugout()
                    print "\n\n%srefreshing page\n\n" %ltime()
                    browser.refresh()

            browser.switch_to_window(browser.window_handles[0])
            time.sleep(1)

        elif content[0] == "3":
            browser.find_element_by_id("tinymcewindow_mce_media").click()
            alert = browser.switch_to_alert()
            alert.send_keys(content[1])
            alert.accept()
            time.sleep(1)

def tryCookie(logincookie):
    browser = mecbrowser(logincookie)
    browser, response = mecopner(browser, "https://www.chess.com/messages")
    currentURL = response.geturl()

    response.close()
    browser.clear_history()
    browser.close()
    gc.collect()

    if "www.chess.com/login" in currentURL:
        if supusr:
            print "\tInvalid login cookie\n\t%s\n" %currentURL
        return False
    else:
        if supusr:
            print "\tValid login cookie\n\t%s\n" %currentURL
        return True

def vcman(vclinklist, yourside):
    numgames = len(vclinklist)
    Username, Password = usrPas()
    browserchoice = selbrowch()
    browser3, handle = pickbrowser(browserchoice, True)
    browser3 = sellogin(Username, Password, browser3)

    logincookie = browser3.get_cookies()
    browser1 = mecbrowser(logincookie)

    parmemvc = Counter()
    oldnames = ([yourside])

    for vcmatch in vclinklist:
        print "\n\n%sChecking match number %i of %i\n\n" %(ltime(), vclinklist.index(vcmatch), numgames)
        skipmatch = False
        counter = 0
        movelist = list()

        while True:
            try:
                browser3 = selopner(browser3, vcmatch)
                WebDriverWait(browser3, 10).until(EC.presence_of_element_located((By.ID, "c33")))
                break

            except:
                counter += 1
                if counter == 15:
                    skipmatch = True
                    break
                print "\n\n%sReopening %s\n\n" %(ltime(), vcmatch)

        if skipmatch:
            print"\n\n\n%sFailed to load page and therefore skipped the match, %s\n\n\n" %(ltime(), vcmatch)
            continue

        browser3.find_element_by_id("c33").click()
        time.sleep(2)

        while True:
            try:
                browser1, response = mecopner(browser1, vcmatch)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        if '      initialSetup: "",' not in str(soup):
            print "\n\n\n%sskipped %s\n\n\n" %(ltime(), vcmatch)
            continue

        boardpos = str(re.findall("boardFlip: (?:[a-zA-Z]|(?:%[a-fA-F]))+", str(soup.find_all(class_ = "chess_viewer")))[0]).replace("boardFlip: ", "")
        yourpos = soup.find_all(class_ = "playername")
        yourpos = (str(yourpos[0]).replace('<span class="playername">', "").replace("</span>", ""), str(yourpos[1]).replace('<span class="playername">', "").replace("</span>", ""))

        vcelem = browser3.find_elements_by_partial_link_text('')

        while yourside not in yourpos:

            if yourpos[0] in oldnames:
                yourside = yourpos[0]
            elif yourpos[1] in oldnames:
                yourside = yourpos[1]

            else:
                yoursidechoice = ""
                while yoursidechoice not in (["1", "2"]):
                    yoursidechoice = raw_input("\n\nCan't find your group in one of the games. Please specify which group is yours\n  1. %s\n  2. %s\nYour group is number: " %(yourpos[0], yourpos[1]))

                    if yoursidechoice == "1":
                        yourside = yourpos[0]
                    if yoursidechoice == "2":
                        yourside = yourpos[1]
                    oldnames.append(yourside)

        if boardpos == "false":
            if str(yourpos[0]).replace('<span class="playername">', "").replace("</span>", "") == yourside:
                for placeholder in vcelem:
                    currentvcmovlink = placeholder.get_attribute("href") or ""

                    if vcmatch + "&mv=" in currentvcmovlink:
                        movelist.append(currentvcmovlink)
                movelist = movelist[1::2]

            elif str(yourpos[1]).replace('<span class="playername">', "").replace("</span>", "") == yourside:
                for placeholder in vcelem:
                    currentvcmovlink = placeholder.get_attribute("href") or ""

                    if vcmatch + "&mv=" in currentvcmovlink:
                        movelist.append(currentvcmovlink)
                movelist = movelist[0::2]

        if boardpos == "true":
            if str(yourpos[1]).replace('<span class="playername">', "").replace("</span>", "") == yourside:
                for placeholder in vcelem:
                    currentvcmovlink = placeholder.get_attribute("href") or ""

                    if vcmatch + "&mv=" in currentvcmovlink:
                        movelist.append(currentvcmovlink)
                movelist = movelist[1::2]

        for pointer in movelist:
            print "\n%schecking %s" %(ltime(), pointer)

            if supusr:
                debugout()

            browser1, response = mecopner(browser1, pointer)

            links1 = []
            text1 = []
            for link in browser1.links(url_regex="chess.com/members/view/"):
                ltext = link.text
                if ltext != "View Profile":
                    user = ltext.replace("[IMG]", "").strip()

                    if user == "":
                        continue
                    if user in parmemvc:
                        parmemvc[user] += 1
                    else:
                        parmemvc[user] = 1

            soup = BeautifulSoup(response)
            p2 = str(soup.find_all(class_ = "next-on"))

            if "next-on" in p2:
                browser3 = selopner(browser3, pointer)
                nextbtn = 2

                while True:
                    try:
                        browser3.find_element_by_css_selector('li.next-on>a').click()
                    except:
                        break
                    time.sleep(2)

                    print "\n%schecking %s page %i" %(ltime(), pointer, nextbtn)

                    if supusr:
                        debugout()

                    vcelem = browser3.find_elements_by_partial_link_text("")
                    for curvcparmem in vcelem:
                        memsellink = curvcparmem.get_attribute("href") or ""

                        if "https://www.chess.com/members/view/" in memsellink:
                            user = re.sub(r"^http?:\/\/.*[\r\n]*", "", memsellink.replace("https://www.chess.com/members/view/", " ")).strip()
                            if user == "":
                                continue
                            if user in parmemvc:
                                parmemvc[user] += 0.5
                            else:
                                parmemvc[user] = 0.5
                    nextbtn += 1

        soup.decompose()
        response.close()
        browser1.clear_history()
        gc.collect()

    browser3.quit()
    return parmemvc

def sendChallenge(browser, matchName, target, myGroup, tmDescription):
    browser = selopner(browser, "https://www.chess.com/groups/match_challenge")

    #print [o.text for o in Select(browser.find_element_by_id("c14")).options]
    Select(browser.find_element_by_id("c14")).select_by_visible_text(myGroup)

    browser.find_element_by_name("c16").send_keys(target)
    browser.find_element_by_name("c17").send_keys(matchName)
    browser.find_element_by_name("c18").send_keys(tmDescription)

    browser.find_element_by_id("c32").click()

def msgFix(content):
    content = streplacer(content, (["\n", ""], ["<text>", "<Text>"], ["<image>", "<Image>"], ["<video>", "<Video>"]))
    content = streplacer(content, (["<Text>", "\n<Text>\n"], ["<Image>", "\n<Image>\n"], ["<Video>", "\n<Video>\n"]))
    content = content.split("\n")

    while "" in content:
        content.remove("")

    txt = False
    img = False
    vid = False

    count = 0
    for part in content:
        if part == "<Text>":
            txt = True
            count += 1
            continue
        elif part == "<Image>":
            img = True
            count += 1
            continue
        elif part == "<Video>":
            vid = True
            count += 1
            continue

        if txt:
            txt = False

        elif img:
            part = streplacer(part, ([" ", ""], ["/newline", ""]))
            if not part[0:4] == "http":
                print "the image on line %i doesn't look like an url!" %(count + 1)

            content[count] = part
            img = False

        elif vid:
            part = streplacer(part, ([" ", ""], ["/newline", ""]))
            if not part[0:4] == "http" or "www.youtube." not in part:
                print "the video on line %i doesn't look like a youtube url!" %(count + 1)

            content[count] = part
            vid = False

        count += 1

    return content

def acceptChallenge(browser, soup, targets):
    for x in str(soup.find_all(class_ = "content left")).replace("\n", " ").split("tr class")[2:]:
        groupName = x[(x.index('</a> <a href="/groups/view/') + 27): x.index('</a></td>')].split('">')

        for data in targets:
            if data[0] in groupName:
                matchlink = "https://www.chess.com%s" %x[x.index('/groups/view_team_match_challenge?id='): x.index('"><strong>View</strong>')]
                try:
                    browser = selopner(browser, matchlink)

                    Select(browser.find_element_by_id("c1")).select_by_visible_text(data[1])

                    browser.find_element_by_id("c2").click()
                    print "%s  Accepted challenge from %s with %s\n\t  %s" %(ltime(), data[0], data[1], matchlink.replace('view_team_match_challenge', 'team_match'))

                except Exception, errormsg:
                    if supusr:
                        print repr(errormsg)
                    print "%sFailed to load %s" %(ltime(), matchlink)
                    continue

def getNewStopAt(browser, targetname):
    while True:
        try:
            browser, response = mecopner(browser, "https://www.chess.com/groups/matches/%s?show_all_current=1" %targetname)
            soup = BeautifulSoup(response)
            break
        except Exception, errormsg:
            if supusr:
                print repr(errormsg)
            time.sleep(1)
    tmarchive = re.findall("/groups/team_match_archive(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))[0]

    soup.decompose()

    while True:
        try:
            browser, response = mecopner(browser, "https://www.chess.com%s&page=1" %tmarchive)
            soup = BeautifulSoup(response)
            break
        except Exception, errormsg:
            print repr(errormsg)
            time.sleep(1)

    souplinks = re.findall("/groups/team_match(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]i|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))

    response.close()
    browser.clear_history()
    gc.collect()

    for link in souplinks:
        if "/groups/team_match?id=" in link:
            return link

def memfiop(fipath, kem):
    if os.path.isfile(fipath):
        if os.stat(fipath).st_size > 0:
            for placeholder in open(fipath, "rb"):
                mem = com3(kem, placeholder, 256, []).replace("\n", "").split(", ")
            return mem
    else:
        open(fipath, "wb").close
    return list()

def fileopen(filename, message):
    msglist = list()
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as rowlist:
                for line in rowlist:
                    msglist.append(streplacer(line, (["\n", ""], ["<Text>", "1"], ["<Image>", "2"], ["<Video>", "3"])))
        else:
            sys.exit("\n\nThe file %s is empty!!!\n\n" %filename)
    else:
        open(filename, "wb").close()
        sys.exit("\n\n%s doesn't exist, it has now been created!!!\n\n" %filename)

    if message:
        return [(msglist[counter],msglist[counter + 1]) for counter in range(0, len(msglist), 2)]
    else:
        return msglist

def memberprocesser(soup, targetx, minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat):
    try:
        if membersinceyear != "" or lastloginyear != "":
            memsinlist = memsin(soup)
            if memsinlist == "":
                return False

            if lastloginyear != "":
                lonln = memsinlist[1]
                if datetime(lonln[0], lonln[1], lonln[2]) < datetime(lastloginyear, lastloginmonth, lastloginday):
                    return False

        if timemax != "" or timemin != "":
            timeoutratio = timeoutchecker(soup)

            if timemax != "":
                if timeoutratio > timemax:
                    return False

            if timemin != "":
                if timeoutratio < timemin:
                    return False

        if timovchoicemax != "" or timovchoicemin != "":
            timemove = TimeMoveChecker(soup)

            if timovchoicemax != "":
                if timemove[0] > timovchoicemax[0]:
                    return False

                if timemove[1] > timovchoicemax[1] and timemove[0] >= timovchoicemax[0]:
                    return False

                if timemove[2] > timovchoicemax[2] and timemove[1] >= timovchoicemax[1] and timemove[0] >= timovchoicemax[0]:
                    return False

            if timovchoicemin != "":
                if timemove[0] < timovchoicemin[0]:
                    return False

                if timemove[1] < timovchoicemin[1] and timemove[0] <= timovchoicemin[0]:
                    return False

                if timemove[2] < timovchoicemin[2] and timemove[1] <= timovchoicemin[1] and timemove[0] <= timovchoicemin[0]:
                    return False

        if mingames != "" or minwinrat != "":
            gamestat = gamestats(soup)

            if mingames != "":
                if gamestat[0] < mingames:
                    return False

            if minwinrat != "":
                if gamestat[1] / gamestat[0]  < float(minwinrat):
                    return False

        if mincurrent != "":
            if currentonlinegames(soup) < mincurrent:
                return False

        if membersinceyear != "":
            memsi = memsinlist[0]

            if datetime(memsi[0], memsi[1], memsi[2]) > datetime(membersinceyear, membersincemonth, membersinceday):
                return False

        if minrat != "" or maxrat != "":
            rating = onlratingchecker(soup)

            if minrat != "":
                if rating < minrat:
                    return False

            if maxrat != "":
                if rating > maxrat:
                    return False

        if minranrat != "" or maxranrat != "":
            rating = ranratingchecker(soup)

            if minranrat != "":
                if rating < minranrat:
                    return False

            if maxranrat != "":
                if rating > maxranrat:
                    return False

        if minpoints != "":
            pts = ptscheck(soup)

            if pts < minpoints:
                return False

        if maxgroup != "" or mingroup != "":
            groupcount = groupmemlister(soup)

            if maxgroup != "":
                if groupcount > maxgroup:
                    return False

            if mingroup != "":
                if groupcount < mingroup:
                    return False

        if avatarch == "y":
            if not AvatarCheck(soup):
                return False

        if youngeryear != "" or olderyear != "":
            birthdate = birthlister(soup)

            if birthdate == "":
                return False

            while "" in birthdate:
                birthdate.remove("")

            birthdate = [int(birthdate[2]), int(birthdate[0]), int(birthdate[1])]

            if youngeryear != "":
                if datetime(birthdate[0], birthdate[1], birthdate[2]) < datetime(youngeryear, youngermonth, youngerday):
                    return False

            if olderyear != "":
                if datetime(birthdate[0], birthdate[1], birthdate[2]) > datetime(olderyear, oldermonth, olderday):
                    return False

        if heritage != "":
            nation = nationlister(soup)

            if heritage not in nation:
                return False

        if memgender != "":
            name = namechecker(soup)
            if name == " ":
                return False

            name = name.split(" ")[0].lower()
            Found = "n"

            if memgender == "f":
                with open("Data/.namelists/female", "rb") as fnlist:
                    for line in fnlist:
                        if name in line:
                            Found = "y"
                            break
            elif memgender == "m":
                with open("Data/.namelists/male", "rb") as mnlist:
                    for line in mnlist:
                        if name in line:
                            Found = "y"
                            break

            if Found == "n":
                return False

    except Exception, errormsg:
        if supusr:
            print repr(errormsg)
            debugout()
        print "\n\n%sskipped %s\n\n" %(ltime(), targetx)
        return False
    return True

def currentonlinegames(soup):
    for placeholder in soup.find_all(class_ = "section-title"):
        if "Current Games" in str(placeholder):
            return int(streplacer(placeholder.text, (["Current Games (", ""], [")", ""])).strip())

def namechecker(soup):
    for placeholder in soup.find_all("strong"):
        strplaceholder = str(placeholder)
        if "Click here" not in strplaceholder and "ChessTV" not in strplaceholder:
            return placeholder.text

def AvatarCheck(soup):
    if "noavatar" in str(soup.find_all(class_ = "avatar-container bottom-8")):
        return False
    return True

def gamestats(soup):
    for stats in soup.find_all(class_ = "even footer"):
        stats = str(stats.text).replace("Total Games:", "").strip()

        if "\n" not in stats:
            stats = streplacer(stats, (["(", ""], [")", ""], ["/", ""], ["W", ""], ["L", ""], ["D", ""])).split(" ")
            while "" in stats:
                stats.remove("")
            return [float(elem) for elem in stats]

def ptscheck(soup):
    for pts in soup.find_all(class_ = "last"):
        pts = str(pts.text)
        if "Points" in pts:
            return int(pts.replace("Points:", "").strip())

def timeoutchecker(soup):
    for placeholder in soup.find_all(class_ = "even"):
        if "Timeouts:" in str(placeholder):
            timeout = int(placeholder.text.replace("Timeouts:", "").strip().replace("% (last 90 days)", ""))
            return timeout

def TimeMoveChecker(soup):
    timemove = (["", "", ""])
    for x in soup.find_all(class_ = "odd"):
        if "Time/Move:" in str(x):
            timemov = x.text.replace("Time/Move:", "").strip().split(" ")
            timemov = [i+j for i,j in zip(timemov[::2],timemov[1::2])]
            for xx in timemov:
                if "days" in xx:
                    timemove[0] = int(xx.replace("days", ""))
                if "hr" in xx:
                    timemove[1] = int(xx.replace("hr", ""))
                if "fewmin" in xx:
                    timemove[2] = xx.replace("fewmin", "")
                elif "min" in xx:
                    timemove[2] = int(xx.replace("min", ""))
            break
    while "" in timemove:
        timemove[timemove.index("")] = 0
    return timemove

def onlratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Online Chess" in str(x):
            try:
                onrating = int(x.text.replace("Online Chess", "").strip())
            except ValueError:
                None
    return onrating

def ranratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Chess960" in str(x):
            try:
                onrating = int(x.text.replace("Chess960", "").strip())
            except ValueError:
                None
    return onrating

def tacratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Tactics" in str(x):
            try:
                onrating = int(x.text.replace("Tactics", "").strip())
            except ValueError:
                None
    return onrating

def lstanratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Live Chess - Standard" in str(x):
            try:
                onrating = int(x.text.replace("Live Chess - Standard", "").strip())
            except ValueError:
                None
    return onrating

def lbulratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Live Chess - Bullet" in str(x):
            try:
                onrating = int(x.text.replace("Live Chess - Bullet", "").strip())
            except ValueError:
                None
    return onrating

def lblitzratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Live Chess - Blitz" in str(x):
            try:
                onrating = int(x.text.replace("Live Chess - Blitz", "").strip())
            except ValueError:
                None
    return onrating

def ratingchecker(soup):
    ratinglist = list()
    recorder = "off"
    for placeholder in soup.find_all(class_ = "right"):
        if "View All Stats" in placeholder:
            recorder = "on"
        elif "Games Archive" in placeholder:
            break
        elif recorder == "on":
            try:
                ratinglist.append(int(placeholder.text))
            except ValueError:
                None
    return ratinglist

def compareOldNew(oldTuple, newTuple):
    timeoutsDictNew = {}
    timeoutsDictAlltime = {}

    for match in newTuple:
        for table in match:
            if table in oldTuple:
                continue

            indexOld = [x for x, tup in enumerate(oldTuple) if tup[0] == table[0] and tup[1] == table[1]]
            if indexOld:
                if table[1] in timeoutsDictNew:
                    timeoutsDictNew[table[1]] += 1
                else:
                    timeoutsDictNew[table[1]] = 1

                oldTuple[indexOld[0]][2] = table[2]

            else:
                if table[1] in timeoutsDictNew:
                    timeoutsDictNew[table[1]] += int(table[2])
                else:
                    timeoutsDictNew[table[1]] = int(table[2])

                oldTuple.append(table)

    return oldTuple, timeoutsDictNew

def memsin(soup):
    memsi = ""
    for placeholder in soup.find_all(class_ = "section-content section-content-2"):
        longnumlist = streplacer(placeholder.text.strip(), (["  ", ""], [",", ""], ["Member Since:", ""], ["Profile Views:", " "], ["Last Login:", " "], ["\n", ""], ["Jan", "01"], ["Feb", "02"], ["Mar", "03"], ["Apr", "04"], ["May", "05"], ["Jun", "06"], ["Jul", "07"], ["Aug", "08"], ["Sep", "09"], ["Oct", "10"], ["Nov", "11"], ["Dec", "12"])).split(" ")
        memsi = [int(longnumlist[2]), int(longnumlist[0]), int(longnumlist[1])], [int(longnumlist[5]), int(longnumlist[3]), int(longnumlist[4])]
    return memsi

def groupmemlister(soup):
    groupcountlist = list()
    for placeholder in soup.find_all(class_ = "parenthesis-link"):
        memgroups = placeholder.text
    try:
        return int(memgroups)
    except UnboundLocalError:
        return 0

def nationlister(soup):
    nationlist = list()
    for placeholder in soup.find_all(class_ = "bottom-12"):
        break
    return placeholder.text.strip()

def birthlister(soup):
    for placeholder in soup.find_all(class_ = "section-content section-content-2"):
        try:
            placeholder = [birth for birth in str(placeholder).split("\n") if "Birthday:" in birth][0]
            pos = placeholder.find("Birthday:")
            birthday = streplacer(placeholder[pos + 19: pos + 31], (["Jan", "01"], ["Feb", "02"], ["Mar", "03"], ["Apr", "04"], ["May", "05"], ["Jun", "06"], ["Jul", "07"], ["Aug", "08"], ["Sep", "09"], ["Oct", "10"], ["Nov", "11"], ["Dec", "12"])).split(" ")
        except IndexError:
            birthday = ""
    return birthday

def memremoverf(inlist, logincookie):
    targetID = str(enterint("\n\nID of the group you want to filter out: "))
    targetlist = list()
    templst = list()
    choice = ""
    while choice not in (["1", "2"]):
        choice = raw_input("\nCollect this groups memberslist from\n 1. Manage members pages (requires login)\n 2. New member pages\nEnter choice: ")

    if choice == "1":
        target = "https://www.chess.com/groups/managemembers?id=%s&page=" %targetID
        if logincookie == "":
            logincookie = login()
    elif choice == "2":
        target = "https://www.chess.com/groups/membersearch?allnew=1&id=%s&page=" %targetID

    for counter in range(1, 101):
        templst.append(target + str(counter))
    targetlist.append(templst)

    filtmem = set(memspider(targetlist, True, mecbrowser(logincookie)))
    return inlist.difference(filtmem)

def runagain():
    pathway = ""
    while pathway not in (["y", "n"]):
        pathway = raw_input("\n\n\nRun again? (y/n) ")
    return pathway

def file_or_input(mult, fdiag1, fdiag2, idiag1, idiag2):
    list1 = ""
    list2 = ""

    choice = ""
    while choice not in (["1", "2"]):
        choice = raw_input("\n\nGet the list from\n 1. Enter onscreen\n 2. Import from file in root directory\nYour choice: ")

    if choice == "2":
        print "\n\nFiles in direcroty:"
        flist = fnamenot(([".csv", ".py", ".pyc", ".log", "~"]), ".")

        while list1 not in flist:
            list1 = raw_input(fdiag1)
        list1 = readFile(list1)

        if mult:
            while list2 not in flist:
                list2 = raw_input(fdiag2)
            list2 = readFile(list2)

    elif choice == "1":
        list1 = streplacer(raw_input(idiag1), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""])).split(",")
        if mult:
            list2 = streplacer(raw_input(idiag2), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""])).split(",")

    return list1, list2

def tlstcreator():
    targetlist = list()
    choice1 = ""
    while choice1 not in (["n"]):
        tlst = list()
        url1 = raw_input("\nPaste the url here: ")

        start1 = enterint("\nEnter pagenumber to start on: ")
        if not start1 == "":
            if "&page=" in url1:
                url1 = url1[0: url1.index("&page=")]
            stop1 = enterint("\nEnter pagenumber to end on: ")

            url1 = "%s&page=" %url1
            for x in range(start1, stop1 + 1):
                tlst.append(url1 + str(x))

        else:
            tlst = [url1]
        targetlist.append(tlst)

        choice1 = ""
        while choice1 not in (["y", "n"]):
            choice1 = raw_input("\nDo you wish to process any additional targets? (y/n): ")
    return targetlist

def notclosedcheck(memlist, browser):
    memlist2 = list()

    for mem in memlist:
        while True:
            try:
                browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %mem)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)
        soupstr = str(soup)

        if mem in soupstr:
            memlist2.append(mem)

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

    return memlist2

def getgrouphome(targetlst, browser):
    grouphomelist = list()

    for target in targetlst:
        browser, response = mecopner(browser, target[0])

        for link in browser.links(url_regex="groups/home/"):
            grouphomelist.append("https://www.chess.com%s" %link.url)

        response.close()
        browser.clear_history()
        gc.collect()

    return list(set(grouphomelist))

def getadmins(targetlst, browser):
    adminlist = list()
    superadminlist = list()

    for link in targetlst:
        while True:
            try:
                browser, response = mecopner(browser, link)
                soup = BeautifulSoup(response)
                break
            except Exception, errormsg:
                if supusr:
                    print repr(errormsg)
                time.sleep(1)

        superadmins = soup.find_all(id = "c14")
        for line in str(superadmins).split("\n"):
            if '<li class="popUpMemberInfo popupTop" data-username="' in line:
                superadminlist.append(line.replace('<li class="popUpMemberInfo popupTop" data-username="', "")[0:-2])

        admins = soup.find_all(id = "c15")
        for line in str(admins).split("\n"):
            if '<li class="popUpMemberInfo popupTop" data-username="' in line:
                adminlist.append(line.replace('<li class="popUpMemberInfo popupTop" data-username="', "")[0:-2])

        soup.decompose()
        response.close()
        browser.clear_history()
        gc.collect()

    return list(set(superadminlist)), list(set(adminlist))

def ltime():
    return "%s " %time.strftime("%H:%M")

def update001():
    scriptname = os.path.basename(sys.argv[0])
    browser = mecbrowser("")

    print "\n\n%sDownloading file(s)" %ltime()

    if scriptname.endswith(".py") or scriptname.endswith(".pyc"):

        if scriptname.endswith(".pyc"):
            scriptname = scriptname[: -1]

        furl = "https://raw.githubusercontent.com/RobinKarlsson/RK-Resource-001/master/RK%20Resource%20001.py"
        browser.retrieve(furl, scriptname)[0]

    elif scriptname.endswith(".exe"):
        import zipfile

        furl = "https://www.dropbox.com/s/zsedtxhcn8ywagz/RK%20Resource%20001.zip?dl=1"
        fname = "temp.zip"
        browser.retrieve(furl, fname)[0]

        print "\n\nDownload complete. Installing..."

        with zipfile.ZipFile(fname, "r") as z:
            z.extractall()

        os.remove(fname)

    else:
        print "\n\nWARNING: Unknown file format, aborting update\n\n"
        return

    print "\n\n%sUpdate complete\n\nShutting down in:\n" %ltime()

    for timer in range(5, 0, -1):
        print timer
        time.sleep(1)

    sys.exit()

def sigstrength(template):
    if usrsys == "Linux":
        cmd = subprocess.Popen(["nm-tool"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

        for line in cmd.split("\n"):
            if "*" in line and "current AP" not in line:
                line = line.strip()

                if supusr:
                    essid = line[1: line.index(":")][:20]

                    sigfreq = line.index("Freq")
                    sigfreq = "%sHz" %line[sigfreq + 5: line.index("Hz")]

                line = [x for x in line.split()]

                sigstren = line.index("Strength")
                sigstren = "%s%%" %line[sigstren + 1]

        cmd = subprocess.Popen(["iwconfig"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

        for line in cmd.split("\n"):
            if "ESSID:" in line:
                if supusr:
                    interf = line[0: line.index(" ")].replace("ESSID:", "")[:9]

            if "Link Quality" in line:
                quality = line.strip().split("  ")
                level = quality[1].replace("Signal level=", "")
                quality = quality[0].replace("Link Quality=", "")
            else:
                quality = "n/a"
                level = "n/a"

        if not supusr:
            try:
                print template.format(ltime(), sigstren.center(15), quality.center(12), level.center(12))
            except NameError:
                print template.format(ltime(), "n/a".center(15), "n/a".center(12), "n/a".center(12))

        else:
            try:
                print template.format(ltime(), interf.center(9), essid.center(20), sigstren.center(7), quality.center(7), level.center(8), sigfreq.center(9))
            except NameError:
                print template.format(ltime(), "n/a".center(9), "No connection".center(20), "n/a".center(7), "n/a".center(7), "n/a".center(8), "n/a".center(9))

    elif usrsys == "Windows":
        signal = False
        cmd = subprocess.Popen(["netsh", "wlan", "show", "all"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

        for line in cmd[cmd.index("SHOW INTERFACES"): cmd.index("SHOW HOSTED NETWORK")].split("\n"):
            if "Signal" in line:
                sigstren = "Signal strength: %s" %sline.split()[2]

        try:
            print template.format(ltime(), sigstren.center(15))
        except NameError:
            print template.format(ltime(), "n/a".center(15))

usrsys = getplatform()[1]
supusr = False

for x in sys.argv:
    if x == "Debug":
        print "\n\n\tDebug outputs active\n\n"
        supusr = True

        try:
            import psutil
        except:
            print "\n\n\tWARNING: couldn't import psutil, RAM and CPU checks might not work properly!!!\n\n"

pathway = "y"
makefolder(([".Config", ".Config/.LoginCred", ".Config/TimeoutsCheck", ".Config/Notes Poster", ".Config/Invites", ".Config/Member Lists", "Data", "Data/.TimeoutsCheck", "Data/Invite Lists", "Data/.Member Lists", "Data/.namelists", "Data/Messages", "Data/Messages/Invite Messages", "Data/Webdriver", "Data/Webdriver/Linux", "Data/Webdriver/Mac", "Data/Webdriver/Windows", "Data/Webdriver/Linux/86", "Data/Webdriver/Linux/64", "Data/Webdriver/Mac/86", "Data/Webdriver/Windows/86", "Data/Webdriver/Extensions", "Data/Webdriver/Extensions/Chrome", "Data/Webdriver/Extensions/Firefox"]))

if os.path.isfile(".Config/.LoginCred/data.dll"):
    with open(".Config/.LoginCred/data.dll", "rb") as txt:
        usrname = ", %s" %com3("Uni2D", txt.read(), 256, []).split(" ")[0]
else:
    usrname = ""

while pathway in (["y"]):
    olprint("*", "*", "-", 72, True)
    for content in (["", "", "", "RK Resource 001", "version 0.9.1.4 Alfa", "", "", ""]):
        olprint2("{0: ^70}", content, "|", "|")
    olprint("|", "|", "-", 72, True)

    for content in (["", "", "developed by Robin Karlsson", "", "", "Contact information", "", "r.robin.karlsson@gmail.com", "https://www.chess.com/members/view/SudoRoot", "", ""]):
        olprint2("{0: ^70}", content, "|", "|")
    olprint("|", "|", "-", 72, True)

    for content in (["", "", "Options", "", "Type /help or /help <number> for more info", "Type /Upgrade to update to the latest version", "", "", "1. Extract the memberslist of one or more groups", "", "2. Build a csv file with data on a list of members", "", "3. Send invites for a group", "", "4. Posts per member in a groups finished votechess matches", "", "5. Build a csv file of a groups team match participants", "", "6. Filter a list of members for those who fill a few requirements", "", "7. Presentation of csv-files from options 2 and 5", "", "8. Send personal notes to a list of members", "", "9. Look for members who has recenty left your group", "", "10. Count number of group notes per member in the last 100 notes pages", "", "11. Build a birthday schedule for a list of members", "", "12. Send a personal message to a list of members", "", "13. Pair lists of players against each others", "", "14. Set operations on two lists", "", "15. Check a teams won/lost tm's per opponent", "", "16. Delete all group notes in a group", "", "17. Accept open challenges","", "18. Get the 1000 latest team matches on cc sorted by size", "", "19. Check groups for new timeouts", "", "20. Post preconfigured group notes", "", "21. Send tm challenges to a group", "", "22. Check signal strength", "", "23. Fix formating problems in textfiles (EXPERIMENTAL)","", ""]):
        olprint2("{0: ^70}", content, "|", "|")
    olprint("*", "*", "-", 72, True)

    flow = ""
    while flow not in (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "42"]):
        flow = raw_input("\n\n\nEnter your choice here%s: " %usrname)

        if flow == "/help 1":
            print "\n\nCreates a list of members from one or more groups. Has the option to remove those who're also members of a specific group (using the members list built in option 9). The list can either be saved to a file or be directly printed onscreen\n\nOptional login if you wish to extract members from pages that arent public (for example the manage members page)"
        elif flow == "/help 2":
            print "\n\nBuild an excell compatible csv file with the following data on a list of members.\n\n Column 1: Username\n Column 2: Real name (if available on members homepage)\n Column 3. Live Standard rating\n Column 4. Live Blitz rating\n Column 5. Live Bullet rating\n Column 6. Online Chess rating\n Column 7. 960 rating\n Column 8. Tactics rating\n Column 9. Timeout-ratio\n Column 10. Last online\n Column 11. Member since\n Column 12. Time per move\n Column 13. Number of groups member is in\n Column 14. Points\n Column 15. Number of online chess games played\n Column 16. Number of online chess games won\n Column 17. Number of online chess games lost\n Column 18. Number of Online chess games drawn\n Column 19. Win ratio for online chess\n Column 20. Member nation (if available on members homepage)\n Column 21. If member has a custom avatar\n\nThis data can be presented and sorted using option 7 in the main script"
        elif flow == "/help 3":
            print "\n\nSend personalized invites for one or more groups. The invites can include text (with member name and nation, to personalize the message), pictures and videos.\n\nTo use this function you need to have a text document with a newline seperated list of members in the 'Data/Invite Lists' folder. The script sends an invite to each member in that file and creates a second file in the Invite Lists folder, with the usernames of those who has received an invite\n\n\nMembers who are present in the groups 'already invited' file will be skipped when sending invites. To block the script from inviting specific members you can add their names to the already invited file for the group in question, and they will be effectivily blocked\n\nWhen running the inviter with the option to only invite those who fill a few requirements the script will remove those who didn't fill the requirements from your invites list\n\nRequires the script to log in on chess.com, to send the invites from your account"
        elif flow == "/help 4":
            print "\n\nGoes through a groups finished, non thematic votechess matches and counts number of posts per member\n\nRequires the script to log in on chess.com, to acess comments in games"
        elif flow == "/help 5":
            print "\n\nBuild an excell compatible csv file with the following data on how each member who has ever played for a group has performed in the groups team matches\n\n Column 1. Username\n Column 2. Number of team matches member has participated in\n Column 3. Points won\n Column 4. Points lost\n Column 5. Ongoing games\n Column 6. Timeouts"
        elif flow == "/help 6":
            print "\n\nTakes a comma seperated list of members and sort out those who doesn't fill a few criterias regarding:\n\n Min online chess rating\n Max online chess rating\n Last online\n Member Since\n Older than (if birthdate is available on members profile)\n Younger than (if birthdate is available on members profile)\n Min number of groups member may be in\n Max number of groups member may be in\n Timeout-ratio\n Time per move\n If they have a custom avatar\n Gender, determined by comparing the members name to a list of male and female names"
        elif flow == "/help 7":
            print "\n\nPresentation of csv files from option 2 and 5. Can present data from the csv files sorted by any column, compare two csv files from option 5 to see what has changed or return the username of each member in the file and present it as a comma seperated list"
        elif flow == "/help 8":
            print "\n\nSend personalized notes to either a comma seperated list of members or those who are present in a set of pages. The note can include text with the members real name and nation.\n\nRequires the script to log in to chess.com, to send notes from your account"
        elif flow == "/help 9":
            print "\n\nAt first run the script builds a list of members who are currently in your group.\nAt future runs the script will build a new memberslist of your group, look for members who are in the memberslist compiled during the last run but not in the latest run.\nRemoves those who has had their accounts closed or changed their names and print the result, which is the members who has left your group in the timeperiod between two runs\n\nRequires the script to log in to and you to be an admin of the group that's checked, to access the manage members page"
        elif flow == "/help 10":
            print "\n\nCount the number of group notes posted per member in the last 100 pages of notes\n\nRequires the script to login to chess.com, to access group notes"
        elif flow == "/help 11":
            print "\n\nTakes a comma seperated list of members and builds a sorted birthday schedule of those who have their birthday visible on their profile"
        elif flow == "/help 12":
            print "\n\nSend personalized personal messages to either a comma seperated list of members or those who are present in a set of pages. The message can include text (with the members real name and nation, to personalize the message) and images.\n\nRequires the script to log in to chess.com, to send pm's from your account"
        elif flow == "/help 13":
            print "\n\nTakes either one or two list of members and offer to pair them against each others based on rating.\nIf given one lists members will be paired against each other after the format, highest ranked vs second highest rank etc. For two lists the script takes each member in the shorter list and pair this member against whoever has the most similar rating in the longer list\n\nRatings can be Live Standard, Live Blitz, Live Bullet, Online chess, 960 or tactics"
        elif flow == "/help 14":
            print "\n\nPerform set operations (union, intersection, difference, symmetric difference) on two lists"
        elif flow == "/help 15":
            print "\n\nCount number of wins, losses and draws per opponent in a teams team match archive"
        elif flow == "/help 16":
            print "\n\nDeletes all group notes from a specified group\n\nRequires login and admin privilege to access and delete notes"
        elif flow == "/help 17":
            print "\n\nPassive function allowing you to set up a file of target groups and specify which group each targets open challenges should be accepted by.\n\nRequires login to scan for open challenges and to accept challenges"
        elif flow == "/help 19":
            print "\n\nCheck added groups for new timeouts since last run.\n\nAt first run the script collects total timeouts data for each member in all ongoing and completed matches, in subsequent runs the script scans for new timeouts and updates the stored timeouts data"
        elif flow == "/help 20":
            print "\n\nCreate a file where you store premade messages (one file per group), when the script run it will select and post one random message from each groups file to each group\n\nLogin required to post notes from your account"
        elif flow == "/help 22":
            print "\n\nPrints your network signal strength continuously every 0.5 seconds"
        elif flow == "/help":
            print "\n\n\nTo add extensions/addons to the scripts chrome or firefox browser you need to download the extension in crx format for chrome or xpi for firefox. Once the addon is downloaded, place it in the Data/Webdriver/Extensions/Chrome or Data/Webdriver/Extensions/Firefox folder.\n\nIt's recommended to use the adblock plus extension\n\n\n\n\nTo use the scripts ability to determine a members gender you will need to have a list of male and female first names in the Data/.namelists folder. male names should be stored in a file called 'male' and female names in a file called 'female'.\n\nFor best performance the names should be in the format:\nname1\nname2\nname3\netc\n\nIt's also recommended to sort the names based on how commonly they are used"

        elif flow == "/Upgrade":
            update001()

    if flow == "1":
        print "\n\n\nchess.com members list extractor\n"
        print "Locate the members list url of the group you wish to target.\n\n  example: https://www.chess.com/groups/membersearch?allnew=1&id=8893\n\nCopy the url.\n"
        target = tlstcreator()

        noadmins = ""
        while noadmins not in (["y", "n"]):
            noadmins = raw_input("\nInclude admins? (y/n) ")

        logincookie = login()
        browser = mecbrowser(logincookie)
        un1 = set(memspider(target, False, browser))

        if noadmins == "n":
            superadmins, admins = getadmins(getgrouphome(target, browser), browser)
            un1 = un1.difference(superadmins + admins)

        remmem = ""
        while remmem not in (["y", "n"]):
            remmem = raw_input("\n\nFilter out members of a group? (y/n) ")

        if remmem == "y":
            un1 = memremoverf(un1, logincookie)
        un1 = ", ".join(un1)

        choice6 = ""
        while choice6 not in (["1", "2"]):
            choice6 = raw_input("\n\nDo you wish to\n 1. Print the extracted names onscreen\n 2. Save them to a file\n\nEnter choice here: ")

        if choice6 == "1":
            print "\n\n%s" %un1

        elif choice6 == "2":
            memfile1 = "%s.txt" %raw_input("\nName of the file to which your list will be saved: ")
            with open(memfile1, "ab") as placeholder2:
                placeholder2.write(un1)

    elif flow == "2":
        target = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to check: ", "")[0]
        while "" in target:
            target.remove("")
        filename = raw_input("Name of the file to which your data will be saved: ")

        getmeminfo(target, filename)

    elif flow == "3":
        flow = ""

        while flow not in (["1", "2", "3", "4", "5"]):
            flow = raw_input("Would you like to\n 1. Send invites for existing groups\n 2. Add a new group\n 3. Inspect an invite list\n 4. Add names to a groups invite list\n 5. Modify a groups configuration file\n\nMake your choice, young padawan: ")
        print "\n"

        if flow == "2":
            name = raw_input("\n\nGroup name: ")
            createconfig(name, enterint("Group ID: "))
            print "\n\nThe following files have been created\n\n  - /Data/Messages/Invite Messages/%s Standard Message (used to invite members from the standard and VIP invites lists)\n  - /Data/Messages/Invite Messages/%s Deserters Message (Used to reinvite those who have left %s)\n  - Data/Invite Lists/%s (main invites list)\n  - Data/Invite Lists/%s priority (used for those whom you want to invite asap, circumvents any filters)\n  - Data/Invite Lists/%s members who has left (here you can place members who has left %s to reinvite them using the invites message from /Data/Messages/Invite Messages/%s Deserters Message)\n  - Data/Invite Lists/%s already invited (stores the names of those who has received an invite from the script, members in this list wont receive an invite even if their names are in the standard invites list)\n\nTo use the inviter you need to first create a invites message for the script to use and put members whom you want to invite in the invites lists\nChanges to the filter used by %s can be made by modifying the file .Config/Invites/%s\n\n\n\n\nNames in the priority invites list will be invited before those in the list of members who has left and the standard list, without the use of any filters. Names in the invites list of members who has left will be invited before those in the standard list and with the deserters invites message\n\n" %(name, name, name, name, name, name, name, name, name, name, name)

        elif flow == "3":
            count = 1
            flist = []
            for x in sorted([x for x in os.listdir("Data/Invite Lists") if isfile(join("Data/Invite Lists", x))]):
                if x[-1] == "~":
                    continue
                print " %i. %s" %(count, x)
                flist.append(x)
                count += 1

            choiceFile = flist[enterint("\nWhich file do you want to inspect: ") - 1]
            with open("Data/Invite Lists/%s" %choiceFile, "rb") as f:
                nameList = f.read()
            print nameList.replace("\n", ", ")
            print "\n\nNumber of members in list: %i\n" %len(nameList.split("\n"))

        elif flow == "4":
            count = 1
            flist = []
            for x in sorted([x for x in os.listdir("Data/Invite Lists") if isfile(join("Data/Invite Lists", x))]):
                if "~" in x or "already invited" in x or "members who has left" in x:
                    continue
                print " %i. %s" %(count, x)
                flist.append(x)
                count += 1

            groupChoice = flist[enterint("\nWhich file do you want to add names to: ") - 1]
            newMem = raw_input("\nEnter a comma seperated list of usernames to be added: ").replace(" ", "")

            with open("Data/Invite Lists/%s" %groupChoice, "ab") as f:
                f.write("\n%s" %"\n".join(newMem.split(",")))

        elif flow == "5":
            count = 1
            flist = []
            for x in sorted([x for x in os.listdir(".Config/Invites") if isfile(join(".Config/Invites", x))]):
                print " %i. %s" %(count, x)
                flist.append(x)
                count += 1

            groupChoice = flist[enterint("\nWhich file do you want to inspect/modify: ") - 1]

            with open(".Config/Invites/%s" %groupChoice, "rb") as f:
                conelements = f.readlines()

            print "\n\n\nCurrent config file setup:\n\n"
            count = 1
            for x in conelements:
                print " %i. %s" %(count, x)
                count += 1

            conelement_index = enterint("\n\nWhich one do you want to change? ") - 1

            conelements[conelement_index] = "%s==%s\n" %(conelements[conelement_index].split("==")[0], raw_input("\nNew value: "))

            with open(".Config/Invites/%s" %groupChoice, "wb") as f:
                for element in conelements:
                    f.write(element)

        else:
            inifilelist = getfilelist(".Config/Invites", ".ini")
            print "\n\nwhich group would you like to send invites for?\n 0 Infinite loop over all groups"
            for fname in inifilelist:
                print "", fname[0], fname[1].replace(".ini", "")

            invchoice = enterint("which group(s) would you like to send invites for? ")

            if invchoice == 0:
                inviter(inifilelist, True)
            else:
                inviter([inifilelist[invchoice - 1]], False)

    elif flow == "4":
        yourside = raw_input("Name of group to check: ")
        vclinklist = getvclinks(yourside)
        parmemvc = vcman(vclinklist, yourside)

        for key, value in sorted(parmemvc.items(), key = itemgetter(1), reverse = True):
            print "\n%s has made %i posts" %(key, value)

        while flow not in (["y", "n"]):
            flow = raw_input("\n\nGet the same list in an invites friendly format? (y/n) ")

        if flow == "y":
            print "\n\n"
            for key, value in sorted(parmemvc.items(), key = itemgetter(1), reverse = True):
                print key + ",",
            print "\n"

    elif flow == "5":
        browser = mecbrowser("")
        pathtm = ""
        while pathtm not in (["1", "2"]):
            pathtm = raw_input(" 1. Check all tm's for a group\n 2. Check a single tm\nYour choice: ")
        targetnameorg = raw_input("\n\n\nName of the group you wish to check: ")
        targetname = re.sub(r"[^a-z A-Z 0-9 -]","", targetnameorg)
        targetname = targetname.replace(" ", "-").lower()

        if pathtm == "1":
            targetnameorgf = targetnameorg
            pagelist = list(set(gettmlinks(browser, targetname, None)))
        elif pathtm == "2":
            pathtm = ""
            while pathtm not in (["1", "2"]):
                pathtm = raw_input("\n\n 1. Check the tm for results\n 2. Check match for members with a timeout-ratio above a specific value\nYour choice: ")
            pagelist = raw_input("team match id: ")
            targetnameorgf = "team match: %s ... " %pagelist
            pagelist = (["https://www.chess.com/groups/team_match?id=%s" %pagelist])

        tmpar, tmtimeout, winssdic, losedic = tmparchecker(browser, pagelist, targetname)

        if pathtm == "1":
            tmparcount = Counter(tmpar)
            tmtimeoutcount = Counter(tmtimeout)
            joined = {}
            membernamelist = list()

            outputfile = open("%s %s.tm.csv" %(targetnameorgf, time.strftime("%Y-%m-%d %H%M")), "wb")
            csvwriter = csv.writer(outputfile, delimiter = " ", quoting=csv.QUOTE_MINIMAL)

            for pointer in set(tmparcount.keys())|set(winssdic.keys())|set(losedic.keys())|set(tmtimeoutcount.keys()):
                joined[pointer] = (float(tmparcount.get(pointer, 0))/10 + (float(tmparcount.get(pointer, 0))*2 - float(winssdic.get(pointer, 0)) - float(losedic.get(pointer, 0)))*5/4 + float(winssdic.get(pointer, 0)) - float(losedic.get(pointer, 0)) - tmtimeoutcount.get(pointer, 0)*3, tmparcount.get(pointer, 0), winssdic.get(pointer, 0), losedic.get(pointer, 0), tmtimeoutcount.get(pointer, 0))

            csvwriter.writerow(("Member name", "tm's participated in", "points won", "points lost", "ongoing games", "timeouts", "win ratio", "timeout ratio"))

            timeoutnum = 0
            ptswon = 0
            ptslost = 0
            for key, value in sorted(joined.items(), key = itemgetter(1), reverse = True):
                gamesplaid = value[3] + value[2]

                if gamesplaid != 0:
                    winrat = value[2] / gamesplaid
                    timerat = value[4] / gamesplaid
                else:
                    winrat = 0
                    timerat = 0

                csvwriter.writerow((key, value[1], value[2], value[3], value[1]*2 - value[2] - value[3], value[4], winrat, timerat))
                timeoutnum += value[4]
                ptswon += value[2]
                ptslost += value[3]

            outputfile.close()
            try:
                print "\n\n\nTimeouts per player (number of timeouts (%i) / number of players (%i)): %.4f" %(timeoutnum, len(joined), (timeoutnum + 0.0) / len(joined))
            except ZeroDivisionError:
                None
            try:
                print "Team match points won ratio (points won (%.1f) / total number of points (%.1f)): %.4f\n\n" %(ptswon, ptslost + ptswon, (ptswon + 0.0) / (ptslost + ptswon))
            except ZeroDivisionError:
                None

        elif pathtm == "2":
            maxtmrat = int(raw_input("\n\nGet members with a timeout-ratio above: ").replace("%", ""))
            browser = mecbrowser("")

            deadbeatlist = list()
            for member in tmpar:
                print "%schecking %s" %(ltime(), member)
                while True:
                    try:
                        browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %member)
                        soup = BeautifulSoup(response)
                        break
                    except Exception, errormsg:
                        if supusr:
                            print repr(errormsg)
                        time.sleep(1)

                if "://www.chess.com/members/view/" not in browser.geturl():
                    continue
                if timeoutchecker(soup) > maxtmrat:
                    deadbeatlist.append(member)

                soup.decompose()
                response.close()
                browser.clear_history()
                gc.collect()

            print "\n\n\nThe following members has a timeoutratio above %i%%: %s" %(maxtmrat, ", ".join(deadbeatlist))

    elif flow == "6":
        passmembers = list()
        membernamelist = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to check: ", "")[0]

        minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat = memprmenu()
        ingroup = raw_input("\nMember should be in group (leave empty to skip, login required!!!): ")
        if ingroup != "":
            logincookie = login()
        else:
            logincookie = ""

        browser = mecbrowser(logincookie)

        target = streplacer(str(membernamelist), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""])).split(",")

        while "" in target:
            target.remove("")

        for targetx in target:
            if supusr:
                debugout()

            print "%schecking %s" %(ltime(), targetx)

            while True:
                try:
                    browser, response = mecopner(browser, "https://www.chess.com/members/view/%s" %targetx)
                    soup = BeautifulSoup(response)
                    break
                except Exception, errormsg:
                    if supusr:
                        print repr(errormsg)
                    time.sleep(1)

            if "://www.chess.com/members/view/" not in browser.geturl():
                print "\n\nfailed to open page, https://www.chess.com/members/view/%s" %targetx
                continue

            if memberprocesser(soup, targetx, minpoints, minrat, maxrat, mingames, mincurrent, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemin, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat):
                if ingroup != "":
                    if ingroupcheck(browser, targetx, ingroup):
                        passmembers.append(targetx)
                else:
                    passmembers.append(targetx)

            response.close()
            browser.clear_history()
            soup.decompose()
            gc.collect()

        choice6 = ""
        while choice6 not in (["1", "2"]):
            choice6 = raw_input("\n\nDo you wish to\n 1. Print the names of those who fill your criterias onscreen\n 2. Save them to a file\n\nEnter choice here: ")

        if choice6 == "1":
            print "\n\n%s" %", ".join(passmembers)

        if choice6 == "2":
            memfile1 = raw_input("\nName of the file to which your list will be saved: ") + ".txt"
            with open(memfile1, "ab") as placeholder2:
                placeholder2.write(streplacer(str(passmembers), (["'", ""], ["[", ""], ["]", ""])))

    elif flow == "7":
        memlist = list()
        clist = list()
        flist = list()
        counter3 = 1

        choicepath = ""
        while choicepath not in (["1", "2"]):
            choicepath = raw_input("\nWhat would you like to process\n 1. csv file over team matches from option 5\n 2. csv file of member stats from option 2\nYour choice, monkeyboy: ")

        print "\n\ncsv files in directory"
        filesindic = os.listdir(".")
        for fname in filesindic:
            if choicepath == "1":
                if fname.endswith(".tm.csv"):
                    flist.append(fname)
                    print " %i. %s" %(counter3, fname)
                    clist.append(str(counter3))
                    counter3 += 1
            elif choicepath == "2":
                if fname.endswith(".mem.csv"):
                    flist.append(fname)
                    print " %i. %s" %(counter3, fname)
                    clist.append(str(counter3))
                    counter3 += 1

        if choicepath == "1":
            choice = ""
            while choice not in (["1", "2"]):
                choice = raw_input("\noptions:\n 1. Get data from one of the csvfiles\n 2. Compare two csv-files\nYour choice: ")
        elif choicepath == "2":
            choice = "1"

        if choice == "1":
            choice1 = ""
            while choice1 not in clist:
                choice1 = raw_input("\nwhich one do you wish to check? ")

            with open(flist[int(choice1) - 1], "rb") as f:
                csvreader = csv.reader(f, delimiter = " ")
                if choicepath == "1":
                    for row in csvreader:
                        if row[0] == "Member name (those who fill your requirements)":
                            break
                        memlist.append(row)

                elif choicepath == "2":
                    for row in csvreader:
                        memlist.append(row)

            csvsoworker(memlist, choicepath)

        elif choice == "2":
            ichoice = ""
            while ichoice not in (["1", "2", "3", "4", "5"]):
                ichoice = raw_input("\nwhat values would you like to compare?\n 1. tm's participated in\n 2. points won\n 3. points lost\n 4. ongoing games\n 5. timeouts\nYour choice: ")
            ichoice = int(ichoice)

            with open(flist[enterint("\nnumber of the older file: ") - 1], "rb") as f:
                csvreader = csv.reader(f, delimiter = " ")
                for row in csvreader:
                    if row[0] == "Member name (those who fill your requirements)":
                        break
                    memlist.append((row[0], row[ichoice]))

            memlist2 = list()
            with open(flist[enterint("number of the new file: ") - 1], "rb") as f:
                csvreader = csv.reader(f, delimiter = " ")
                for row in csvreader:
                    if row[0] == "Member name (those who fill your requirements)":
                        break
                    memlist2.append((row[0], row[ichoice]))

            colwidth = max(len(element) for row in memlist for element in row) + 2
            print "\n\n%s\n" %"".join(element.ljust(colwidth) for element in (memlist[0][0], memlist[0][1] + " old", memlist[0][1] + " new", "difference"))
            fmemlist = list()
            for tup in memlist2:
                if tup not in memlist:
                    for tup2 in memlist:
                        if tup[tup.index(tup[0])] in tup2 and max(float(tup[1]), float(tup2[1])) != 0.0:
                            fmemlist.append((tup[0], str(min(float(tup[1]), float(tup2[1]))).replace(".0", ""), str(max(float(tup[1]), float(tup2[1]))).replace(".0", ""), str(abs(float(tup[1]) - float(tup2[1]))).replace(".0", "")))
            fmemlist = sorted(fmemlist, reverse = True, key = lambda tup: tup[-1])
            for cpointer in fmemlist:
                print "".join(element.ljust(colwidth) for element in cpointer)

    elif flow == "8":
        target = file_or_input(False, "\n\nName of the file containing your list of members: ", "", "\n\nEnter list of members to send notes: ", "")[0]
        print "\n\nYou have entered %i names\n\n" %len(target)
        msg = msgcomfix(raw_input("\n\nEnter message to use (available commands: /name = member name or username, /firstname - member first name or username (if no name is available), /nation = member nation): "))
        nationalt = raw_input("\nWhat to use if member nation is international? ")
        interval = enterint("Interval between notes (s): ")

        shutdown = ""
        while shutdown not in (["y", "n"]):
            shutdown = raw_input("\n\nShut down computer when complete (might require elevated privileges)? (y/n) ")

        noteposter(target, msg, interval, nationalt, shutdown)

    elif flow == "9":
        while flow not in (["1", "2"]):
            flow = raw_input("\n\nWould you like to\n 1. Check existing groups\n 2. Add a new group\nMake your choice, young padawan: ")

        if flow == "2":
            name = raw_input("\n\nGroup name: ")
            Key = raw_input("Encryption key: ")

            invconpath = ".Config/Invites/%s.ini" %name
            membersleftinvfile = "\nMembers who has left invites file (optional)=="
            if os.path.isfile(invconpath):
                membersleftinvfile = membersleftinvfile + configopen(invconpath)["Invites file for those who has left the group"]
            else:
                membersleftinvfile = "%sData/Invite Lists/%s members who has left" %(membersleftinvfile, name)

            with open(".Config/Member Lists/%s.ini" %name, "wb") as setupfile:
                setupfile.write("Group ID==%i\nEncryption Key==%s\nMemberslist file==Data/.Member Lists/%s%s" %(enterint("Group ID: "), Key, name, membersleftinvfile))

            print "\n\nThe following files have been created\n\n  - /Data/Messages/Invite Messages/%s Standard Message (used to invite members from the standard and VIP invites lists)\n  - /Data/Messages/Invite Messages/%s Deserters Message (Used to reinvite those who have left %s)\n  - Data/Invite Lists/%s (main invites list)\n  - Data/Invite Lists/%s priority (used for those whom you want to invite asap, circumvents any filters)\n  - Data/Invite Lists/%s members who has left (here you can place members who has left %s to reinvite them using the invites message from /Data/Messages/Invite Messages/%s Deserters Message)\n  - Data/Invite Lists/%s already invited (stores the names of those who has received an invite from the script, members in this list wont receive an invite even if their names are in the standard invites list)\n\nTo use the inviter you need to first create a invites message for the script to use and put members whom you want to invite in the invites lists\nChanges to the filter used by %s can be made by modifying the file .Config/Invites/%s\n\n" %(name, name, name, name, name, name, name, name, name, name, name)
            continue

        filelist = getfilelist(".Config/Member Lists", ".ini")
        print "\n\nWhich group do you wish to check?\n 0 Loop over all groups"
        for fname in filelist:
            print "", fname[0], fname[1][0:-4]
        choice = enterint("which group(s) would you like to process? ")

        if choice == 0:
            targetlst = filelist
        else:
            targetlst = [filelist[choice - 1]]

        logincookie = login()
        browser = mecbrowser(logincookie)

        for target in targetlst:
            condic = configopen(".Config/Member Lists/%s" %target[1])
            deserters, newcount, oldcount = nineworker(condic["Memberslist file"], str(condic["Group ID"]), browser, str(condic["Encryption Key"]))

            print "\n\n%sMembers who are no longer in %s: %s\nNumber of members on last run: %i\nNumber of members now: %i" %(ltime(), target[1][0:-4], ", ".join(deserters), oldcount, newcount)

            leftfile = condic["Members who has left invites file (optional)"]
            if os.path.isfile(leftfile) is True and len(deserters) > 0:
                with open(leftfile, "ab") as colfile:
                    colfile.write("\n%s" %"\n".join(deserters))

    elif flow == "10":
        grcheck = raw_input("group to check: ")
        grcheck = re.sub(r"[^a-z A-Z 0-9 -]","", grcheck)
        grcheck = grcheck.replace(" ", "-").lower()
        grcheck = "https://www.chess.com/groups/notes/%s?page=" %grcheck
        logincookie = login()

        browser = mecbrowser(logincookie)

        target = list()
        for counter in range(1, 101):
            target.append(grcheck + str(counter))

        notedic = dict()
        for targetp in target:
            print ltime() + targetp

            if supusr:
                debugout()

            while True:
                try:
                    browser, response = mecopner(browser, targetp)
                    soup = BeautifulSoup(response)
                    break
                except Exception, errormsg:
                    if supusr:
                        print repr(errormsg)
                    time.sleep(1)

            links1 = browser.links()
            for link in links1:
                ltext = link.text
                if "/members/view/" in str(link) and ltext != "View profile[IMG]":
                    if ltext in notedic:
                        notedic[ltext] += 1
                    else:
                        notedic[ltext] = 1
            soupbrake = str(soup.find_all(class_ = "next-on"))

            soup.decompose()
            response.close()
            browser.clear_history()
            gc.collect()

            if soupbrake == "[]":
                break

        sorteddic = OrderedDict(sorted(notedic.items(), key = lambda x: x[1], reverse = True))

        for nam, num in sorteddic.items():
            print "%s has made %i notes" %(nam, num)

        while flow not in (["y", "n"]):
            flow = raw_input("\n\nGet the same list in an invites friendly format? (y/n) ")

        if flow == "y":
            print "\n\n"
            for nam, num in sorteddic.items():
                print "%s," %nam,
            print "\n"

    elif flow == "11":
        target = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to check: ", "")[0]
        birthdaylist = ageproc(target)
        birthdsorter(birthdaylist)

    elif flow == "12":
        target = file_or_input(False, "\n\nName of the file containing list of members to pm: ", "", "\n\nEnter list of members to pm: ", "")[0]

        print "\n\n%i pm's will be sent\n" %len(target)

        pmdriver(target, "2")

    elif flow == "13":
        gchoice = ""
        while gchoice not in (["1", "2", "3"]):
            gchoice = raw_input("\n\n 1. Pair a list of members against each others\n 2. Pair two lists of members to play each others\n 3. find a fair play solution for a tm\nChoice: ")

        browser = mecbrowser("")

        if gchoice == "1":
            target = file_or_input(False, "\n\nName of the file containing your list of players: ", "", "\n\nEnter list of players: ", "")[0]
            while "" in target:
                target.remove("")

        elif gchoice == "2":
            name1org = raw_input("Name of group 1: ")
            target1 = file_or_input(False, "\n\nName of the file containing %s's players: " %name1org, "", "\n\nEnter %s's list of players: " %name1org, "")[0]
            while "" in target1:
                target1.remove("")
            name2org = raw_input("Name of group 2: ")
            target2 = file_or_input(False, "\n\nName of the file containing %s's players: " %name2org, "", "\n\nEnter %s's list of players: " %name2org, "")[0]
            while "" in target2:
                target2.remove("")

            target1, target2 = remcomelem(target1, target2)

        elif gchoice == "3":
            tmURL = raw_input("\n\nlink to tm: ")
            ratingrange = enterint("Rating range: ")
            group1, lineup1, group2, lineup2 = getTmParticipants(browser, tmURL)


            lineup1a, offset1 = balancetm(lineup1, lineup2, ratingrange)
            lineup2a, offset2 = balancetm(lineup2, lineup1, ratingrange)

            if supusr:
                print "\n\n\n%s vs %s\n offset: %i" %(group2, group1, offset2)
                for i, pair in enumerate(lineup2a):
                    print "\n %i. %s (%s) vs %s (%s)" %(i + 1, pair[0][0], pair[0][1], pair[1][0], pair[1][1])

                print "\n\n\n%s vs %s\n offset: %i" %(group1, group2, offset1)
                for i, pair in enumerate(lineup1a):
                    print "\n %i. %s (%s) vs %s (%s)" %(i + 1, pair[0][0], pair[0][1], pair[1][0], pair[1][1])
                
            else:
                if offset2 < offset1:
                    temp = group2
                    group2 = group1
                    group1 = temp
                    lineup = lineup2a
                    offset = offset2
                else:
                    lineup = lineup1a
                    offset = offset1

                print "\n\n\n%s vs %s" %(group1, group2)
                for i, pair in enumerate(lineup):
                    print "\n %i. %s (%s) vs %s (%s)" %(i + 1, pair[0][0], pair[0][1], pair[1][0], pair[1][1])

            pathway = runagain()
            continue

        choice = ""
        while choice not in (["1", "2", "3", "4", "5", "6"]):
            choice = raw_input("\nMake pairs based on\n 1. Live Standard\n 2. Live Bullet\n 3. Live Blitz\n 4. Online Chess\n 5. 960\n 6. Tactics\nYour choice: ")

        if gchoice == "1":
            partup = pairsorter(browser, target, choice)
            partup = zip(partup, partup[1:])[::2]
            for pair in partup:
                print "%s (%i) - %s (%i)" %(pair[0][0], pair[0][1], pair[1][0], pair[1][1])

        elif gchoice == "2":
            partup1org = pairsorter(browser, target1, choice)
            partup2org = pairsorter(browser, target2, choice)

            if len(partup1org) < len(partup2org):
                partup1 = partup1org
                partup2 = partup2org
                name1 = name1org
                name2 = name2org
            else:
                partup2 = partup1org
                partup1 = partup2org
                name2 = name1org
                name1 = name2org

            pairs = evenpairing(partup1, partup2)

            print "%s - %s" %(name1, name2)
            for pair in pairs:
                print "%s (%i) - %s (%i)" %(pair[0][0], pair[0][1], pair[1][0], pair[1][1])

    elif flow == "14":
        choice = ""
        while choice not in (["1", "2", "3", "4", "5"]):
            choice = raw_input("\n\nwhat would you like to get\n 1. Elements common to both lists (intersection)\n 2. Elements from both lists (union)\n 3. Elements in list 1 but not in list 2 (difference)\n 4. Elements in either list but not in both (symmetric difference)\n\n 5. Length of a comma seperated list\n\nYour choice: ")

        if choice in (["1", "2", "3", "4"]):
            list1, list2 = file_or_input(True, "\n\nName of file 1: ", "Name of file 2: ", "\n\nList1: ", "List2: ")
        else:
            list1 = raw_input("\n\nEnter list: ")

        if choice == "1":
            prlst = streplacer(str(list(set(list1).intersection(set(list2)))), (["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice == "2":
            prlst = streplacer(str(list(set(list1).union(set(list2)))), (["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice == "3":
            prlst = streplacer(str(list(set(list1).difference(set(list2)))), (["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice == "4":
            prlst = streplacer(str(list(set(list1).symmetric_difference(set(list2)))), (["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice == "5":
            print len(list1.split(","))
            pathway = runagain()
            continue

        choice6 = ""
        while choice6 not in (["1", "2"]):
            choice6 = raw_input("\n\nDo you wish to\n 1. Print the data onscreen\n 2. Save it to a file\n\nEnter choice here: ")

        if choice6 == "1":
            print "\n\n%s" %prlst

        elif choice6 == "2":
            sfile = raw_input("\nName of the file to which your list will be saved: ") + ".txt"
            with open(sfile, "wb") as placeholder2:
                placeholder2.write(prlst)

    elif flow == "15":
        targetnameorg = raw_input("\n\n\nName of the group you wish to check: ")
        targetname = re.sub(r"[^a-z A-Z 0-9 -]","", targetnameorg)
        targetname = targetname.replace(" ", "-").lower()

        mtchlist = gettmopdata(targetname)
        parttup = list()
        winssdic = dict()
        losedic = dict()
        drawdic = dict()

        for tm in mtchlist:
            if "Won" in tm[5]:
                if tm[2] in winssdic:
                    winssdic[tm[2]] += 1
                else:
                    winssdic[tm[2]] = 1

            elif "Lost" in tm[5]:
                if tm[2] in losedic:
                    losedic[tm[2]] += 1
                else:
                    losedic[tm[2]] = 1

            elif "Draw" in tm[5]:
                if tm[2] in drawdic:
                    drawdic[tm[2]] += 1
                else:
                    drawdic[tm[2]] = 1

            else:
                if supusr:
                    print "something aint right in this match, please send this to the developer:\n"
                    print tm
                    debugout()
                

        width = 0
        for opteam in set(winssdic.keys())|set(losedic.keys())|set(drawdic.keys()):
            oplen = len(opteam.decode("UTF-8"))
            if oplen > width:
                width = oplen
            parttup.append((opteam, winssdic.get(opteam, 0), losedic.get(opteam, 0), drawdic.get(opteam, 0), winssdic.get(opteam, 0) + losedic.get(opteam, 0) + drawdic.get(opteam, 0)))
        width += 2

        prchoice = ""
        while prchoice not in (["1", "2", "3", "4", "5"]):
            prchoice = raw_input("\n\nSort by\n 1. Opponent name\n 2. Matches won\n 3. Matches lost\n 4. Matches Drawn\n 5. Total number of tm's\nEnter choice: ")
        print "\n\n"

        if prchoice == "1":
            parttup = sorted(parttup, key = lambda tup: tup[0].lower())
        else:
            parttup = sorted(parttup, reverse = True, key = lambda tup: tup[int(prchoice) - 1])

        template = "|{0:%i}|{1:6}|{2:6}|{3:6}|{4:6}|" %width
        print "\n\n\n%s\n%s" %(template.format(" Opponent name", "Won", "Lost", "Draw", "Total"), template.format("-" * width, "-" * 6, "-" * 6, "-" * 6, "-" * 6))
        for tm in parttup:
            print template.format(tm[0], tm[1], tm[2], tm[3], tm[4])

    elif flow == "16":
        gname = re.sub(r"[^a-z A-Z 0-9 -]","", raw_input("\n\nName of target group: ")).replace(" ", "-").lower()
        counter = 1
        sleeptime = enterint("Time to wait between between deletes (4 seconds recommended): ")
        if sleeptime == "":
            sleeptime = 5
        shutdown = ""
        while shutdown not in (["y", "n"]):
            shutdown = raw_input("\nShut down computer when complete (might require elevated privileges)? (y/n) ")

        browserchoice = selbrowch()
        Username, Password = usrPas()
        browser, handle = pickbrowser(browserchoice, True)
        browser = sellogin(Username, Password, browser)

        while True:
            browser = selopner(browser, "https://www.chess.com/groups/notes/%s" %gname)

            if supusr:
                debugout()

            time.sleep(sleeptime)
            try:
                browser.find_element_by_css_selector("a.red").click()
                browser.switch_to_alert().accept()
                counter = 1
            except:
                counter += 1
                if counter == 10:
                    print "\n\nDone!!!\n\n"
                    break
        browser.quit()

        if shutdown == "y":
            turnofcomp()

    elif flow == "17":
        targets = []

        while flow not in (["1", "2", "3"]):
            flow = raw_input("\n\nWhat would you like to do?\n 1. Manually select groups you want to accept challenges from\n 2. Accept open challenges as per the config file\n 3. Add targets to config file\n\nChoose wisely, young padawan: ")

        if flow == "1":
            while flow != "n":
                targets.append([raw_input("\n\nName of target group: "), raw_input("Name of the group you want to accept with: ")])
                flow = raw_input("\nAdd another target group? (y/n) ")

        else:
            if os.path.isfile(".Config/17"):
                with open(".Config/17", "rb") as placeholder:
                    for x in placeholder.read().split("\n\n")[1:]:
                        targets.append(x.split("\n"))
            else:
                open(".Config/17", "wb").close()

            print "\nCurrent targets in config file:"
            for x in targets:
                print " - Open challenges from %s will be accepted by %s" %(x[0], x[1])

            if flow == "3":
                while True:
                    flow = raw_input("\nAdd another target group? (y/n) ")
                    if flow == "n":
                        break
                    with open(".Config/17", "ab") as placeholder:
                        placeholder.write("\n\n%s\n%s" %(raw_input("Name of target group: "), raw_input("Name of the group you want to accept with: ")))
                continue

        browserchoice = selbrowch()
        Username, Password = usrPas()

        browser, handle = pickbrowser(browserchoice, True)
        browser = sellogin(Username, Password, browser)

        logincookie = browser.get_cookies()
        browser1 = mecbrowser(logincookie)

        while True:
            while True:
                try:
                    browser1, response = mecopner(browser1, "https://www.chess.com/groups/team_match_challenges")
                    soup = BeautifulSoup(response)
                    break
                except Exception, errormsg:
                    if supusr:
                        print repr(errormsg)
                    time.sleep(1)

            acceptChallenge(browser, soup, targets)

            time.sleep(3)

    elif flow == "18":
        for x in latestTMsOnsite(mecbrowser("")):
            print "%s vs %s : %s players, score: %s. link: %s\n" %(x[0], x[1], x[2], x[3], x[4])

    elif flow == "19":
        while flow not in (["1", "2"]):
            flow = raw_input("\n\nChoose your path wisely, monkey boy ;)\n 1. Check groups for timeouts\n 2. Add new group\n\nThe moment of truth is upon you: ")

        if flow == "1":
            browser = mecbrowser("")
            inifilelist = getfilelist(".Config/TimeoutsCheck", ".ini")

            for cfile in inifilelist:
                timeoutsList = []
                condic = configopen(".Config/TimeoutsCheck/%s" %cfile[1])

                groupnameorg = cfile[1].replace(".ini", "")
                groupname = condic["Group name"]
                lastCheck = condic["Last check"]
                stopAt = condic["Stop at"]

                if stopAt == "":
                    stopAt = None
                if lastCheck == "":
                    lastCheck = "all time"

                newStop = getNewStopAt(browser, groupname)
                timeoutsListOld, timeoutsDictFull = getOldTimeouts(groupnameorg)

                links = gettmlinks(browser, groupname, stopAt)

                for tmpage in list(set(links)):
                    timeouts = getTmTimouts(browser, groupname, tmpage)

                    if len(timeouts) != 0:
                        timeoutsList.append(timeouts)

                newResults, timeoutsDictNew = compareOldNew(timeoutsListOld, timeoutsList)
                timeoutsDictFull = Counter(timeoutsDictFull) + Counter(timeoutsDictNew)

                print "\n\n\n\n\t\t\t%s\n" %groupnameorg
                print "".join(element.ljust(31) for element in ["Member name", "Timeouts %s - %s" %(lastCheck, time.strftime("%d/%m")), "Timeouts total"])
                for member, timeouts in sorted(timeoutsDictNew.items(), key = itemgetter(1), reverse = True):
                    print "".join(element.ljust(32) for element in [member, str(timeouts), str(timeoutsDictFull[member])])

                with open("Data/.TimeoutsCheck/%s" %groupnameorg, "wb") as placeholder:
                    for line in newResults:
                        placeholder.write("%s,%s,%s\n" %(line[0], line[1], line[2]))

                with open(".Config/TimeoutsCheck/%s.ini" %groupnameorg, "wb") as placeholder:
                    placeholder.write("Group name==%s\nLast check==%s\nStop at==%s" %(groupname, time.strftime("%d/%m"), newStop))

        elif flow == "2":
            gnameorg = raw_input("\n\nName of the group you want to add: ")
            gname = re.sub(r"[^a-z A-Z 0-9 -]","", gnameorg)
            gname = gname.replace(" ", "-").lower()

            with open(".Config/TimeoutsCheck/%s.ini" %gnameorg, "wb") as placeholder:
                placeholder.write("Group name==%s\nLast check==\nStop at==" %gname)

    elif flow == "20":
        while flow not in (["1", "2"]):
            flow = raw_input("\n\nChoose your path, young padawan\n 1. Post in groups\n 2. Add new group or edit an existing one\n\nYour path is: ")

        if flow == "1":
            inifilelist = getfilelist(".Config/Notes Poster", ".data")

            sleepTime = enterint("\n\nTime to wait between posts: ")
            browserchoice = selbrowch()
            
            Username, Password = usrPas()

            browser, handle = pickbrowser(browserchoice, True)
            browser = sellogin(Username, Password, browser)

            for cfile in inifilelist:
                with open(".Config/Notes Poster/%s" %cfile[1], "rb") as placeholder:
                    note = placeholder.read()

                note = [x for x in note.replace("\n\n", "\n").split("\n") if x.replace("\n", "").replace(" ", "") != ""]
                note = random.choice(note)

                browser = selopner(browser, "https://www.chess.com/groups/notes/%s" %cfile[1][: -5])
                browser.find_element_by_id("c17").send_keys(note)
                browser.find_element_by_id("c18").click()

                time.sleep(sleepTime)

            browser.quit()

        elif flow == "2":
            gname = re.sub(r"[^a-z A-Z 0-9 -]","", raw_input("\n\nName of the group you want to add/edit: "))
            gname = gname.replace(" ", "-").lower()

            if not os.path.isfile(".Config/Notes Poster/%s.data" %gname):
                open(".Config/Notes Poster/%s.data" %gname, "wb").close()

            while True:
                flow = raw_input("Add new note? (y/n) ")

                if flow == "n":
                    break

                newNote = raw_input("Enter note: ")

                with open(".Config/Notes Poster/%s.data" %gname, "ab") as placeholder:
                    placeholder.write("\n\n%s" %newNote)

    elif flow == "21":
        target = raw_input("Target group name: ")
        myGroup = raw_input("Name of my group: ")
        nbMatches = enterint("Number of challenges to send: ")
        matchName = raw_input("Name of the match(es): ")
        tmDescription = raw_input("Match description: ")

        browserchoice = selbrowch()
        Username, Password = usrPas()

        browser, handle = pickbrowser(browserchoice, True)
        browser = sellogin(Username, Password, browser)

        for count in xrange(0, nbMatches):
            sendChallenge(browser, matchName, target, myGroup, tmDescription)
            time.sleep(300)

        browser.quit()

    elif flow == "22":
        if usrsys == "Linux":
            if not supusr:
                template = "|{0:6}|{1:15}|{2:12}|{3:12}|"
                print "\n\n\n%s\n%s" %(template.format(" Time", "Signal Strength", "Link Quality", "Signal Level"), template.format("-" * 6, "-" * 15, "-" * 12, "-" * 12))
            else:
                template = "|{0:6}|{1:9}|{2:20}|{3:7}|{4:7}|{5:8}|{6:9}|"
                print "\n\n\n%s\n%s" %(template.format(" Time", "Interface", "ESSID".center(20), "Sig Str", "Quality", "Sig lvl", "Frequency"), template.format("-" * 6, "-" * 9, "-" * 20, "-" * 7, "-" * 7, "-" * 8, "-" * 9))

        elif usrsys == "Windows":
            template = "|{0:6}|{1:15}|"
            print "\n\n\n%s\n%s" %( template.format(" Time", "Signal Strength"), template.format("-" * 6, "-" * 15))

        else:
            print "\n\nUnfortunately this option is currently not suported on %s" %usrsys
            continue

        while True:
            sigstrength(template)
            time.sleep(0.4)

    elif flow == "23":
        while flow not in (["1", "2"]):
            flow = raw_input("\n\nWhat would you like to try and fix?\n 1. Invites List\n 2. Invites Message\n\nChooce wisely, monkey boy: ")

        if flow == "1":
            fileList = getfilelist("Data/Invite Lists", "")
        elif flow == "2":
            fileList = getfilelist("Data/Messages/Invite Messages", "")

        print "\n\n"
        for fname in fileList:
            print "", fname[0], fname[1].replace(".ini", "")

        fileChoice = enterint("which file would you like to try and automatically fix (WARNING EXPERIMENTAL! backup of your file to prevent data loss)? ")

        if flow == "1":
            myFile = "Data/Invite Lists/%s" %fileList[fileChoice - 1][1]

            with open(myFile, "rb") as f:
                content = f.read()

            content = streplacer(content, ([" ", ""], [",", "\n"])).split("\n")

            while "" in content:
                content.remove("")

        elif flow == "2":
            myFile = "Data/Messages/Invite Messages/%s" %fileList[fileChoice - 1][1]

            with open(myFile, "rb") as f:
                content = f.read()

            content = msgFix(content)

        with open(myFile, "wb") as f:
            f.write("\n".join(content))


    elif flow == "42":
        choice = ""
        while not choice in (["1", "2"]):
            choice = raw_input("check\n 1. notes\n 2. friendslist\nEnter choice: ")
        tocheck = raw_input("Members to check: ").replace(" ", "").split(",")
        checkfor = raw_input("Check for: ").lower()

        present, notpresent = notesfriendscheck(tocheck, checkfor, choice)

        print "\n\nFound in:"
        for mem in present:
            print "%s, " %mem,
        print "\n\n\nNot found in:"
        for mem in notpresent:
            print "%s, " %mem,
        print "\n"

    gc.collect()
    pathway = runagain()
