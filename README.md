RK Resource 001

Developed by Robin Karlsson

contact mail: r.robin.karlsson@gmail.com
contact chess.com: chess.com/members/view/RobinKarlsson

===============

Requirements

- Python 2.7
- Libraries: Mechanize, BeautifulSoup, Selenium

===============

Instructions

 1) install the required software, the libraries can either be installed to your system or tarballed
 
 2) get the script
 
 3) run the script
 
===============

At first run the script will set up its file architecture. Selenium webdrivers should be placed in the Webdriver/"YOUR_OS"/"BROWSER_YOU_USE" folder. Addons to the Webdriver goes to Webdriver/Extensions/"BROWSER_YOU_USE" folder

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



 6) Takes a comma seperated list of members and sort out those who doesn't fill a few criterias regarding:

- Min online chess rating

- Max online chess rating

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



 8) Removes doublets from a textfile and has the option to remove those who are members of a specific group                     


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
