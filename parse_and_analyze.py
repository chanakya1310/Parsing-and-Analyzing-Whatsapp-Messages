import re
import pandas as pd
from FindAuthor import *
from getDataPoint import *
from startsWithDateAndTime import *
from extract_emojis import *
import math
import numpy as np
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
import emoji


parsedData = [] # An empty list for parsed data
conversationPath = 'chats.txt'


with open(conversationPath, encoding="utf-8") as fp:
    fp.readline()
    fp.readline()
    messageBuffer = []
    date, time, author = None, None, None
    media = 0
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
            if message != "<Media omitted>":
                media += 1
                messageBuffer.append(message)
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns = ['Date', 'Time', 'Author', 'Message'])

df['Date'] = pd.to_datetime(df['Date'])

df = df.dropna()
df.to_csv('chats.csv')

# Performing Some Analysis on the data.

a = dict(df['Author'].value_counts())

print("Group Wise Stats:")
print("Total Number of Messages", len(df))
df["emojis"] = df["Message"].apply(extract_emojis) # A Column named emojis is created which contains emojis present in that specific message
emojis = list(df["emojis"])
total_emojis_used = 0
for i in emojis:
    total_emojis_used += len(i)
print("Total number of Emojis used in conversations are :", total_emojis_used)

URLPATTERN = r'(https?://\S+)'
df['urlcount'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
print("The total number of Links shared are:", np.sum(df.urlcount))
print("The total number of images shared are", media)
print()

labels = ['Total Messages', 'Total Emojis', 'Total Links', 'Total Images']
top = [len(df), total_emojis_used, np.sum(df.urlcount), media]
source = ColumnDataSource(data=dict(overall_stats = labels, stats = top, color=Spectral6))
sorted_labels = sorted(labels, key=lambda x: top[labels.index(x)])

# A Bar Graph plotted to see the overall stats
p = figure(
    x_range = sorted_labels,
    plot_height = 400,
    plot_width = 600,
    title = "Stats",
    tools = "hover",
    tooltips = "@overall_stats: @stats"
    )

p.vbar(
    x = 'overall_stats',
    top = 'stats',
    bottom = 0,
    width = 0.9,
    source = source,
    color = 'color'
)

names = np.array(list(a.keys()))
print("The number of people in the group are {} and their names are {}".format(len(names), names))

#Plotting a PieChart to view the proportion of total messages sent by each user.
data = pd.Series(a).reset_index(name='value').rename(columns={'index':'names'})
data['angle'] = data['value']/data['value'].sum() * 2 * math.pi
data['color'] = Category20c[len(a)]

p1 = figure(plot_height = 350, title = "Pie Chart", toolbar_location = None,
        tools = "hover", tooltips = "@names: @value")

p1.wedge(x = 0, y = 1, radius = 0.4,
        start_angle = cumsum('angle', include_zero=True), end_angle = cumsum('angle'),
        line_color = "white", fill_color = 'color', legend = 'names', source = data)

show(gridplot([[p],[p1]]))
