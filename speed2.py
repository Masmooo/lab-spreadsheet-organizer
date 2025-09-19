import csv
import math

with open('lmao.csv', 'r+', newline='') as file:
    highestDeg = 0.0
    reader = csv.reader(file)
    next(reader)
    for row in reader :
        if float(row[len(row)-1]) > highestDeg :
            highestDeg = float(row[len(row)-1])
    
    if int(highestDeg + .5) % 2 == 0:
        # its an odd # with decimal between .5 and .999...
        highestDeg = int(highestDeg + .5)
    elif int(highestDeg) % 2 == 0 :
        # its an even #
        highestDeg = int(highestDeg)
    else : 
        # its an odd number with decimal between 0.0 and 0.499...
        highestDeg = int(math.floor(highestDeg / 2.0)) * 2

    print("highestDeg: " + str(highestDeg))
    numDegrees = int((highestDeg - 10) / 2)
    print("numDegrees: " + str(numDegrees))

    allCats = [[] for i in range(numDegrees + 1)]

    file.seek(0)
    reader2 = csv.reader(file)
    next(reader)

    firstTemp = True
    currIndex = 0

    numValidBurstsAfterThresh = 0
    checkValidBursts = False
    degThresh = 0
    last = False
    for row in reader2 :
        
        # when recently moved to the next degree threshold, check
        # if we've moved downward for the next 10
        if checkValidBursts :
            # is above previous thresh
            # print("Must be above: " + str(degThresh - 2.5))
            # print("Value is: " + str(row[len(row) - 1]))
            if float(row[len(row) - 1]) > degThresh - 2.5 :
                numValidBurstsAfterThresh += 1
                if numValidBurstsAfterThresh == 10 : #change the integer here to increase number of burst checks after threshold is crossed
                    checkValidBursts = False
                    numValidBurstsAfterThresh = 0
            # is below previous thresh, put all misplaced rows 1 index back
            else :
                if last :
                    break
                print("temperature went below threshold  between " + str(degThresh - 4) + " and " + str(degThresh - 2) + " after " + str(numValidBurstsAfterThresh) + " bursts, recategorizing")
                degThresh -= 2
                currIndex -= 1
                index = len(allCats[currIndex + 1]) - 1 - numValidBurstsAfterThresh
                falseRows = allCats[currIndex + 1][index:]
                numRowsToRemove = len(allCats[currIndex + 1])
                print("array size: " + str(numRowsToRemove))
                for i in range(numRowsToRemove) :
                    print("popping index " + str(len(allCats[currIndex + 1]) - 1))
                    allCats[currIndex + 1].pop(len(allCats[currIndex + 1]) - 1)

                for i in range(len(falseRows)) :
                    allCats[currIndex].append(falseRows[i])
                    checkValidBursts = False
                    numValidBurstsAfterThresh = 0

        # sets degThresh based on first row temperature
        if firstTemp :
            firstTemp = False
            degThresh = int(math.ceil(float(row[len(row) - 1]) / 2.0)) * 2
            if degThresh < 12 :
                degThresh = 12

        # if temp for row is below the next threshold, append to curr list of rows
        if float(row[len(row) - 1]) - float(degThresh) < -.5 :
            allCats[currIndex].append(row)
        # if crossed threshold, start checking for regressing temperature,
        # start appending to list of rows at next index
        else :
            checkValidBursts = True
            numValidBurstsAfterThresh = 0
            degThresh += 2
            currIndex += 1
            allCats[currIndex].append(row)
            if degThresh == highestDeg :
                last = True

    def getAvg(rows) :
        avgs = ['' for i in range(len(rows[0]))]
        for i in range(8) :
            sum = 0
            ind = 0
            if i == 7 :
                ind = 13
            else :
                ind = i + 5

            for j in range(len(rows)) :
                sum += float(rows[j][ind])
            
            avgs[ind] = sum / float(len(rows))

        return avgs

    for i in range(len(allCats)) :
        sortedFileName = 'all' + str((i*2) + 10) + '.csv'
        
        with open(sortedFileName, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerows(allCats[i])

            avgsRow = getAvg(allCats[i])
            csv_writer.writerow(avgsRow)
        