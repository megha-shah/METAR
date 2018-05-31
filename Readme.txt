 METAR:

 Steps to setup:
 1. Untar the tar.gz file
 2. Install Redis database
 3. Install pip
 4. cd METAR/
 5. Run "pip install -r requirements.txt"
 6. python flaskProject.py
 7. Open the browser and go to sample url - "http://localhost:5000/metar/info?scode=KSGS&nocache=1"

Information mentioned in the pdf:

pdf- http://chesapeakesportpilot.com/wp-content/uploads/2015/03/military_wx_codes.pdf

1. It is not neccessary that temperature group exist 
2. If temperature group exist, it must be just after the cloud group
3. The first three letters of each cloud group denote sky coverage and the first 3 letters must be anyone among these- SKC, FEW, SCT, BKN, OVC
4. Wind group will contain KT 

