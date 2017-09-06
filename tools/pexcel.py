from imports import *

def printRows(name):
    print "Working with: ", name
    wb = openpyxl.load_workbook(name)
    sheets = wb.get_sheet_names()
    print "Which workbook would you like to work on?"
    for x in range(len(sheets)):
            print str(x+1), ") ", sheets[x]
    sheet = int(raw_input())-1
    print "Selected: ", str(sheets[sheet])
    ws = wb[sheets[sheet]]
    print ws
    current = "None"
    for row in tuple(ws.rows):
        if row[0].value:
            current = row[0].value
        for count in range(len(tuple(ws.columns))):
            print row[count].value
    print "Current: ", current

def combineCols(name):
    '''
    Should add ability to read sheet name and columns through args
    '''
    wb = openpyxl.load_workbook(name[0])
    print wb.get_sheet_names()
    ws = wb['Combined']
    current = "None"
    count = 1
    for row in ws.iter_rows(min_row=1, max_col=3):
        for cell in row:
            print(cell.value)
    for row in tuple(ws.rows):
        #print "Row: " + str(row)
        if row[0].value:
            current = str(row[0].value)
        if isinstance(row[1].value,datetime.datetime):
            row[1].value = str(row[1].value)
        temp = str(current + " - " + row[1].value.encode('utf-8'))
        #print "Temp: " + temp
        ws.cell(row=1, column=3)
        row[2].value = temp
        count+=1
        print row[2].value
    wb.save(name[0])
