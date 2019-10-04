import csv
import numpy as np


source_file = 'source/daily_tag_5131.csv'

def calculatePositiveGain(source_csv_path):
    list_of_rows = []
    with open(source_csv_path, newline='') as csvfile:
        tagReader = csv.reader(csvfile, delimiter=',')
        row_index = 0
        for row in tagReader:
            if row_index > 0:
                tag_row = np.array(row[1:],dtype = 'int')
                list_of_rows.append(tag_row)
            row_index += 1
    list_of_rows = np.array(list_of_rows)
    return list_of_rows

def cumulate(tagging):
    cumSet = []
    for i in range(len(tagging),0,-1):
        rowSet = []
        for j in range(len(tagging[0])):
            rowElement = np.sum(tagging[-i:,j])
            rowSet.append(rowElement)
        cumSet.append(rowSet)
    cumSet = np.array(cumSet)
    return cumSet

def norm(cumulatives):
    totals = cumulatives[0]
    non_zero_columns = len(totals[totals>0]) - 1
    normalized = cumulatives/totals
    normalized = np.array(normalized)
    return normalized, non_zero_columns

def calcGain(normalized):
    gainSet = []
    for i in range(len(normalized)-1):
        rowSet = []
        for j in range(1,len(normalized[0])):
            tot2 = normalized[i,0]
            tot1 = normalized[i+1,0]
            rev2 = normalized[i,j]
            rev1 = normalized[i+1,j]
            rowElement = (tot2-tot1)*(rev2-rev1-tot2+tot1)/2 + (rev1-tot1)*(tot2-tot1)
            rowSet.append(rowElement)
        gainSet.append(rowSet)
    gainSet = np.array(gainSet)
    return gainSet

def addGains(gains):

    row = []
    for i in range(len(gains[0])):
        col = gains[:,i]
        col = col[col>0]
        sum = col.sum()
        row.append(sum)
    row = np.array(row)
    return row

def avgGains(posGains,columns):
    return posGains.sum()/columns
    # averageGains = np.nanmean(posGains,axis=0)
    return averageGains

def main():
    global source_file

    tagging = calculatePositiveGain(source_file)
    cumulatives = cumulate(tagging)
    normalized, columns = norm(cumulatives)
    gains = calcGain(normalized)
    positive_gains = addGains(gains)
    average_gains = avgGains(positive_gains, columns)
    print(f'Average Gain [0.0 to 0.5]: {average_gains}')
    print(f'Average Normalized Gain [0.0 to 1.0]: {average_gains/0.5}')

main()