Developed by Robin Karlsson

contact: r.robin.karlsson@gmail.com

   chess.com/members/view/RobinKarlsson

===============

Requirements

- Python 2.7
- Libraries: Mechanize, BeautifulSoup, Selenium

===============

Instructions


Step 1.
 - download and install python 2.7, https://www.python.org/download/releases/2.7.7/

 - Once python is installed either download and tarball or install (using pip would be the simplest way to install them, https://pip.pypa.io/en/latest/index.html) the following libraries: mechanize, bs4 and selenium


Step 2.
 - Download and unpack the script, https://github.com/RobinKarlsson/RK-Resource-001/archive/master.zip

 - open a command prompt/terminal window and navigate to the unpacked folder

 - type python "RK Resource 001.py" to launch the script. It will now set up its file architecture


Step 3.
A few functions in the script requires a webdriver to function properly. The firefox driver comes with the selenium library so if you have firefox installed you're good to go.
If you prefer chrome over firefox you can download a chromedriver from http://chromedriver.storage.googleapis.com/index.html (or for ie, http://selenium-release.storage.googleapis.com/index.html).
Place the webdriver(s) in the folder /Webdriver/YOUR_OS/86


Step 4.
run the script again and you should be good to go ;))

ps. don't forget to update regularly



===============



Miscellaneous




After adding a new group for which you wish to do invites you must create an invites message! Go to the folder /Messages/Invite Messages. There should now be two files called "{Group Name} Standard message" and "{Group Name} Deserter message".

The Standard message will be used for members from your standard and priority invites lists, while the deserter message will be used for members from the invites list of members who has left (to find members who has left your group use option 9 in the script, if you use the same name when adding a new group for 9 as you did for the inviter members who has left your group will be automatically added to the invites list of members who has left).


Format of the invites messages should be as follows:
<Text>
By using the <Text> command followed by a newline you tell the script that what is entered here should be entered as raw text. 
<Image>
With this command we tell the script that this text should be entered as a image url, for example: http://d1lalstwiwz2br.cloudfront.net/images_users/avatars/RobinKarlsson_large.4.jpeg
<Video>
This text here is entered as a youtube video url, for example: http://www.youtube.com/watch?v=GY8YBF8dHQo



Text and images can be multiple times and they are written in the order you place them in the message file.


The text can include newlines, references to the members nation and name given on their profile through the commands:


 - /name = gets replaced with the name given on members profile, username if no name is given.
 - /nation = gets replaced with the members nation of origin (by modifying the file "/Invite Lists/Config/{Group Name}.ini" you can chooce what to use if member nation is international, plus set a few filters that will be used by the invites)
 - /newline = newline... do NOT add a newline by enter unless you're done with the current section!!! use the /newline command



example message:
<Text>
Hey /name, how is /nation?/newlineWe would love for you to come and join us here at etc
<Image>
image url
<Text>
some more text
<Video>
video url



===============


                 
                 
Options                                 

                                                                        
                                                                        

 1) Creates a list of members from one or more groups. Has the option to remove those who're also members of a specific group (using the members list built in option 9). The list can either be saved to a file or be directly printed onscreen          

                                                                        
 2) Build an excell compatible csv file with the following data on a list of members.


- Column 1: Username

- Column 2: Real name (if available on members homepage)

- Column 3. Live Standard rating

- Column 4. Live Blitz rating

- Column 5. Live Bullet rating

- Column 6. Online Chess rating

- Column 7. 960 rating

- Column 8. Tactics rating

- Column 9. Timeout-ratio

- Column 10. Last online

- Column 11. Member since

- Column 12. Time per move

- Column 13. Number of groups member is in

- Column 14. Points

- Column 15. Number of online chess games played

- Column 16. Number of online chess games won

- Column 17. Number of online chess games lost

- Column 18. Number of Online chess games drawn

- Column 19. Win ratio for  online chess

- Column 20. Member nation (if available on members homepage)

- Column 21. If member has a custom avatar


This data can be presented and sorted using option 7 in the main script

 

 3) Send personalized invites for one or more groups. The invites can include text (with member name and nation, to personalize the message), pictures and videos.                      
      

                                                        
 4) Goes through a groups finished, non thematic votechess matches and counts number of posts per member    
         

                                             
 5) Build an excell compatible csv file with the following data on how each member who has ever played for a group has performed in the groups team matches

- Column 1. Username

- Column 2. Number of team matches member has participated in

- Column 3. Points won

- Column 4. Points lost

- Column 5. Ongoing games

- Column 6. Timeouts   

- Column 7. Win ratio



 6) Takes a comma seperated list of members and sort out those who doesn't fill a few criterias regarding:

- Min online chess rating

- Max online chess rating

- Min 960 chess rating

- Max 960 chess rating

- Last online

- Member Since

- Older than (if birthdate is available on members profile)

- Younger than (if birthdate is available on members profile)

- Min number of groups member may be in

- Max number of groups member may be in

- Timeout-ratio

- Time per move

- If they have a custom avatar

- Gender   
       

                                                 
 7) Presentation of csv files from option 2 and 5. Can present data from the csv files sorted by any column, compare two csv files from option 5 to see what has changed or return the username of each member in the file and present it as a comma seperated list       



 8) Send personalized notes to either a comma seperated list of members or those who are present in a set of pages. The note can include text with the members real name (or username) and nation.



 9) At first run the script builds a list of members who are currently in your group.

At future runs the script will build a new memberslist of your group, look for members who are in the memberslist compiled during the last run but not in the latest run.

Removes those who has had their accounts closed or changed their names and print the result, which is the members who has left your group in the timeperiod between two runs         



 10) Count number of group notes per member in the last 100 notes pages 



 11) Takes a comma seperated list of members and builds a sorted birthday schedule of those who have their birthday visible on their profile          



 12) Send personalized personal messages to either a comma seperated list of members or those who are present in a set of pages. The message can include text (with the members real name and nation, to personalize the message) and images           



 13) Takes either one or two list of members and offer to pair them against each others based on rating.

If given one lists members will be paired against each other after the format, highest ranked vs second highest rank etc. For two lists the script takes each member in the shorter list and pair this member against whoever has the most similar rating in the longer list

Ratings can be Live Standard, Live Blitz, Live Bullet, Online chess, 960 or tactics      



 14) Perform set operations on two lists (union, intersection, difference, symmetric difference)



 15) Count number of wins, losses and draws per opponent in a teams team match archive



 16) Delete all group notes in a group
