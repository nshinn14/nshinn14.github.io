import csv

cols = ['EIN', 'totrevnue', 'totexpns']
with open('16eofinextractez.dat', 'r') as datfile:        
    table = []
    table.append(cols)
    line = datfile.readline()
    feed = line.split(' ')
    locEin = feed.index(cols[0])
    locTR = feed.index(cols[1])
    locTE = feed.index(cols[2])
    
    for line in datfile:
        feed = line.split(' ')
        newLine = [feed[locEin], feed[locTR], feed[locTE]]
        table.append(newLine)

with open('990Files2016.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	[writer.writerow(r) for r in table]