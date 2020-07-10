import re
import pandas as pd
from FindAuthor import *
from getDataPoint import *
from startsWithDateAndTime import *

# from utils.getDataPoint import *
# from utils.startsWithDateAndTime import *

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
#         print(line)
        if not line: 
            break
        line = line.strip() 
#         print(line)
        if startsWithDateAndTime(line):
#             print("True")
            if len(messageBuffer) > 0: 
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) 
            messageBuffer.clear() 
            date, time, author, message = getDataPoint(line)
            if message != "<Media omitted>":
                messageBuffer.append(message) 
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns = ['Date', 'Time', 'Author', 'Message'])

df['Date'] = pd.to_datetime(df['Date'])
print(df.head(5))
df = df.dropna()
df.to_csv('chats.csv')
