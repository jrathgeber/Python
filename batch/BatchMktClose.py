# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 06:52:28 2017

@author: Jason
"""

import sendMail;
import os;
import time
import ftplib
import FileReadingRE as FR
import configparser
from shutil import copyfile

config = configparser.ConfigParser()
config.read('C:\etc\properties.ini') 

gdurl = config['godaddy']['godaddy.url']
gduser = config['godaddy']['godaddy.user']
gdpass = config['godaddy']['godaddy.pass']

url = config['yahoo']['yahoo.url']
user = config['yahoo']['yahoo.user']
password = config['yahoo']['yahoo.pass']
server = config['yahoo']['yahoo.server']
port = config['yahoo']['yahoo.port']
username = config['yahoo']['yahoo.username']

#cc_list = ('jrathgeber@yahoo.com','rathgeber.webster@gmail.com')
cc_list = ('jrathgeber@yahoo.com')   

model = 'MaxAlphaLive'
timestr = time.strftime("%d%m%y")
session = ftplib.FTP(gdurl,gduser,gdpass)

# Backtest Js and download prices    
os.chdir('c:\\dep\\Mechanizd\\rightedge\\')

#send live MaxAlpha Output
with open('C:\dec\RightEdge\Systems\MaxAlphaLive\output.html', 'r') as f:
    data = str(f.read())
    sendMail.send_mail('jrathgeber@yahoo.com', cc_list, 'Max Alpha One Live', data, ['C:\dec\RightEdge\Systems\MaxAlphaLive\output.txt'], server, port, username, password)
    
    copyfile("C:\dec\RightEdge\Systems\\" + model + "\output.html", 'C:\dev\godaddy\\mech\output\RightEdge\\Live\\' + model + '_' + timestr + '.htm')  

    file = open('C:\dec\RightEdge\Systems\MaxAlphaLive\output.html','rb')
    session.storbinary('STOR /mech/output/RightEdge/Live/' + model + '_' + timestr + '.htm', file)     # send the file
    file.close()

    f.close();    
    
FR.fileReading("C:\dev\godaddy\\mech\output\RightEdge\\Live\\*.htm", 'C:\dev\godaddy\\mech\output\RightEdge\Live\RightEdgeResults.htm', 'Rightedge Live - Today')

fileSummary = open('C:\dev\godaddy\\mech\output\RightEdge\Live\RightEdgeResults.htm','rb')
session.storbinary('STOR /mech/output/RightEdge/Live/RightEdgeResults.htm', fileSummary)     # send the file
fileSummary.close()   
    
session.quit()
        
# Send Back Test    
exec(open('C:\\dep\\Mechanizd\\rightedge\\RightEdgeIB.py').read())
    
# Send Z7 Live Status    
with open('F:\Zorro\Zorro_19X\Log\Z7.htm', 'r') as f:
    data = str(f.read())
    sendMail.send_mail('jrathgeber@yahoo.com', 'jrathgeber@yahoo.com', 'Zorro Summary Z7', data, ['F:\Zorro\Zorro\Log\Z7.txt'],server, port, username, password)    
    
# Backtest Js and download prices    
exec(open('C:\\dep\\Mechanizd\\zorro\\BacktestJ.py').read())