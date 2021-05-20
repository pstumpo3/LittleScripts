# LittleScripts

This repo contain:
----an email listener: a script that access and scrape a specific folder of your email continously; when the object of an unread email contain a specific key word, script trigger the UiPath orchestrator by an api call, and add a new item (the content is the email's object) of a specific queue.

----3 different api call to the same website (https://edw.morningstar.com), manage the response and finally write it in a csv file to make it easier to read.

All this scripts work using a congif.json.
