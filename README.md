# LittleScripts

This repo contain:
----UiPathEmailListener
A script that access and scrape a specific folder of your email continously in background; when the object of an unread email contain a specific key word, script trigger UiPath orchestrator by an api call, and add a new item (the content is the email's object) of a specific queue.

----LBSproject
3 different api call to the same website (https://edw.morningstar.com), manage the response and finally write it in a csv file to make it easier to read.

All this scripts work using a congif.json, customize it using your credential and information.
