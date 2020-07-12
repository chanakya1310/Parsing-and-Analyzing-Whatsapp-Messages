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

# Performing Some Analysis on the data.

print(df.head(5))
a = dict(df['Author'].value_counts())

names = np.array(list(a.keys()))
print("The number of people in the group are {} and their names are {}".format(len(names), names))

data = pd.Series(a).reset_index(name='value').rename(columns={'index':'names'})
data['angle'] = data['value']/data['value'].sum() * 2 * math.pi
data['color'] = Category20c[len(a)]

p = figure(plot_height = 350, title = "Pie Chart", toolbar_location = None,
        tools = "hover", tooltips = "@names: @value")

p.wedge(x = 0, y = 1, radius = 0.4,
        start_angle = cumsum('angle', include_zero=True), end_angle = cumsum('angle'),
        line_color = "white", fill_color = 'color', legend = 'names', source = data)

show(p)
