# -*- coding: utf-8 -*-
# RK resource 001
# developed by Robin Karlsson
# contact email: "r.robin.karlsson@gmail.com"
# contact chess.com profile: "http://www.chess.com/members/view/RobinKarlsson"
# version 0.8.9 dev

import mechanize
import os
import sys
import csv
import urlparse
import cookielib
import random
import base64
import stat
import re
import time
import platform as _platform
from time import strftime, gmtime
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from operator import itemgetter
from collections import OrderedDict
from collections import Counter
from string import punctuation
supusr = True

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
            counter = 1
            print "\n\nwhat would you like to include?"
            while counter < len(memlist[0]):
                print " " + str(counter) + ". " + memlist[0][counter]
                counter += 1

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
            print " " + count2id + ". " + pointer
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
                memlist2 = sorted(memlist2, key = lambda tup: tup[0].lower())
            elif type(memlist2[0][choice2]) is float or type(memlist2[0][choice2]) is list:
                memlist2 = sorted(memlist2, reverse = True, key = lambda tup: tup[choice2])

        print "\n\n" + "".join(element.ljust(colwidth) for element in ltitle) + "\n"
        llength = len(memlist2[0])
        for cpointer in memlist2:
            counter = 0
            while counter < llength:
                cpointer[counter] = str(cpointer[counter])
                counter += 1
            print "".join(element.ljust(colwidth) for element in cpointer)

    elif choice == "2":
        del memlist[0]
        memlist2 = list()

        for cpointer in memlist:
            memlist2.append(cpointer[0])

        print "\n\n" + streplacer(str(memlist2), (["'", ""], ["[", ""], ["]", ""]))

