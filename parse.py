import re
import pandas as pd
from FindAuthor import *
from getDataPoint import *
from startsWithDateAndTime import *


parsedData = [] # An empty list for parsed data
conversationPath = 'Enter your text file here'
print(conversationPath)

with open(conversationPath, encoding="utf-8") as fp:
    fp.readline()
    fp.readline()
    messageBuffer = [] 
    date, time, author = None, None, None
    while True:
        line = fp.readline() 
        if not line: 
            break
        line = line.strip() 
        if startsWithDateAndTime(line):
            if len(messageBuffer) > 0: 
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) 
            messageBuffer.clear() 
            date, time, author, message = getDataPoint(line)
            if message != "<Media omitted>":  # The code works in case the media files are not exported.
                messageBuffer.append(message) 
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns = ['Date', 'Time', 'Author', 'Message'])

df['Date'] = pd.to_datetime(df['Date'])
print(df.head(5))
df = df.dropna()
df.to_csv('Whatsapp-Chats.csv') 
