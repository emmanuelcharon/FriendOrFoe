FriendOrFoe
===========

by Emmanuel Charon, Machine Learning engineer at Diffbot, and Chris Oliver, freelance designer.

FriendOrFoe is a tool to find web pages mentioning your page, and see if they agree with you on different topics.

Take a page corresponding to an article or a blog post, FriendOrFoe will:
    find the pages that link to this page using Mozscape,
    extract relevant data from those pages using Diffbot,
    analyze their text using Semantria,
    compare their sentiments to the reference url on intersecting topics.

Example of use, from the UNIX command line, using an example given in the repository:
    python FriendOrFoe.py allData_example1.json

To use the program for a page on the web, you will need to create an account for the different APIs used here: 
   Diffbot : diffbot.com
   Semantria : semantria.com
   Mozscape : moz.com

These 3 APIs have a free starter plan and will give you some keys to be able to use their service. 

Once you registered and have your keys, edit the file "keys.py" and put your 5 keys.
   
Now you can determine who are the friends and foes of any page on the web!

    python FriendOrFoe.py http://paulgraham.com/hubs.html