def getmeminfo(target, filename):
    browser = mecbrowser("")

    memlist = list()
    outputfile = open(filename + " " + strftime("%Y-%m-%d", gmtime()) + ".mem.csv", "wb")
    csvwriter = csv.writer(outputfile, delimiter = " ", quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(("Username", "Real name", "Live Standard rating", "Live Blitz rating", "Live Bullet rating", "Online rating", "960 rating", "Tactics rating", "Timeout-ratio", "Last online", "Member since", "Time/move", "Groups", "Points", "Total games", "Games won", "Games lost", "Games drawn", "Win ratio", "Nation", "Custom avatar"))

    for mem in target:
        print "Processing " + mem
        browser, response = mecopner(browser, "http://www.chess.com/members/view/" + mem)
        if "://www.chess.com/members/view/" not in browser.geturl():
            continue

        soup = BeautifulSoup(response)

        timemove = TimeMoveChecker(soup)
        memsinlastonl = memsin(soup)
        gamestat = gamestats(soup)
        if gamestat[0] != 0.0:
            winratm = gamestat[1] / gamestat[0]
        else:
            winratm = 0

        csvwriter.writerow((mem, namechecker(soup).encode("utf-8"), lstanratingchecker(soup), lblitzratingchecker(soup), lbulratingchecker(soup), onlratingchecker(soup), ranratingchecker(soup), tacratingchecker(soup), timeoutchecker(soup), memsinlastonl[1], memsinlastonl[0], timemove, groupmemlister(soup), ptscheck(soup), gamestat[0], gamestat[1], gamestat[2], gamestat[3], winratm, nationlister(soup).encode("utf-8"), AvatarCheck(soup)))

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
    browser.set_handle_gzip(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    return browser

def pickbrowser(browserchoice, adext):
    usrplatform = getplatform()
    handle = False
    while True:
        if browserchoice == "1":
            fopt = webdriver.FirefoxProfile()
            if adext == True:
                for fname in os.listdir("Webdriver/Extensions/Firefox"):
                    if fname.endswith(".xpi"):
                        try:
                            fopt.add_extension(os.path.abspath("Webdriver/Extensions/Firefox/" + fname))
                            if "adblock" in fname:
                                handle = True
                        except Exception, errormsg:
                            if supusr is True:
                                print repr(errormsg)
                            print "Failed to load " + os.path.abspath("Webdriver/Extensions/Firefox/" + fname)
            try:
                browser = webdriver.Firefox(fopt)
            except Exception, errormsg:
                if supusr is True:
                    print repr(errormsg)
                print "\n\nFailed to initiate Firefox with addons, reverting to standard\n\n"
                browser = webdriver.Firefox()
            break

        elif browserchoice == "2":
            copt = Options()
            if adext == True:
                for fname in os.listdir("Webdriver/Extensions/Chrome"):
                    if fname.endswith(".crx"):
                        try:
                            copt.add_extension(os.path.abspath("Webdriver/Extensions/Chrome/" + fname))
                            if "adblock" in fname:
                                handle = True
                        except Exception, errormsg:
                            if supusr is True:
                                print repr(errormsg)
                            print "Failed to load " + os.path.abspath("Webdriver/Extensions/Chrome/" + fname)

            if usrplatform[1] == "Linux":
                chromepath = os.path.abspath("Webdriver/Linux/86/chromedriver")
                os.environ["webdriver.chrome.driver"] = chromepath
                try:
                    browser = webdriver.Chrome(chromepath, chrome_options = copt)
                except Exception, errormsg:
                    if supusr is True:
                        print repr(errormsg)
                    print "\n\nFailed to initiate Chrome with extensions, reverting to standard\n\n"
                    browser = webdriver.Chrome(chromepath)
                break

            elif usrplatform[1] == "Windows":
                chromepath = os.path.abspath("Webdriver/Windows/86/chromedriver.exe")
                os.environ["webdriver.chrome.driver"] = chromepath
                browser = webdriver.Chrome(chromepath, chrome_options = copt)
                break

            elif usrplatform[1] == "Darwin":
                chromepath = os.path.abspath("Webdriver/Mac/86/chromedriver")
                os.environ["webdriver.chrome.driver"] = chromepath
                browser = webdriver.Chrome(chromepath, chrome_options = copt)
                break

        elif browserchoice == "3":
            if usrplatform[1] == "Linux":
                browser = webdriver.PhantomJS(os.path.abspath("Webdriver/Linux/86/phantomjs"))
                break

            elif usrplatform[1] == "Windows":
                browser = webdriver.PhantomJS(os.path.abspath("Webdriver/Windows/86/phantomjs.exe"))
                break

            elif usrplatform[1] == "Darwin":
                browser = webdriver.PhantomJS(os.path.abspath("Webdriver/Mac/86/phantomjs"))
                break

        elif browserchoice == "4":
            if usrplatform[1] == "Windows":
                browser = webdriver.Ie(os.path.abspath("Webdriver/Windows/86/IEDriverServer.exe"))
                break
        browserchoice = raw_input("\nSomething went wrong, please send this to the developer: " + browserchoice + str(usrplatform) + "\n\nTry and pick another browser\n 1. Firefox\n 2. Chrome\n 3. PhantomJS\n 4. Internet Explorer\nEnter choice: ")

    if handle == True:
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
        browser, response = mecopner(browser, str(linkarchive) + "&page=" + str(pointer))
        soup = BeautifulSoup(response)
        soupbrake = str(soup.find_all(class_ = "next-on"))

        evenmtch = soup.find_all(class_ = "even")
        mtchlist = resource01(evenmtch, mtchlist)

        oddmtch = soup.find_all(class_ = "odd")
        mtchlist = resource01(oddmtch, mtchlist)

        if soupbrake == "[]":
            break
        pointer += 1
    return mtchlist

def turnofcomp():
    usrplatform = getplatform()

    if usrplatform[1] == "Linux":
        import dbus
        try:
            dbus.Interface(dbus.SystemBus().get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager"), "org.freedesktop.ConsoleKit.Manager").get_dbus_method("Stop")() #ConsoleKit
        except Exception, errormsg:
            if supusr is True:
                print repr(errormsg)

        try:
            dbus.Interface(dbus.SystemBus().sys_bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/devices/computer"), "org.freedesktop.Hal.Device.SystemPowerManagement")() #HAL
        except Exception, errormsg:
            if supusr is True:
                print repr(errormsg)

    elif usrplatform[1] == "Windows":
        os.system("shutdown -h now")

    elif usrplatform[1] == "Darwin":
        try:
            import subprocess
            subprocess.call(["osascript", "-e", 'tell app "System Events" to shut down'])
        except Exception, errormsg:
            if supusr is True:
                print repr(errormsg)

    os.system("shutdown -h now")

def resource01(evenmtch, mtchlist):
    ctrl = False
    for element in evenmtch:
        if ctrl == True:
            mtchlist.append(str(element.text.encode("utf8")).split("\n"))
        ctrl = True
    return mtchlist

def gettmlinks(targetname):
    browser = mecbrowser("")
    linklist = gettmlinklist(targetname, browser)

    linkarchive = linklist.pop(-1)
    pointer = 1

    while True:
        browser, response = mecopner(browser, str(linkarchive) + "&page=" + str(pointer))
        soup = BeautifulSoup(response)

        soupbrake = str(soup.find_all(class_ = "next-on"))
        souplinks = re.findall("/groups/team_match(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]i|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))
        for link in souplinks:
            linklist.append("http://www.chess.com" + link)

        if soupbrake == "[]":
            break
        pointer += 1

    linklist = list(set(linklist))
    return linklist

def birthdsorter(birthdaylist):
    choice = "1"
    while choice not in (["1"]):
        choice = raw_input("\n\nOptions:\n 1. print the collected information sorted by birthdays\nYour choice: ")

    if choice == "1":
        birthdaylist = sorted(birthdaylist)
        for element in birthdaylist:
            print str(element[1]) + "/" + str(element[0]) + " - " + element[3] + ", born " + str(element[2])

def getvclinks(yourside):
    linklist = list()
    yourside = re.sub(r"[^a-z A-Z 0-9]","", yourside)
    yourside = yourside.replace(" ", "-").lower()
    browser = mecbrowser("")

    pagenum = 1
    while pagenum <= 100:
        browser, response = mecopner(browser, "http://www.chess.com/groups/votechess_diagrams/" + yourside + "/?sortby=completed&page=" + str(pagenum))
        soup = BeautifulSoup(response)
        souplinks = re.findall("/votechess/game(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))
        for link in souplinks:
            linklist.append("http://www.chess.com" + link)

        soupbrake = str(soup.find_all(class_ = "next-on"))
        if soupbrake == "[]":
            break

        pagenum += 1
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

def pmdriver(target, choice):
    while "" in target:
        target.remove("")
    print "\n\n\n\nsupported commands, will be replaced with each members respective info\n /name - members name or username (if name is unavailable)\n /nation - members nation of origin\n /newline - pagebreak\n\n\n"
    subjectorg = raw_input("subject line: ")
    msglist = list()
    choicepm = "y"
    while choicepm == "y":
        while choicepm not in(["1", "2"]):
            choicepm = raw_input("\n\nAdd a snippet containing\n 1. Text\n 2. Image\nYour choice: ")
        if choicepm == "1":
            text = raw_input("Enter the text: ")
        elif choicepm == "2":
            text = raw_input("Enter url of the image: ")
        msglist.append((choicepm, text))

        while choicepm not in (["y", "n"]):
            choicepm = raw_input("add another snippet? (y/n) ")

    nnation = raw_input("If member nation is International, use this instead: ")

    while True:
        sleeptime = raw_input("\n\nSeconds to wait between pm's: ")
        try:
            sleeptime = int(sleeptime)
            break
        except ValueError:
            "do nothing"        

    browserchoice = selbrowch()

    shutdown = ""
    while shutdown not in (["y", "n"]):
        shutdown = raw_input("\n\nShut down computer when complete (requires elevated privileges)? (y/n) ")

    choice2 = ""
    while choice2 not in (["y", "n"]):
        choice2 = raw_input("\nSort out those who dont fill a few requirements? (y/n) ")

    Username = raw_input("\n\n\nUsername: ")
    Password = raw_input("Password: ")

    browser0, handle = pickbrowser(browserchoice, True)
    browser0 = sellogin(Username, Password, browser0)

    logincookie = browser0.get_cookies()

    if choice == "1":
        memtpm = spider(target, logincookie, False)
    elif choice == "2":
        memtpm = target

    if choice2 == "y":
        minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat = memprmenu()

    browser1 = mecbrowser(logincookie)
    print "\n\n"

    counter = 1
    for membername2 in memtpm:
        if choice2 == "y":
            passmemfil = memberprocesser(True, browser1, ([membername2]), minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat)

            if membername2 not in passmemfil:
                continue

        if browserchoice == "1":
            counter += 1
            if counter > 70:
                browser0.quit()
                browser0, handle = pickbrowser(browserchoice, True)
                browser0 = sellogin(Username, Password, browser0)
                counter = 1

        print "sending pm to " + membername2
        membername = "http://www.chess.com/members/view/" + membername2

        browser1, response = mecopner(browser1, membername)
        soup = BeautifulSoup(response)

        for placeholder in soup.find_all(class_ = "flag"):
            country = placeholder["title"]
        if country == "International":
            country = nnation

        name = namechecker(soup)
        if name == " ":
            name = membername2

        subject = streplacer(subjectorg, (["/name", name.strip()], ["/nation", country.strip()], ["/newline", "\n"]))

        for link in soup.find_all("a", href=True):
            if link.text == "Send a Message":
                memlink = link["href"]
                browser0.get("http://www.chess.com" + memlink)
                time.sleep(2)

        try:
            WebDriverWait(browser0, 10).until(EC.presence_of_element_located((By.ID, "c15")))
            browser0.find_element_by_name("c15").send_keys(subject)
        except Exception, errormsg:
            if supusr is True:
                print repr(errormsg)
            continue

        while True:
            try:
                browser0.switch_to_frame("tinymcewindow_ifr")
                browser0.find_element_by_id("tinymce").clear()
                browser0.switch_to_default_content()
                filtmcemsg(msglist, browser0, name, country, browserchoice)

                browser0.find_element_by_id("c16").click()
                break
            except Exception, errormsg:
                if supusr is True:
                    print repr(errormsg)
                print "\n\nRetrying " + membername2

                while True:
                    browser0.get("http://www.chess.com" + memlink)
                    try:
                        WebDriverWait(browser0, 10).until(EC.presence_of_element_located((By.ID, "c15")))
                        browser0.find_element_by_name("c15").send_keys(subject)
                        break
                    except Exception, errormsg:
                        if supusr is True:
                            print repr(errormsg)
                        print "retrying"

        time.sleep(sleeptime)
    browser0.quit()

    if shutdown == "y":
        turnofcomp()

def mecopner(browser, pointl):
    while True:
        try:
            response = browser.open(pointl)
            break
        except Exception, errormsg:
            if supusr is True:
                print repr(errormsg)
            print "something went wrong, reopening " + pointl
            time.sleep(1)
    return browser, response

def nineworker(infile, inid, logincookie, key):
    memlist = list()
    target = list()
    memlistorg = memfiop("mem/" + infile, key)

    counter = 1
    while counter <= 100:
        target.append("http://www.chess.com/groups/managemembers?id=" + inid + "&page=" + str(counter))
        counter += 1

    un = spider([target], logincookie, True)

    for member in memlistorg:
        if member not in un:
            memlist.append(member)

    if len(memlist) != 0:
        memlist = notclosedcheck(memlist)

    with open("mem/" + infile, "wb") as placeholder:
        placeholder.write(com2(key, str(un).replace("'", "").replace("[", "").replace("]", ""), 256, []))
    return memlist

def tmparchecker(pagelist, targetname):
    tmyear = enterint("\nOnly check tm's that has been open for registration since year, leave empty to skip (YYYY) ")
    if tmyear != "":
        tmmonth = enterint("\nOnly check tm's that has been open for registration since month (MM) ")
        tmday = enterint("\nOnly check tm's that has been open for registration since day (DD) ")

    tmpar = list()
    timeoutlist = list()
    winssdic = dict()
    losedic = dict()
    browser = mecbrowser("")
    print "\n\n"

    for page in pagelist:
        if "http://www.chess.com/groups/team_match?id=" not in page:
            continue
        print "processing: " + page
        alltmresults = list()
        counter2 = 0
        browser, response = mecopner(browser, page)
        soup = BeautifulSoup(response)

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
                print page + " didn't pass the timecheck"
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
                    placeholder = re.findall("http://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)
                    try:
                        placeholder = str(placeholder[0]).replace("http://www.chess.com/members/view/", "")
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
                    counter = 0
                    placeholder = str(placeholder)

                    if "menu-icons timeline right-8" in placeholder:
                        timeouts = placeholder.count('class="menu-icons timeline right-8" title="Timeout"')
                        while counter < timeouts:
                            timeouters1 = str(re.findall("http://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)[0]).replace("http://www.chess.com/members/view/", "")
                            timeoutlist.append(timeouters1)
                            counter += 1

            elif targetname == str(soupgroup[1]).replace("/groups/home/", ""):
                for placeholder in souppar[3::4]:
                    placeholder = str(placeholder)
                    placeholder = re.findall("http://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)
                    try:
                        placeholder = str(placeholder[0]).replace("http://www.chess.com/members/view/", "")
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
                    counter = 0
                    placeholder = str(placeholder)

                    if "menu-icons timeline left-8" in placeholder:
                        timeouts = placeholder.count('class="menu-icons timeline left-8" title="Timeout"')
                        while counter < timeouts:
                            timeouters1 = str(re.findall("http://www.chess.com/members/view/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", placeholder)[3]).replace("http://www.chess.com/members/view/", "")
                            timeoutlist.append(timeouters1)
                            counter += 1

            else:
                print "\n\nfailed to find your group in this match: " + page + "!!!\n"

        except IndexError:
            placeholder = list()
    return tmpar, timeoutlist, winssdic, losedic

def spider(target, logincookie, silent):
    browser = mecbrowser(logincookie)

    usrlist = list()
    for tlst in target:
        for pointer in tlst:
            browser, response = mecopner(browser, pointer)

            if "http://www.chess.com/groups/view/" in browser.geturl():
                break

            soup = BeautifulSoup(response)
            p2 = str(soup.find_all(class_ = "next-on"))
            if silent == False:
                print "checking " + pointer

            for link in browser.links(url_regex="chess.com/members/view/"):
                ltext = link.text
                if ltext != "View Profile":
                    usrlist.append(ltext.replace("[IMG]", ""))

            if "next-on" not in p2:
                break
    return list(set(usrlist))

def ageproc(target):
    while "" in target:
        target.remove("")
    browser = mecbrowser("")

    flist = []
    for targetx in target:
        print "checking: " + targetx
        tlst = [targetx]
        browser, response = mecopner(browser, "http://www.chess.com/members/view/" + targetx)

        if "://www.chess.com/members/view/" not in browser.geturl():
            continue
        soup = BeautifulSoup(response)

        birthdate = birthlister(soup)
        if birthdate == "":
            continue
        while "" in birthdate:
            birthdate.remove("")

        birthdate = map(int, [element.replace(",", "") for element in birthdate])
        flist.append(birthdate + tlst)
    return flist

def selbrowch():
    browserchoice = ""
    while browserchoice not in (["1", "2", "3", "4"]):
        browserchoice = raw_input("Which browser do you want to use\n 1. Firefox\n 2. Chrome\n 3. PhantomJS\n 4. Internet Explorer\nYour choice: ")
    return browserchoice

def inviter(choicelist, invitenum):
    choice2 = ""
    while choice2 not in (["y", "n"]):
        choice2 = raw_input("\n\nOnly invite those who fill a few requirements? (y/n) ")

    country = ""
    if choicelist[0] == "168":
        invgroup = ""
        if choice2 == "y":
            minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat = memprmenu()

        groupinv = raw_input("\nid of the group you want to send invites for: ")
        groupinv = "http://www.chess.com/groups/invite_members?id=" + groupinv
        infile = raw_input("name of the file containing your invites list: ")
        infile = "Invite Lists/" + infile
        alrfile = infile + " already invited"

        print "\n\n\n\nsupported commands, will be replaced with each members respective info\n /name - members name or username (if name is unavailable)\n /nation - members nation of origin\n /newline - pagebreak\n\n\n"
        msglist = list()
        choice = "y"
        while choice == "y":
            while choice not in(["1", "2", "3"]):
                choice = raw_input("\n\nAdd a snippet containing\n 1. Text\n 2. Image\n 3. Video\nYour choice: ")

            if choice == "1":
                text = raw_input("Enter the text: ")
            elif choice == "2":
                text = raw_input("Enter url of the image: ")
            elif choice == "3":
                text = raw_input("Enter url of the video: ")
            msglist.append((choice, text))

            while choice not in (["y", "n"]):
                choice = raw_input("add another snippet? (y/n) ")
        countryalt = raw_input("If member nation is International, use this instead: ")

    invinf = "no"
    if choicelist[0] == "42":
        invinf = "yes"
        choicelist = (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"])

    elif choicelist[0] == "84":
        choicelist = list()
        invinf = "yes"
        block = ""
        while block not in (["n"]):
            tempval = ""
            while tempval not in (["1", "2", "3", "4", "5", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]):
                tempval = raw_input("Group number: ")
            choicelist.append(tempval)
            block = raw_input("Add another group? (y/n) ")

    browserchoice = selbrowch()

    Username = raw_input("\n\n\nUsername: ")
    Password = raw_input("Password: ")

    browser2, handle = pickbrowser(browserchoice, True)
    browser2 = sellogin(Username, Password, browser2)

    logincookie = browser2.get_cookies()
    browser1 = mecbrowser(logincookie)

    lonl = [int(elem) for elem in str(date.today() - timedelta(days = 3)).split("-")]
    msin = [int(elem) for elem in str(date.today() - timedelta(days = 60)).split("-")]

    redo = "yes"
    counter = 1
    while redo == "yes":
        for choice5 in choicelist:
            if browserchoice == "1":
                counter += 1
                counted = "y"
                if counter > 70:
                    browser2.quit()
                    browser2, handle = pickbrowser(browserchoice, True)
                    browser2 = sellogin(Username, Password, browser2)
                    counter = 1

            invitenum2 = invitenum
            memint = list()

            if choice5 == "1": #Star Trek: The Dominion
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 20
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to The Dominion"
                groupinv = "http://www.chess.com/groups/invite_members?id=15896"
                infile = "Invite Lists/Star Trek: The Dominion"
                alrfile = "Invite Lists/Star Trek: The Dominion already invited"
                msglist = (("2", "http://4.bp.blogspot.com/_KcFkeN0I6po/SxKzhR0mUCI/AAAAAAAAEbE/jcE4_kPJu6Q/s1600/7of9.jpg"), ("1", "/newline/newlinePuzzles, Riddles, Chess!!!/newline/newlineThe largest Star Trek themed group on chess.com wants you, /name, for the grand Dominions /nation contingent/newline/newlineWith over 900 members we run vote chess, team matches, doubles chess and an in-house members league. Join now, and together we will impose order on this galaxy!!!/newline/newline"), ("2", "http://d1lalstwiwz2br.cloudfront.net/images_users/tiny_mce/RobinKarlsson/phpiGxzYM.jpeg"), ("1", "/newline/newlineA chess game is divided into three stages:/newlinethe first, when you hope you have the advantage/newlinethe second, when you believe you have an advantage/newlineand the third, when you know youre going to lose!/newline/newline"), ("3", "https://www.youtube.com/watch?v=JKPISUSOjiw"))

            elif choice5 == "2": #Karemma Ministry of Trade
                countryalt = ""
                minrat = 1700
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 80
                minwinrat = 0.5
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 8
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = ""
                heritage = ""
                memgender = ""
                invgroup = "to The Karemma"
                groupinv = "http://www.chess.com/groups/invite_members?id=26088"
                infile = "Invite Lists/Karemma Commerse Ministry"
                alrfile = "Invite Lists/Karemma Commerse Ministry already invited"
                msglist = (("1", "Hello /name. Welcome to the Karemma Commerce Ministry, the most influential trading organization of the gamma quadrant./newline"), ("2", "http://static1.wikia.nocookie.net/__cb20050911110619/memoryalpha/en/images/a/ab/Karemma_starship.jpg"), ("1", "/newlineThe Karemma are the merchants of the Dominion, responsible for the absolute majority of transportation and mercantile establishments throughout the gamma quadrant. And as the organization that negotiates trade agreements for this proud and powerful race, the Karemma Commerse Ministry power are rivaled only by the Founders/newline/newlineSo join us, and together we will see profits rise above our wildest expectations/newline"), ("3", "http://www.youtube.com/watch?v=FvGZzzNLnBY"))

            elif choice5 == "3": #The Breen Confederacy
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to The Breen Confederacy"
                groupinv = "http://www.chess.com/groups/invite_members?id=21974"
                infile = "Invite Lists/The Breen Confederacy"
                alrfile = "Invite Lists/The Breen Confederacy already invited"
                msglist = (("1", "Welcome, /name, to the grand Breen Confederacy's /nation contingent. An elite group aligned with the Dominion, specialising in votechess and thematic matches./newline/newline"), ("2", "http://images1.wikia.nocookie.net/__cb20061013002747/stexpanded/images/e/e4/BreenShip.jpg"), ("1", '/newline    "Never turn your back on a Breen"/newline/newline        -A Romulan saying/newline'), ("3", "http://www.youtube.com/watch?v=j2rH2Uh2MWs"))

            elif choice5 == "4": #The Cardassian Empire
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to The Cardassian Empire"
                infile = "Invite Lists/The Cardassian Empire"
                alrfile = "Invite Lists/The Cardassian Empire already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=20126"
                msglist = (("1", "Welcome, /name, to the Cardassian Empire, the strongest power in the Alpha Quadrant/newline/newline"), ("2", "http://static1.wikia.nocookie.net/__cb20061230121459/memoryalpha/en/images/2/24/Cardassia.jpg"), ("1", "/newline/newlineWelcome to our Capital world, Cardassia Prime, headed by our esteemed leader Gul Dukat. Our military might as well as inteliigence is SUPREME!/newline/newlineSo come and join us, and relish in our phenomenal victories!/newline/newline"), ("3", "http://www.youtube.com/watch?v=GiyXGQk_pc0"))

            elif choice5 == "5": #Death Star III
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Death Star III"
                infile = "Invite Lists/Death Star III"
                alrfile = "Invite Lists/Death Star III already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=17618"
                msglist = (("1", "Hello /name. Welcome to the Death Star, a Dynamically Dangerous Spacestation and Superweapon capable of Destroying an Entire Planet with its Powerful Superlaser../newline/newline"), ("2", "http://loyalkng.com/wp-content/uploads/2009/05/deathstarfiring2.jpg"), ("1", "/newlineThe Death Star has a crew of 265,675, as well as 52,276 gunners, 607,360 troops, 30,984 stormtroopers, and 180,216 pilots Its hangars contain assault shuttles, blastboats, Strike cruisers, land vehicles, support ships, and 7,293 TIE Fighters. It is protected by 10,000 turbolaser batteries, 2,600 Ion Cannons, and 768 Tractor Beam projectors./newline/newlineWelcome To Our Leader, Darth Vader :) Join us and together we will rule this galaxy!!!!/newline/newline"), ("3", "http://www.youtube.com/watch?v=4ImO0ST1WkM"))

            elif choice5 == "6": #Jungle Team
                minrat = 1300
                maxrat = ""
                mingames = ""
                minranrat = ""
                maxranrat = ""
                minwinrat = 0.25
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 15
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Jungle Team"
                infile = "Invite Lists/Jungle Team"
                alrfile = "Invite Lists/Jungle Team already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=17050"
                countryalt = "the outskirts of our Roman empire"
                msglist = (("1", "I invite you /name "), ("2", "http://d1lalstwiwz2br.cloudfront.net/images_users/tiny_mce/Teo_/phpIKXtlr.gif"), ("1", " to join the jungle team....have fun.....play teammatches and tournaments.... come and take a look/newline"), ("3", "http://www.youtube.com/watch?v=o1tj2zJ2Wvg"))

            elif choice5 == "7": #Legio XIII Gemina
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Legio XIII Gemina"
                infile = "Invite Lists/Legio XIII Gemina"
                alrfile = "Invite Lists/Legio XIII Gemina already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=22596"
                countryalt = "the outskirts of our Roman empire"
                msglist = (("1", "Augustus needs you, triarii /name, for the reconstituted legio XIII gemina. As a veteran of the disbanded 13th legion you have proven your worth in battle, and once more your skills are needed in defence against the barbarian hordes roaming /nation/newlineThis is your true destiny, will you answer the call of Rome and once more march toward victories that shall be legend!! Forever etching the name /name in history/newline/newline"), ("2", "http://3219a2.medialib.glogster.com/jessicaann77/media/bd/bdab41001c3686ad707a2050c9a41ba876e06939/xslegionrecruiting.jpg"), ("1", "/newline/newlinein 41 BC emperor Augustus reconstituted the thirteenth legion (dispanded 45 BC, following the final battle of Munda) to deal with the rebellion of Sextus Pompeius in Sicily./newlineThe legion thus acquired the cognomen Gemina (twin), after being reinforced with veteran legionnaries from other legions following the war against Mark Antony and the battle of Actium/newline"), ("3", "http://www.youtube.com/watch?v=kFmDt_E3WbU"))

            elif choice5 == "8": #Andromeda
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Andromeda"
                infile = "Invite Lists/Andromeda"
                alrfile = "Invite Lists/Andromeda already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=21262"
                countryalt = "international water"
                msglist = (("1", "Welcome to the Systems Commonwealth flagship, the Andromeda Ascendant, high guard recruit /name. As a human hailing from the geographical block that constituted /nation in the 21st century you have been selected for, if you choose to accept, special service onboard this Glorious Heritage-class heavy cruiser. As a crewmember of the Andromeda you will be taking part in rescue missions, map distant starsystems and conduct first contact missions with alien civilizations uneducated in the fine art of chess./newline/newline"), ("2", "http://www.sciforums.com/attachment.php?attachmentid=4853"), ("1", "/newline/newlineConstructed in CY 9768 Andromeda Ascendant is the tenth Glorious Heritage-class heavy cruiser, High Guard ship of the line, built by the Systems Commonwealth. And as such she is one of the bright stars of the High Guard fleet, capable of high-endurance, independent operations. Glorious Heritage-class ships are often called upon to perform disaster relief and refugee support operations due to their spacious interiors and ability to ferry large quantities of emergency supplies and additional personnel. They are also the preferred platform for first contact missions, given their formidable combat capabilities and their ability to operate without a battlegroup - often critical to assuring potential Commonwealth members that the High Guard comes in peace./newline/newline"), ("3", "http://www.youtube.com/watch?v=Y8uE-HXASuE"))

            elif choice5 == "9": #Tholian Assembly
                minrat = ""
                maxrat = ""
                minranrat = 1600
                maxranrat = ""
                mingames = ""
                minwinrat = ""
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "n"
                heritage = ""
                memgender = ""
                invgroup = "to the Tholian Assembly"
                infile = "Invite Lists/Tholian Assembly"
                alrfile = "Invite Lists/Tholian Assembly already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=29722"
                countryalt = "uncharted territories"
                msglist = (("2", "http://img4.wikia.nocookie.net/__cb20110905051618/memoryalpha/en/images/4/48/Tholian%2C_2155.jpg"), ("1", "/newline/newlineHey /name, I have heard that you like to play 960 chess. If that's the case I think you will love this new, elite 960 groups!/newline"), ("2", "http://i33.fastpic.ru/big/2013/0412/1c/d51339e321c2ca257d770294b1dbff1c.jpg"), ("1", "/newlineWe will be playing in exciting team matches, participate in group tournaments and most of all, have fun...... ;))/newlineSo join now, lend your talent to the Tholian Assembly and the name /name of /nation will forever be remembered throughout the vast expanse of the milky way/newline"), ("3", "http://www.youtube.com/watch?v=EEOqZsKAmCg"))

            elif choice5 == "10": #Space 1999
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Space 1999"
                infile = "Invite Lists/Space 1999"
                alrfile = "Invite Lists/Space 1999 already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=26614"
                msglist = (("2", "http://th07.deviantart.net/fs70/PRE/f/2011/331/8/2/moonbase_alpha_next_generation_by_heavy_fantasy-d4hg1v4.jpg"), ("1", "/newline/newlineWe want you, /name, for this rogue moons /nation settlement./newline/newline"), ("2", "http://upload.wikimedia.org/wikipedia/en/3/39/Space1999_Year1_Title.jpg"), ("1", "/newline/newlinePrimarily a scientific research station, Moonbase Alpha houses 311 personnel including scientists, astronauts, medical personnel, and security officers./newlineSpace: 1999: Nuclear waste from Earth, which was stored on the Moon's far side, explodes in a catastrophic accident on 13 September 1999, knocking the Moon out of orbit and sending it, and the 311 inhabitants of Moonbase Alpha, hurtling uncontrollably into space/newlineWATCH CLOSELY:))"), ("3", "http://www.youtube.com/watch?v=8WZW4groJro"))

            elif choice5 == "11": #Space 2099
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Space 2099"
                infile = "Invite Lists/Space 2099"
                alrfile = "Invite Lists/Space 2099 already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=26624"
                msglist = (("2", "http://th07.deviantart.net/fs70/PRE/f/2011/331/8/2/moonbase_alpha_next_generation_by_heavy_fantasy-d4hg1v4.jpg"), ("1", "/newline/newlineWe want you, /name, for this rogue moons /nation settlement./newline"), ("2", "http://www.thescifiworld.net/img/interviews/space2099_08-big.jpg"), ("1", "/newlinePrimarily a scientific research station, Moonbase Alpha houses 311 personnel including scientists, astronauts, medical personnel, and security officers./newlineSpace: 1999: Nuclear waste from Earth, which was stored on the Moon's far side, explodes in a catastrophic accident on 13 September 1999, knocking the Moon out of orbit and sending it, and the 311 inhabitants of Moonbase Alpha, hurtling uncontrollably into space/newlineWATCH CLOSELY:))"), ("3", "http://www.youtube.com/watch?v=8WZW4groJro"))

            elif choice5 == "12": #Chess Star Resort
                countryalt = "the International kingdom of Atlantis"
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to CSR"
                infile = "Invite Lists/CSR"
                alrfile = "Invite Lists/CSR already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=18514"
                msglist = (("2", "http://files.chesscomfiles.com/images_users/tiny_mce/Pepra/knightmoves.gif"), ("1", "/newline/newlineWelcome, /name, to Chess Star Resort. The one and only luxury 5 star hotel resort on chess.com/newlineJoin us, and experience all our activities firsthand... puzzles... team matches... tournaments and much much more/newline"), ("2", "http://www.washingtonpost.com/rf/image_606w/2010-2019/WashingtonPost/2013/10/18/Travel/Images/SALAMANDER20111382132477.jpg"), ("1", "/newlineCSR has since its founding just over a year ago housed some of the greatest chess players from many nations, including /nation. But without the great /name in our ranks, this hold little value/newline"), ("3", "http://www.youtube.com/watch?v=6_SqDur3IvQ"))

            elif choice5 == "13": #Magnus Carlsen group
                countryalt = ""
                minrat = ""
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 20
                minwinrat = 0.25
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to the Magnus Carlsen group"
                infile = "Invite Lists/The Magnus Carlsen Group"
                alrfile = "Invite Lists/The Magnus Carlsen Group already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=19744"
                msglist = (("2", "http://kevinthegerbil.com/images/blonde_chess.jpg"), ("1", "/newline/newlineWelcome /name to the Magnus Carlsen group. Magnus Carlsen was the third youngest GM in history at an age of 13 years, 4 months, 27 days! He has become the highest rated player in history before he reached 25 (years old) and he is on his way to becoming the world champion. He may also become the first person to reach and ELO of 3000. This is a group where we discuss his games and himself. We find out his strategies and then use them to win team matches and become the best in chess.com just like Magnus did!/newline"), ("3", "http://www.youtube.com/watch?v=ZD0Z0CwRDJw"))

            elif choice5 == "14": #October
                countryalt = ""
                minrat = 1900
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 20
                minwinrat = 0.25
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = ""
                heritage = ""
                memgender = ""
                invgroup = "to October"
                groupinv = "http://www.chess.com/groups/invite_members?id=11977"
                infile = "Invite Lists/October"
                alrfile = "Invite Lists/October already invited"
                msglist = (("2", "http://img0.joyreactor.com/pics/post/comics-chess-soldier-577272.jpeg"), ("1", "/newlinePuzzles, Riddles, Chess!!!/newline/newlineWinter is coming! and October wants you, /name, for this elite, high rated and fun-loving chess group/newline"), ("2", "http://kevinthegerbil.com/images/blonde_chess.jpg"), ("3", "http://www.youtube.com/watch?v=6_SqDur3IvQ"))

            elif choice5 == "15": #Knights of the Realm
                countryalt = "the uncharted territories"
                minrat = 1400
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 40
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Knights of the Realm"
                groupinv = "http://www.chess.com/groups/invite_members?id=23260"
                infile = "Invite Lists/Knights of the Realm"
                alrfile = "Invite Lists/Knights of the Realm already invited"
                msglist = (("2", "http://d1lalstwiwz2br.cloudfront.net/images_users/tiny_mce/thee_black_knight/phpUJ1yFu.gif"), ("1", "/newline/newlineWelcome to the Knights of the Realm, squire /name of /nation. The Knights set up fair team matches, vote chess matches, 960 matches and inhouse tournaments (Jousts). By fair matches, we mean that each individual game, has less than a 100 point rating difference./newline/newlineWe also have an analysis Department to post games in, and have them analyized, or maybe help to analyze the games of others. There is plenty of information to improve your game in the forums, and other interesting things./newline/newline/Lord Robin Karlsson/newline"), ("3", "http://www.youtube.com/watch?v=QMy6xsvxSfg"))

            elif choice5 == "16": #Stargate Command
                countryalt = ""
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.25
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 13
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "y"
                heritage = ""
                memgender = ""
                invgroup = "to Stargate Command"
                groupinv = "http://www.chess.com/groups/invite_members?id=21212"
                infile = "Invite Lists/Stargate Command"
                alrfile = "Invite Lists/Stargate Command already invited"
                msglist = (("2", "http://www.bullshift.net/data/images/2013/10/tumblr-m0ocvrknvb1qzrlhgo2-r1-500.gif"), ("1", "/newline/newlineWelcome, /name, to Stargate Command!!!/newline/newline"), ("2", "http://www.stargate-sg1-solutions.com/screencaps/AOT/23%20Under%20Siege/slides/AOT23180.jpg"), ("1", "/newline/newlineThe SGC base acts as the secure ground station for all Stargate activities. It is typically commanded by a Major General and is staffed by subject matter experts and military support personnel, several elite special operations teams, and several SG teams, including SG-1. Follow through through the Stargate, as we explore the universe of Chess.com. We will see many wonders,encounter friends and foes,and play brilliant chess in spectacular matches..../newlineand maybe even play some stargate golf, if time allow ;))/newline/newline"), ("3", "https://www.youtube.com/watch?v=MUBQLcKvcfI"))

            elif choice5 == "17": #Family Guy
                minrat = 1300
                maxrat = ""
                minranrat = ""
                maxranrat = ""
                mingames = 50
                minwinrat = 0.33
                lastloginyear = lonl[0]
                lastloginmonth = lonl[1]
                lastloginday = lonl[2]
                membersinceyear = msin[0]
                membersincemonth = msin[1]
                membersinceday = msin[2]
                youngeryear = ""
                youngermonth = ""
                youngerday = ""
                olderyear = ""
                oldermonth = ""
                olderday = ""
                timemax = 10
                maxgroup = ""
                mingroup = ""
                timovchoicemin = ""
                timovchoicemax = ""
                avatarch = "n"
                heritage = ""
                memgender = ""
                invgroup = "to Family Guy"
                infile = "Invite Lists/Family Guy"
                alrfile = "Invite Lists/Family Guy already invited"
                groupinv = "http://www.chess.com/groups/invite_members?id=14966"
                countryalt = "International water"
                msglist = (("1", "Welcome /name to the most awesome Family Guy fan club on chess.com... This is for everyone who likes family guy no matter if you're an alien or terran, from /nation or atlantis, a fan of Brian or Peter, we are all welcome./newline/newline"), ("2", "http://digitaljournal.com/img/1/4/8/8/6/8/i/5/8/6/o/family_guy.jpg"), ("1", "/newline/newlineWe are a happy bunch of people who like to come together and talk about our favorite FG episodes or jokes, recent events in the series and maybe even play a little bit of chess every now and then, to pass the time :))/newline/newline"), ("3", "http://www.youtube.com/watch?v=LhnRHOYRncc"))

            memtinv = remove_doublets(infile)
            #memalrinv = remove_doublets(alrfile)
            #memtinv = [x for x in memtinv if x not in memalrinv]

            already_picked = list()
            if invitenum2 > len(memtinv):
                invitenum2 = len(memtinv)

            while len(already_picked) < invitenum2:
                picked = random.choice(memtinv)

                if not picked in already_picked:
                    already_picked.append(picked)

            for member in already_picked:
                if choice2 == "y":
                    try:
                        passmemfil = memberprocesser(True, browser1, ([member]), minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat)
                    except UnboundLocalError:
                        continue
                    if member not in passmemfil:
                        memtinv.remove(member)
                        continue

                if browserchoice == "1":
                    if counted == "y":
                        counted = ""
                    else:
                        counter += 1
                    if counter > 70:
                        browser2.quit()
                        browser2, handle = pickbrowser(browserchoice, True)
                        browser2 = sellogin(Username, Password, browser2)
                        counter = 1

                browser1, response = mecopner(browser1, "http://www.chess.com/members/view/" + member)
                soup = BeautifulSoup(response)

                for placeholder in soup.find_all(class_ = "flag"):
                    country = placeholder["title"]
                if country == "International":
                    country = countryalt

                name = namechecker(soup)
                if name == " ":
                    name = member

                browser2.get(groupinv)

                try:
                    WebDriverWait(browser2, 5).until(EC.presence_of_element_located((By.ID, "c15")))
                    browser2.find_element_by_name("c15").send_keys(member)
                except:
                    break

                while True:
                    try:
                        print "\nInviting " + member + " " + invgroup
                        memint.append(member)

                        browser2.switch_to_frame("tinymcewindow_ifr")
                        browser2.find_element_by_id("tinymce").clear()
                        browser2.switch_to_default_content()

                        filtmcemsg(msglist, browser2, name, country, browserchoice)
                        browser2.find_element_by_id("c18").click()
                        break

                    except Exception, errormsg:
                        if supusr is True:
                            print repr(errormsg)
                        print "\n\nRetrying " + member + " " + invgroup + "!!!\n\n"
                        while True:
                            browser2.get(groupinv)
                            try:
                                WebDriverWait(browser2, 5).until(EC.presence_of_element_located((By.ID, "c15")))
                                browser2.find_element_by_name("c15").send_keys(member)
                                break
                            except Exception, errormsg:
                                if supusr is True:
                                    print repr(errormsg)
                                print "retrying"

            updinvlist = set(memtinv).difference(set(memint))
            updinvlist = misc1(updinvlist)
            memint = misc1(memint)

            with open(infile, "wb") as placeholder2:
                placeholder2.write(updinvlist)

            if len(memint) != 0:
                with open(alrfile, "ab") as placeholder3:
                    placeholder3.write(memint + ", ")

        if invinf == "no":
            browser2.quit()
            redo = "no"

def filtmcemsg(msglist, browser, name, country, browserchoice):
    for content in msglist:
        if content[0] == "1":
            #browser.execute_script("tinyMCE.activeEditor.insertContent('%s')" % streplacer(content[1], (["/name", name.strip()], ["/nation", country.strip()], ["/newline", " <br/>"])))

            browser.switch_to_frame("tinymcewindow_ifr")
            browser.find_element_by_id("tinymce").send_keys(streplacer(content[1], (["/name", name.strip()], ["/nation", country.strip()], ["/newline", "\n"])))
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
                    if supusr is True:
                        print repr(errormsg)
                    print "\n\nrefreshing page\n\n"
                    browser.refresh()

            browser.switch_to_window(browser.window_handles[0])
            time.sleep(1)

        elif content[0] == "3":
            browser.find_element_by_id("tinymcewindow_mce_media").click()
            alert = browser.switch_to_alert()
            alert.send_keys(content[1])
            alert.accept()
            time.sleep(1)

def login():
    Username = raw_input("Username: ")
    Password = raw_input("Password: ")

    if Username == "" or Password == "":
        return ""

    browserchoice = selbrowch()
    browser, handle = pickbrowser(browserchoice, True)
    browser = sellogin(Username, Password, browser)

    logincookie = browser.get_cookies()
    browser.quit()
    return logincookie

def misc1(sortedlines2):
    sortedlines2 = streplacer(str(sortedlines2), (["'", ""], ["set(", ""], [")", ""], ["(", ""], ["[", ""], ["]", ""]))
    return sortedlines2

def remove_doublets(filename):
    target = ""
    if os.path.isfile(filename) is True:
        if os.stat(filename).st_size > 0:
            for target in csv.reader(open(filename, "rb")):
                placeholder = target
    else:
        open(filename, "wb").close()
        target = ""
    return streplacer(str(OrderedDict.fromkeys((line for line in target if line)).keys()), (["' ", ""], ["'", ""], [",", ""], ["]", ""], ["[", ""], ["  ", " "])).split()

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
        browser, response = mecopner(browser, "http://www.chess.com/members/view/" + mem)
        if "://www.chess.com/members/view/" not in browser.geturl():
            continue

        soup = BeautifulSoup(response)
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
    return sorted(partup, reverse = True, key = lambda tup: tup[1])

def olprint(startc, endc, inchar, endn, nline):
    x = 0
    sys.stdout.write(startc)
    while x < endn:
        sys.stdout.write(inchar)
        x += 1
    sys.stdout.write(endc)
    sys.stdout.flush()
    if nline == True:
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

def memprmenu():
    minrat = enterint("\n\nMin (online chess) rating allowed. leave empty to skip: ")
    maxrat = enterint("Max (online chess) rating allowed. leave empty to skip: ")
    minranrat = enterint("Min (960) rating allowed. leave empty to skip: ")
    maxranrat = enterint("Max (960) rating allowed. leave empty to skip: ")
    mingames = enterint("\nMin number of games played (online chess). leave empty to skip : ")
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
    maxgroup = enterint("\nMax number of groups member may be in. leave empty to skip: ")
    mingroup = enterint("Min number of groups member may be in. leave empty to skip: ")

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
    return minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat

def makefolder(flst):
    for folder in flst:
        if not os.path.exists(folder):
            os.makedirs(folder)

def gettmlinklist(targetname, browser):
    linklist = list()

    browser, response = mecopner(browser, "http://www.chess.com/groups/matches/" + targetname + "?show_all_current=1")
    soup = BeautifulSoup(response)
    souplinks = re.findall("/groups/team_match(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(soup.find_all("a")))
    for link in souplinks:
        linklist.append("http://www.chess.com" + link)

    pointerlist = (0, 1, 2)
    for pointer in pointerlist:
        del linklist[-1]
    return linklist

def sellogin(Username, Password, browser):
    browser.get("https://www.chess.com/login")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "btnLogin")))

    browser.find_element_by_name("c1").send_keys(Username)
    browser.find_element_by_name("loginpassword").send_keys(Password)

    browser.find_element_by_id("btnLogin").click()
    time.sleep(1)
    return browser

def olprint2(tlen, middle, right, left):
    print right,
    print tlen.format(middle),
    print left

def vcman(vclinklist, yourside):
    browserchoice = selbrowch()
    browser3, handle = pickbrowser(browserchoice, True)
    browser3 = sellogin(raw_input("Username: "), raw_input("Password: "), browser3)

    logincookie = browser3.get_cookies()
    browser1 = mecbrowser(logincookie)

    parmemvc = Counter()
    for vcmatch in vclinklist:
        movelist = list()
        browser3.get(vcmatch)
        WebDriverWait(browser3, 10).until(EC.presence_of_element_located((By.ID, "c33")))
        browser3.find_element_by_id("c33").click()
        time.sleep(2)

        browser1, response = mecopner(browser1, vcmatch)
        soup = BeautifulSoup(response)

        if '      initialSetup: "",' not in str(soup):
            print "\n\n\nskipped " + vcmatch + "\n\n\n"
            continue

        boardpos = str(re.findall("boardFlip: (?:[a-zA-Z]|(?:%[a-fA-F]))+", str(soup.find_all(class_ = "chess_viewer")))[0]).replace("boardFlip: ", "")
        yourpos = soup.find_all(class_ = "playername")
        yourpos = (str(yourpos[0]).replace('<span class="playername">', "").replace("</span>", ""), str(yourpos[1]).replace('<span class="playername">', "").replace("</span>", ""))

        vcelem = browser3.find_elements_by_partial_link_text('')

        while yourside not in yourpos:
            yoursidechoice = ""
            while yoursidechoice not in (["1", "2"]):
                yoursidechoice = raw_input("\n\nCan't find your group in one of the games. Please specify which group is yours\n  1. " + yourpos[0] + "\n  2. " + yourpos[1] + "\nYour group is number: ")

            if yoursidechoice == "1":
                yourside = yourpos[0]
            if yoursidechoice == "2":
                yourside = yourpos[1]

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
            print "\nchecking " + pointer
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
                browser3.get(pointer)
                nextbtn = 2
                while True:
                    try:
                        browser3.find_element_by_css_selector('li.next-on>a').click()
                    except:
                        break
                    time.sleep(2)
                    print "\nchecking " + pointer + " page " + str(nextbtn)
                    vcelem = browser3.find_elements_by_partial_link_text("")
                    for curvcparmem in vcelem:
                        memsellink = curvcparmem.get_attribute("href") or ""

                        if "http://www.chess.com/members/view/" in memsellink:
                            user = re.sub(r"^http?:\/\/.*[\r\n]*", "", memsellink.replace("http://www.chess.com/members/view/", " ")).strip()
                            if user == "":
                                continue
                            if user in parmemvc:
                                parmemvc[user] += 0.5
                            else:
                                parmemvc[user] = 0.5
                    nextbtn += 1
    browser3.quit()
    return parmemvc

def memfiop(fipath, kem):
    if os.path.isfile(fipath) is True:
        if os.stat(fipath).st_size > 0:
            for placeholder in open(fipath, "rb"):
                mem = com3(kem, placeholder, 256, []).replace("\n", "").split(", ")
            return mem
    else:
        open(fipath, "wb").close
    return list()

def memberprocesser(silent, browser, target, minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat):
    target = streplacer(str(target), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""])).split(",")
    while "" in target:
        target.remove("")
    passmem = list()

    for targetx in target:
        if silent == False:
            print "checking " + targetx

        browser, response = mecopner(browser, "http://www.chess.com/members/view/" + targetx)
        try:
            if "://www.chess.com/members/view/" not in browser.geturl():
                continue
            soup = BeautifulSoup(response)

            if membersinceyear != "" or lastloginyear != "":
                memsinlist = memsin(soup)
                if memsinlist == "":
                    continue

                if lastloginyear != "":
                    lonln = memsinlist[1]
                    if datetime(lonln[0], lonln[1], lonln[2]) < datetime(lastloginyear, lastloginmonth, lastloginday):
                        continue

            if timemax != "":
                if timeoutchecker(soup) > timemax:
                    continue

            if timovchoicemax != "" or timovchoicemin != "":
                timemove = TimeMoveChecker(soup)

                if timovchoicemax != "":
                    if timemove[0] > timovchoicemax[0]:
                        continue
                    if timemove[1] > timovchoicemax[1] and timemove[0] >= timovchoicemax[0]:
                        continue
                    if timemove[2] > timovchoicemax[2] and timemove[1] >= timovchoicemax[1] and timemove[0] >= timovchoicemax[0]:
                        continue

                if timovchoicemin != "":
                    if timemove[0] < timovchoicemin[0]:
                        continue
                    if timemove[1] < timovchoicemin[1] and timemove[0] <= timovchoicemin[0]:
                        continue
                    if timemove[2] < timovchoicemin[2] and timemove[1] <= timovchoicemin[1] and timemove[0] <= timovchoicemin[0]:
                        continue

            if mingames != "" or minwinrat != "":
                gamestat = gamestats(soup)

                if mingames != "":
                    if gamestat[0] < mingames:
                        continue
                if minwinrat != "":
                    if gamestat[1] / gamestat[0]  < float(minwinrat):
                        continue

            if membersinceyear != "":
                memsi = memsinlist[0]
                if datetime(memsi[0], memsi[1], memsi[2]) > datetime(membersinceyear, membersincemonth, membersinceday):
                    continue

            if minrat != "" or maxrat != "":
                rating = onlratingchecker(soup)
                if minrat != "":
                    if rating < minrat:
                        continue
                if maxrat != "":
                    if rating > maxrat:
                        continue

            if minranrat != "" or maxranrat != "":
                rating = ranratingchecker(soup)
                if minranrat != "":
                    if rating < minranrat:
                        continue
                if maxranrat != "":
                    if rating > maxranrat:
                        continue

            if maxgroup != "" or mingroup != "":
                groupcount = groupmemlister(soup)

                if maxgroup != "":
                    if groupcount > maxgroup:
                        continue
                if mingroup != "":
                    if groupcount < mingroup:
                        continue

            if avatarch == "y":
                if AvatarCheck(soup) == False:
                    continue

            if youngeryear != "" or olderyear != "":
                birthdate = birthlister(soup)
                if birthdate == "":
                    continue
                while "" in birthdate:
                    birthdate.remove("")

                birthdate = [int(birthdate[2]), int(birthdate[0]), int(birthdate[1])]

                if youngeryear != "":
                    if datetime(birthdate[0], birthdate[1], birthdate[2]) < datetime(youngeryear, youngermonth, youngerday):
                        continue
                if olderyear != "":
                    if datetime(birthdate[0], birthdate[1], birthdate[2]) > datetime(olderyear, oldermonth, olderday):
                        continue

            if heritage != "":
                nation = nationlister(soup)

                if heritage not in nation:
                    continue

            if memgender != "":
                name = namechecker(soup)
                if name == " ":
                    continue
                name = name.split(" ")[0].lower()
                Found = "n"

                if memgender == "f":
                    with open("namelists/female", "rb") as fnlist:
                        for line in fnlist:
                            if name in line:
                                Found = "y"
                                break
                elif memgender == "m":
                    with open("namelists/male", "rb") as mnlist:
                        for line in mnlist:
                            if name in line:
                                Found = "y"
                                break
                if Found == "n":
                    continue

            passmem.append(targetx)
        except Exception, errormsg:
            if supusr is True:
                print repr(errormsg)
            print "\n\nskipped " + targetx + "\n\n"
            continue
    return passmem

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
                "nothing"
    return onrating

def ranratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Chess960" in str(x):
            try:
                onrating = int(x.text.replace("Chess960", "").strip())
            except ValueError:
                "nothing"
    return onrating

def tacratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Tactics" in str(x):
            try:
                onrating = int(x.text.replace("Tactics", "").strip())
            except ValueError:
                "nothing"
    return onrating

def lstanratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Live Chess - Standard" in str(x):
            try:
                onrating = int(x.text.replace("Live Chess - Standard", "").strip())
            except ValueError:
                "nothing"
    return onrating

def lbulratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Live Chess - Bullet" in str(x):
            try:
                onrating = int(x.text.replace("Live Chess - Bullet", "").strip())
            except ValueError:
                "nothing"
    return onrating

def lblitzratingchecker(soup):
    onrating = 0
    for x in soup.find_all(class_ = "clearfix stats-header"):
        if "Live Chess - Blitz" in str(x):
            try:
                onrating = int(x.text.replace("Live Chess - Blitz", "").strip())
            except ValueError:
                "nothing"
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
                "nada"
    return ratinglist

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
    return int(memgroups)

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

def memremoverf(un1):
    pointer = ""
    while pointer != "n":
        while pointer not in (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", ""]):
            pointer = raw_input("\nChose group to filter out\n 1. Star Trek: The Dominion\n 2. The Breen Confederacy\n 3. The Cardassian Empire\n 4. Death Star III\n 5. Karemma\n 6. Space 1999\n 7. Space 2099\n 8. Andromeda\n 9. Legio XIII Gemina\n 10. Utopia\n 11. Space Angels\n 12. Chess!\n 13. Carpe Diem\n 14. Chess Star Resort\n 15. Jungle Team\n 16. Family Guy\nYour choice: ")

        if pointer == "1":
            un1 = un1.difference(dommem)

        elif pointer == "2":
            un1 = un1.difference(memfiop("mem/breenmem", "keybreen"))

        elif pointer == "3":
            un1 = un1.difference(memfiop("mem/carmem", "keycarda"))

        elif pointer == "4":
            un1 = un1.difference(memfiop("mem/deathmem", "keydeath"))

        elif pointer == "5":
            un1 = un1.difference(memfiop("mem/karemma", "keykar"))

        elif pointer == "6":
            un1 = un1.difference(memfiop("mem/1999", "key1999"))

        elif pointer == "7":
            un1 = un1.difference(memfiop("mem/2099", "key2099"))

        elif pointer == "8":
            un1 = un1.difference(memfiop("mem/andromeda", "keyandromeda"))

        elif pointer == "9":
            un1 = un1.difference(memfiop("mem/legio", "keylegio"))

        elif pointer == "10":
            un1 = un1.difference(memfiop("mem/utopia", "keyutopia"))

        elif pointer == "11":
            un1 = un1.difference(memfiop("mem/angelmem", "keyangel"))

        elif pointer == "12":
            un1 = un1.difference(memfiop("mem/chessmem", "keyChess"))

        elif pointer == "13":
            un1 = un1.difference(memfiop("mem/CarpeDiemmem", "keyCD"))

        elif pointer == "14":
            un1 = un1.difference(memfiop("mem/CSR", "keyCSR"))

        elif pointer == "15":
            un1 = un1.difference(memfiop("mem/Jungle Team", "keyJT"))

        elif pointer == "16":
            un1 = un1.difference(memfiop("mem/Family Guy", "keyFG"))

        while pointer not in (["y", "n"]):
            pointer = raw_input("Filter out members from another group? (y/n)")
    return un1

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
        list1 = remove_doublets(list1)

        if mult == True:
            while list2 not in flist:
                list2 = raw_input(fdiag2)
            list2 = remove_doublets(list2)

    elif choice == "1":
        list1 = streplacer(raw_input(idiag1), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""])).split(",")
        if mult == True:
            list2 = streplacer(raw_input(idiag2), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""])).split(",")

    return list1, list2

def tlstcreator():
    targetlist = list()
    choice1 = ""
    while choice1 not in (["n"]):
        tlst = list()
        url1 = raw_input("\nPaste the url here: ")
        if "&page=" in url1:
            url1 = url1[0: url1.index("&page=")]
        url1 = url1 + "&page="
        start1 = enterint("\nEnter pagenumber to start on: ")
        stop1 = enterint("\nEnter pagenumber to end on: ")

        while start1 <= stop1:
            tlst.append(url1 + str(start1))
            start1 += 1
        targetlist.append(tlst)

        choice1 = ""
        while choice1 not in (["y", "n"]):
            choice1 = raw_input("\nDo you wish to process any additional targets? (y/n): ")
    return targetlist

def notclosedcheck(memlist):
    browser = mecbrowser("")
    memlist2 = list()
    for mem in memlist:
        browser, response = mecopner(browser, "http://www.chess.com/members/view/" + mem)
        soup = str(BeautifulSoup(response))

        if mem in soup:
            memlist2.append(mem)
    return memlist2

olprint("*", "*", "-", 72, True)
for content in (["", "", "", "RK Resource 001", "version 0.8.9 dev", "", "", ""]):
    olprint2("{0: ^70}", content, "|", "|")
olprint("|", "|", "-", 72, True)

for content in (["", "", "developed by Robin Karlsson", "", "", "Contact information", "", "r.robin.karlsson@gmail.com", "http://www.chess.com/members/view/RobinKarlsson", "", ""]):
    olprint2("{0: ^70}", content, "|", "|")
olprint("|", "|", "-", 72, True)

for content in (["", "", "Options", "Type /help or /help <number> for more info", "", "", "1. Extract the memberslist of one or more groups", "", "2. Build a csv file with data on a list of members", "", "3. Send invites for a group", "", "4. Posts per member in a groups finished votechess matches", "", "5. Build a csv file of a groups team match participants", "", "6. Filter a list of members for those who fill a few requirements", "", "7. Presentation of csv-files from options 2 and 5", "", "8. Process invite lists", "", "9. Look for members who has recenty left your group", "", "10. Count number of group notes per member in the last 100 notes pages", "", "11. Build a birthday schedule for a list of members", "", "12. Send a personal message to a list of members", "", "13. Pair lists of players against each others", "", "14. Set operations on two lists", "", "15. Check a teams won/lost tm's per opponent", "", ""]):
    olprint2("{0: ^70}", content, "|", "|")
olprint("*", "*", "-", 72, True)

pathway = "y"
makefolder((["mem", "Invite Lists", "namelists", "Webdriver", "Webdriver/Linux", "Webdriver/Mac", "Webdriver/Windows", "Webdriver/Linux/86", "Webdriver/Mac/86", "Webdriver/Windows/86", "Webdriver/Extensions", "Webdriver/Extensions/Chrome", "Webdriver/Extensions/Firefox"]))
dommem = memfiop("mem/dommem", "keydom")

while pathway in (["y"]):
    flow = ""
    while flow not in (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "42"]):
        flow = raw_input("\n\n\nEnter your choice here: ")

        if flow == "/help 1":
            print "\n\nCreates a list of members from one or more groups. Has the option to remove those who're also members of a specific group (using the members list built in option 9). The list can either be saved to a file or be directly printed onscreen\n\nOptional login if you wish to extract members from pages that arent public (for example the manage members page)"
        elif flow == "/help 2":
            print "\n\nBuild an excell compatible csv file with the following data on a list of members.\n\n Column 1: Username\n Column 2: Real name (if available on members homepage)\n Column 3. Live Standard rating\n Column 4. Live Blitz rating\n Column 5. Live Bullet rating\n Column 6. Online Chess rating\n Column 7. 960 rating\n Column 8. Tactics rating\n Column 9. Timeout-ratio\n Column 10. Last online\n Column 11. Member since\n Column 12. Time per move\n Column 13. Number of groups member is in\n Column 14. Points\n Column 15. Number of online chess games played\n Column 16. Number of online chess games won\n Column 17. Number of online chess games lost\n Column 18. Number of Online chess games drawn\n Column 19. Win ratio for online chess\n Column 20. Member nation (if available on members homepage)\n Column 21. If member has a custom avatar\n\nThis data can be presented and sorted using option 7 in the main script"
        elif flow == "/help 3":
            print "\n\nSend personalized invites for one or more groups. The invites can include text (with member name and nation, to personalize the message), pictures and videos.\n\nTo use this function you need to have a text document with a comma seperated list of members in the folder called 'Invite Lists'. The script sends an invite to each member in that file and creates a second file in the Invite Lists folder, with the usernames of those who has received an invite\n\n\nMembers who are present in the groups 'already invited' file will be skipped when sending invites. To block the script from inviting specific members you can add their names to the already invited file for the group in question, and they will be effectivily blocked\n\nWhen running the inviter with the option to only invite those who fill a few requirements the script will remove those who didn't fill the requirements from your invites list\n\nRequires the script to log in on chess.com, to send the invites from your account"
        elif flow == "/help 4":
            print "\n\nGoes through a groups finished, non thematic votechess matches and counts number of posts per member\n\nRequires the script to log in on chess.com, to acess comments in games"
        elif flow == "/help 5":
            print "\n\nBuild an excell compatible csv file with the following data on how each member who has ever played for a group has performed in the groups team matches\n\n Column 1. Username\n Column 2. Number of team matches member has participated in\n Column 3. Points won\n Column 4. Points lost\n Column 5. Ongoing games\n Column 6. Timeouts"
        elif flow == "/help 6":
            print "\n\nTakes a comma seperated list of members and sort out those who doesn't fill a few criterias regarding:\n\n Min online chess rating\n Max online chess rating\n Last online\n Member Since\n Older than (if birthdate is available on members profile)\n Younger than (if birthdate is available on members profile)\n Min number of groups member may be in\n Max number of groups member may be in\n Timeout-ratio\n Time per move\n If they have a custom avatar\n Gender, determined by comparing the members name to a list of male and female names"
        elif flow == "/help 7":
            print "\n\nPresentation of csv files from option 2 and 5. Can present data from the csv files sorted by any column, compare two csv files from option 5 to see what has changed or return the username of each member in the file and present it as a comma seperated list"
        elif flow == "/help 8":
            print "\n\nRemoves doublets from a textfile and has the option to remove those who are members of a specific group"
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
        elif flow == "/help":
            print "\n\n\nTo add extensions/addons to the scripts chrome or firefox browser you need to download the extension in crx format for chrome or xpi for firefox. Once the addon is downloaded, place it in the Webdriver/Extensions/Chrome or Webdriver/Extensions/Firefox folder.\n\nIt's recommended to use the adblock plus extension\n\n\n\n\nTo use the scripts ability to determine a members gender you will need to have a list of male and female first names in the namelists folder. male names should be stored in a file called 'male' and female names in a file called 'female'.\n\nFor best performance the names should be in the format:\nname1\nname2\nname3\netc\n\nIt's also recommended to sort the names based on how commonly they are used"

    if flow == "1":
        print "\n\n\nchess.com members list extractor\n"
        print "Locate the members list url of the group you wish to target.\n\n  example: http://www.chess.com/groups/membersearch?allnew=1&id=8893\n\nCopy the url.\n"
        target = tlstcreator()

        logincookie = login()
        un1 = set(spider(target, logincookie, False))

        remmem = ""
        while remmem not in (["y", "n"]):
            remmem = raw_input("\n\nFilter out members of a group? (y/n) ")

        if remmem == "y":
            un1 = memremoverf(un1)
        un1 = misc1(un1)

        choice6 = ""
        while choice6 not in (["1", "2"]):
            choice6 = raw_input("\n\nDo you wish to\n 1. Print the extracted names onscreen\n 2. Save them to a file\n\nEnter choice here: ")

        if choice6 == "1":
            print "\n\n" + un1

        elif choice6 == "2":
            memfile1 = raw_input("\nName of the file to which your list will be saved: ")
            with open(memfile1, "ab") as placeholder2:
                placeholder2.write(un1)

    elif flow == "2":
        target = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to check: ", "")[0]
        while "" in target:
            target.remove("")
        filename = raw_input("Name of the file to which your data will be saved: ")

        getmeminfo(target, filename)

    elif flow == "3":
        choice5 = ""
        while choice5 not in (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "42", "84", "168"]):
            choice5 = raw_input("\n\nWhich group would you like to send invites for?\n\n    Dominion affiliated groups:\n 1. Star Trek: The Dominion\n 2. Karemma Commerce Ministry\n 3. The Breen Confederacy\n 4. The Cardassian Empire\n 5. Death Star III\n\n    Non Dominion groups:\n\n 6. Jungle Team\n 7. Legio XIII Gemina\n 8. Andromeda\n 9. Tholian Assembly\n 10. Space 1999\n 11. Space 2099\n 12. Chess Star Resort\n 13. Magnus Carlsen group\n 14. October\n 15. Knights of the Realm\n 16. Stargate Command\n 17. Family Guy\n\n 42. endless loop that goes through all the groups, indefinitely\n 84. Create you own custom infinite loop from the supported groups\n 168. Send invites for another group\n\nEnter choice here: ")
        inviter(([choice5]), 200)

    elif flow == "4":
        yourside = raw_input("Name of group to check: ")
        vclinklist = getvclinks(yourside)
        parmemvc = vcman(vclinklist, yourside)

        for key, value in sorted(parmemvc.items(), key = itemgetter(1), reverse = True):
            print "\n" + key + " has made " + str(int(value)) + " posts"

    elif flow == "5":
        pathtm = ""
        while pathtm not in (["1", "2"]):
            pathtm = raw_input(" 1. Check all tm's for a group\n 2. Check a single tm\nYour choice: ")
        targetnameorg = raw_input("\n\n\nName of the group you wish to check: ")
        targetname = re.sub(r"[^a-z A-Z 0-9]","", targetnameorg)
        targetname = targetname.replace(" ", "-").lower()

        if pathtm == "1":
            targetnameorgf = targetnameorg
            pagelist = gettmlinks(targetname)
        elif pathtm == "2":
            pathtm = ""
            while pathtm not in (["1", "2"]):
                pathtm = raw_input("\n\n 1. Check the tm for results\n 2. Check match for members with a timeout-ratio above a specific value\nYour choice: ")
            pagelist = raw_input("team match id: ")
            targetnameorgf = "team match: " + pagelist + " ... "
            pagelist = (["http://www.chess.com/groups/team_match?id=" + pagelist])

        tmpar, tmtimeout, winssdic, losedic = tmparchecker(pagelist, targetname)

        if pathtm == "1":
            tmparcount = Counter(tmpar)
            tmtimeoutcount = Counter(tmtimeout)
            joined = {}
            membernamelist = list()

            outputfile = open(targetnameorgf + " " + strftime("%Y-%m-%d", gmtime()) + ".tm.csv", "wb")
            csvwriter = csv.writer(outputfile, delimiter = " ", quoting=csv.QUOTE_MINIMAL)

            for pointer in set(tmparcount.keys())|set(winssdic.keys())|set(losedic.keys())|set(tmtimeoutcount.keys()):
                joined[pointer] = (float(tmparcount.get(pointer, 0))/10 + (float(tmparcount.get(pointer, 0))*2 - float(winssdic.get(pointer, 0)) - float(losedic.get(pointer, 0)))*5/4 + float(winssdic.get(pointer, 0)) - float(losedic.get(pointer, 0)) - tmtimeoutcount.get(pointer, 0)*3, tmparcount.get(pointer, 0), winssdic.get(pointer, 0), losedic.get(pointer, 0), tmtimeoutcount.get(pointer, 0))

            csvwriter.writerow(("Member name", "tm's participated in", "points won", "points lost", "ongoing games", "timeouts", "win ratio"))

            for key, value in sorted(joined.items(), key = itemgetter(1), reverse = True):
                try:
                    winrat = value[2] / (value[3] + value[2])
                except ZeroDivisionError:
                    winrat = 0
                csvwriter.writerow((key, value[1], value[2], value[3], value[1]*2 - value[2] - value[3], value[4], winrat))

            choicetm = ""
            while choicetm not in (["y", "n"]):
                choicetm = raw_input("continue to remove those who dosn't fill your requirements? (y/n) ")

            if choicetm == "y":
                membernamelist = list()
                browser = mecbrowser("")
                for key in joined:
                    membernamelist.append(key)

                minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat = memprmenu()
                passmembers = memberprocesser(False, browser, membernamelist, minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat)
                joined2 = dict()
                membernamelist = list()
                for key in joined:
                    if key in passmembers:
                        joined2[key] = joined[key]

                csvwriter.writerow(("Member name (those who fill your requirements)", "tm's participated in", "points won", "points lost", "ongoing games", "timeouts", "win ratio"))

                for key, value in sorted(joined2.items(), key = itemgetter(1), reverse = True):
                    try:
                        winrat = value[2] / (value[3] + value[2])
                    except ZeroDivisionError:
                        winrat = 0
                    csvwriter.writerow((key, value[1], value[2], value[3], value[1]*2 - value[2] - value[3], value[4], winrat))
            outputfile.close()

        elif pathtm == "2":
            maxtmrat = int(raw_input("\n\nGet members with a timeout-ratio above: ").replace("%", ""))
            browser = mecbrowser("")

            deadbeatlist = list()
            for member in tmpar:
                print "checking " + member
                browser, response = mecopner(browser, "http://www.chess.com/members/view/" + member)
                if "://www.chess.com/members/view/" not in browser.geturl():
                    continue
                soup = BeautifulSoup(response)
                if timeoutchecker(soup) > maxtmrat:
                    deadbeatlist.append(member)
            print "\n\n\nThe following members has a timeoutratio above " + str(maxtmrat) + "%: " + streplacer(str(deadbeatlist), (["'", ""], ["[", ""], ["]", ""]))

    elif flow == "6":
        membernamelist = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to check: ", "")[0]
        browser = mecbrowser("")

        minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat = memprmenu()
        passmembers = memberprocesser(False, browser, membernamelist, minrat, maxrat, mingames, minwinrat, lastloginyear, lastloginmonth, lastloginday, membersinceyear, membersincemonth, membersinceday, youngeryear, youngermonth, youngerday, olderyear, oldermonth, olderday, timemax, maxgroup, mingroup, timovchoicemin, timovchoicemax, avatarch, heritage, memgender, minranrat, maxranrat)

        choice6 = ""
        while choice6 not in (["1", "2"]):
            choice6 = raw_input("\n\nDo you wish to\n 1. Print the names of those who fill your criterias onscreen\n 2. Save them to a file\n\nEnter choice here: ")

        if choice6 == "1":
            print "\n\n" + streplacer(str(passmembers), (["'", ""], ["[", ""], ["]", ""]))

        if choice6 == "2":
            memfile1 = raw_input("\nName of the file to which your list will be saved: ")
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
                    print " " + str(counter3) + ". " + fname
                    clist.append(str(counter3))
                    counter3 += 1
            elif choicepath == "2":
                if fname.endswith(".mem.csv"):
                    flist.append(fname)
                    print " " + str(counter3) + ". " + fname
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
                    choice5 = ""
                    while choice5 not in (["1", "2"]):
                        choice5 = raw_input("\n\nWhat part of the csv-file do you wish to inspect?\n 1. everyone who has ever plaid for said group\n 2. those who fill your requirements\n\nYour choice, young padawan? ")

                    if choice5 == "1":
                        for row in csvreader:
                            if row[0] == "Member name (those who fill your requirements)":
                                break
                            memlist.append(row)

                    elif choice5 == "2":
                        recorder = ""
                        for row in csvreader:
                            if row[0] == "Member name (those who fill your requirements)":
                                recorder = "yy"
                                row[0] = "Member name"

                            if recorder == "yy":
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
            print "\n\n" + "".join(element.ljust(colwidth) for element in (memlist[0][0], memlist[0][1] + " old", memlist[0][1] + " new", "difference")) + "\n"
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
        print "\n\n\nRemoves doublets and unwanted elements from your list (ie those who are either already members or banned/unwanted)\n\nFiles in directory:\n"
        flist = fnamenot(([".csv", ".py", ".pyc", ".log", "~"]), ".")

        preexlist = ""
        while preexlist not in flist:
            preexlist = raw_input("\nFull name of the file containing your invites list: ")

        un4 = set(remove_doublets(preexlist))
        un4 = memremoverf(un4)
        un4 = misc1(un4)

        with open(preexlist, "wb") as placeholder2:
            placeholder2.write(un4)

    elif flow == "9":
        choiceorg = ""
        while choiceorg not in (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "42", "168"]):
            choiceorg = raw_input("\nWhich group do you wish to check?\n 1. Star Trek: The Dominion\n 2. The Breen Confederacy\n 3. The Cardassian Empire\n 4. Death Star III\n 5. Karemma Ministry of Trade\n 6. Space 1999\n 7. Space 2099\n 8. Andromeda\n 9. legio XIII gemina\n 10. The Majestical Utopia\n 11. Space Angels\n 12. Chess!\n 13. Carpe Diem\n 14. CSR\n 15. Family Guy\n 16. Jungle Team\n\n 42. Check groups 1-10, 14-16\n 168. Check another group\n\nYour choice: ")
        print "\n\nWe will start by extracting the latest memberslist for your group\n"
        logincookie = login()

        if choiceorg == "42":
            choiceorg = (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "14", "15", "16"])
        else:
            choiceorg = ([choiceorg])

        for choice in choiceorg:
            if choice == "1":
                memlist = nineworker("dommem", "15896", logincookie, "keydom")
                group = "the Dominion"

            elif choice == "2":
                memlist = nineworker("breenmem", "21974", logincookie, "keybreen")
                group = "the Breen Confederacy"

            elif choice == "3":
                memlist = nineworker("carmem", "20126", logincookie, "keycarda")
                group = "the Cardassian Empire"

            elif choice == "4":
                memlist = nineworker("deathmem", "17618", logincookie, "keydeath")
                group = "Death Star III"

            elif choice == "5":
                memlist = nineworker("karemma", "26088", logincookie, "keykar")
                group = "Karemma Ministry of Trade"

            elif choice == "6":
                memlist = nineworker("1999", "26614", logincookie, "key1999")
                group = "Space 1999"

            elif choice == "7":
                memlist = nineworker("2099", "26624", logincookie, "key2099")
                group = "Space 2099"

            elif choice == "8":
                memlist = nineworker("andromeda", "21262", logincookie, "keyandromeda")
                group = "Andromeda"

            elif choice == "9":
                memlist = nineworker("legio", "22596", logincookie, "keylegio")
                group = "Legio XIII Gemina"

            elif choice == "10":
                memlist = nineworker("utopia", "23674", logincookie, "keyutopia")
                group = "Majestical Utopia"

            elif choice == "11":
                memlist = nineworker("angelmem", "18512", logincookie, "keyangel")
                group = "Space Angels"

            elif choice == "12":
                memlist = nineworker("chessmem", "18810", logincookie, "keyChess")
                group = "Chess!"

            elif choice == "13":
                memlist = nineworker("CarpeDiemmem", "14704", logincookie, "keyCD")
                group = "Carpe Diem"

            elif choice == "14":
                memlist = nineworker("CSR", "18514", logincookie, "keyCSR")
                group = "Chess Star Resort"

            elif choice == "15":
                memlist = nineworker("Family Guy", "14966", logincookie, "keyFG")
                group = "Family Guy"

            elif choice == "16":
                memlist = nineworker("Jungle Team", "17050", logincookie, "keyJT")
                group = "Jungle Team"

            elif choice == "168":
                group = raw_input("Name of group to check: ")
                groupid = raw_input("Groups id: ")
                memlist = nineworker(group, groupid, logincookie, "Custom")
                

            print "\n\nMembers who are no longer in " + group + ": " + streplacer(str(memlist), (["'", ""], ["[", ""], ["]", ""]))

    elif flow == "10":
        grcheck = raw_input("group to check: ")
        grcheck = re.sub(r"[^a-z A-Z 0-9]","", grcheck)
        grcheck = grcheck.replace(" ", "-").lower()
        grcheck = "http://www.chess.com/groups/notes/" + grcheck + "?page="
        logincookie = login()

        browser = mecbrowser(logincookie)

        target = list()
        counter = 1
        while counter <= 100:
            target.append(grcheck + str(counter))
            counter += 1

        notedic = dict()
        for targetp in target:
            print targetp
            browser, response = mecopner(browser, targetp)
            soup = BeautifulSoup(response)

            links1 = browser.links()
            for link in links1:
                ltext = link.text
                if "/members/view/" in str(link) and ltext != "View profile[IMG]":
                    if ltext in notedic:
                        notedic[ltext] += 1
                    else:
                        notedic[ltext] = 1
            soupbrake = str(soup.find_all(class_ = "next-on"))
            if soupbrake == "[]":
                break

        sorteddic = OrderedDict(sorted(notedic.items(), key = lambda x: x[1], reverse = True))

        for nam, num in sorteddic.items():
            print nam + " has made " + str(num) + " notes"

    elif flow == "11":
        target = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to check: ", "")[0]
        birthdaylist = ageproc(target)
        birthdsorter(birthdaylist)

    elif flow == "12":
        choice = ""
        while choice not in (["1", "2"]):
            choice = raw_input("\n\noptions:\n 1. send a pm to all members from a set of pages\n 2. pm members from a custom list\nYour choice, young padawan: ")
        if choice == "1":
            target = tlstcreator()
        elif choice == "2":
            target = file_or_input(False, "\n\nName of the file containing your list: ", "", "\n\nEnter list of members to pm: ", "")[0]
        pmdriver(target, choice)

    elif flow == "13":
        gchoice = ""
        while gchoice not in (["1", "2"]):
            gchoice = raw_input("\n\n 1. Pair a list of members against each others\n 2. Pair two lists of members to play each others\nChoice: ")

        if gchoice == "1":
            target = file_or_input(False, "\n\nName of the file containing your list of players: ", "", "\n\nEnter list of players: ", "")[0]
            while "" in target:
                target.remove("")

        elif gchoice == "2":
            name1org = raw_input("Name of group 1: ")
            target1 = file_or_input(False, "\n\nName of the file containing " + name1org + "'s players: ", "", "\n\nEnter " + name1org + "'s list of players: ", "")[0]
            while "" in target1:
                target1.remove("")
            name2org = raw_input("Name of group 2: ")
            target2 = file_or_input(False, "\n\nName of the file containing " + name2org + "'s players: ", "", "\n\nEnter " + name2org + "'s list of players: ", "")[0]
            while "" in target2:
                target2.remove("")

            target1, target2 = remcomelem(target1, target2)

        browser = mecbrowser("")

        choice = ""
        while choice not in (["1", "2", "3", "4", "5", "6"]):
            choice = raw_input("\nMake pairs based on\n 1. Live Standard\n 2. Live Bullet\n 3. Live Blitz\n 4. Online Chess\n 5. 960\n 6. Tactics\nYour choice: ")

        if gchoice == "1":
            partup = pairsorter(browser, target, choice)
            partup = zip(partup, partup[1:])[::2]
            for pair in partup:
                print pair[0][0] + " (" + str(pair[0][1]) + ") - " + pair[1][0] + " (" + str(pair[1][1]) + ")"

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

            print name1 + " - " + name2
            for pair in pairs:
                print pair[0][0] + " (" + str(pair[0][1]) + ") - " + pair[1][0] + " (" + str(pair[1][1]) + ")"

    elif flow == "14":
        choice14 = ""
        while choice14 not in (["1", "2", "3", "4"]):
            choice14 = raw_input("\n\nwhat would you like to get\n 1. Elements common to both lists (intersection)\n 2. Elements from both lists (union)\n 3. Elements in list 1 but not in list 2 (difference)\n 4. Elements in either list but not in both (symmetric difference)\nYour choice: ")

        list1, list2 = file_or_input(True, "\n\nName of file 1: ", "Name of file 2: ", "\n\nList1: ", "List2: ")

        if choice14 == "1":
            prlst = streplacer(str(list(set(list1).intersection(set(list2)))), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice14 == "2":
            prlst = streplacer(str(list(set(list1).union(set(list2)))), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice14 == "3":
            prlst = streplacer(str(list(set(list1).difference(set(list2)))), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))
        elif choice14 == "4":
            prlst = streplacer(str(list(set(list1).symmetric_difference(set(list2)))), ([" ", ""], ["(", ""], [")", ""], ["]", ""], ["[", ""], ["'", ""]))

        choice6 = ""
        while choice6 not in (["1", "2"]):
            choice6 = raw_input("\n\nDo you wish to\n 1. Print the data onscreen\n 2. Save it to a file\n\nEnter choice here: ")

        if choice6 == "1":
            print "\n\n" + prlst

        elif choice6 == "2":
            sfile = raw_input("\nName of the file to which your list will be saved: ")
            with open(sfile, "wb") as placeholder2:
                placeholder2.write(prlst)

    elif flow == "15":
        targetnameorg = raw_input("\n\n\nName of the group you wish to check: ")
        targetname = re.sub(r"[^a-z A-Z 0-9]","", targetnameorg)
        targetname = targetname.replace(" ", "-").lower()

        mtchlist = gettmopdata(targetname)
        parttup = list()
        winssdic = dict()
        losedic = dict()
        drawdic = dict()

        for tm in mtchlist:
            if tm[5] == "Won":
                if tm[2] in winssdic:
                    winssdic[tm[2]] += 1
                else:
                    winssdic[tm[2]] = 1

            elif tm[5] == "Lost":
                if tm[2] in losedic:
                    losedic[tm[2]] += 1
                else:
                    losedic[tm[2]] = 1

            elif tm[5] == "Draw":
                if tm[2] in drawdic:
                    drawdic[tm[2]] += 1
                else:
                    drawdic[tm[2]] = 1

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

        template = "|{0:" + str(width) + "}|{1:6}|{2:6}|{3:6}|{4:6}|"
        print "\n\n\n" + template.format(" Opponent name", "Won", "Lost", "Draw", "Total") + "\n" + template.format("-" * width, "-" * 6, "-" * 6, "-" * 6, "-" * 6)
        for tm in parttup:
            print template.format(tm[0], tm[1], tm[2], tm[3], tm[4])

    elif flow == "42":
        turnofcomp()

    pathway = ""
    while pathway not in (["y", "n"]):
        pathway = raw_input("\n\n\nRun again? (y/n) ")
