import csv
import numpy as np


source_file = 'source/daily_tag_5625.csv'
threshold = 0.95

def loadUpCSV(source_csv_path):
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
    normalized = cumulatives/totals
    for i in range(len(totals)-1,0,-1):
        if totals[i] == 0:
            normalized = np.delete(normalized,i,axis=1)
    normalized = np.array(normalized)
    return normalized

def getReductions(normalized):
    global threshold
    reductions = []
    # print(f'cols indexes {1} to {len(normalized[0, :])-1}')
    # print(f'rows indexes {len(normalized[:,0])-1} to {1-1}')
    for colIndex in range(1, len(normalized[0, :])):
        foundReduction = False
        for rowIndex in range(len(normalized[:,0])-1,-1,-1):
            if not foundReduction:
                if normalized[rowIndex,colIndex] > threshold:
                    reductions.append(1-normalized[rowIndex,0])
                    # print(f'row,col: {rowIndex}, {colIndex}')
                    foundReduction = True

    reductions = np.array(reductions)
    return reductions

def main():
    global source_file

    tagging = loadUpCSV(source_file)
    cumulatives = cumulate(tagging)
    normalized= norm(cumulatives)
    reductions = getReductions(normalized)

    print(reductions)
    print()
    print(f'Minimum: {np.min(reductions)}')
    print(f'Median: {np.median(reductions)}')
    print(f'Mean: {np.mean(reductions)}')
    print(f'Max: {np.max(reductions)}')



main()