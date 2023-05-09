# AdobeLrToCSV
Simple and short Python Code to export your Adobe LightRoom to CSV and play with the data. I am not a developer and wanted to focus and share the key things to retrieve and massage data from the Adobe LightRoom catalogue.

Testing has been done on LightRoom Classic 12.3 Catalogue.
The key principle is the LightRoom Classic Catalogue just a SQLite3 db. With decent SQL knowledge, you can play with it as you want. I am sharing the query closest to my need.

The code should not make any modification to your catalogue. I still highly recommending to use a copy of your in production LightRoom catalogue and will not take any responsibility if anything bad happens.
USE AT YOUR OWN RISK !!

After long research in the db structure, I cannot find the file size. The workaround used is the last characters of AgLibraryFile.importHash seems to be the file size. 

All the rest is in the code as comments.
