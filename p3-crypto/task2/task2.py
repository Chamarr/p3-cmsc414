#!/usr/bin/env python

#./task2 task2.in

import sys
import itertools

filename = sys.argv[1]

# messageTypes = {
#     "07ef5a82d56d2e705d8905095db1de0e": "BALANCE",
#     "be541528f39789ef874969217b0a7caa": "TRANSFER",
#     "22138a921c15b539ded1b96c4cbb951b": "INVOICE" }

messageLength = {
    "BALANCE": 2,
    "TRANSFER": 5,
    "INVOICE": 4 }

success = False

orderings = list(itertools.permutations(list(messageLength.keys())))
orderingsidx = 0

while not success:
    print("new iteration", file = sys.stderr)
    messageCounts = { 
        "BALANCE": 0,
        "TRANSFER": 0,
        "INVOICE": 0 }

    messageTypeToValues = {
        "BALANCE": None,
        "TRANSFER": None,
        "INVOICE": None }

    messageValuesToTypes = {}

    currLineMessage = 1

    insideMessage = False

    currMessage = None

    currOrdering = orderings[orderingsidx]
    currOrderingidx = 0
    
    try:
        with open(filename, 'rb') as file:
            for lineNum in itertools.count(start=1):
                currBlock = file.read(16)
                if not currBlock:
                    if messageCounts["BALANCE"] >= 2 and messageCounts["TRANSFER"] >= 1 and messageCounts["INVOICE"] >= 1 and not insideMessage:
                        success = True
                    break
                currBlockHex = currBlock.hex()
                if currBlockHex in messageTypeToValues.values() and insideMessage:
                    break
                if currBlockHex in messageTypeToValues.values() and not insideMessage:
                    currLineMessage = 1
                    insideMessage = True
                    currMessage = messageValuesToTypes[currBlockHex]
                    messageCounts[currMessage] += 1
                    print(lineNum, currMessage, file = sys.stderr)
                if currBlockHex not in messageTypeToValues.values() and not insideMessage:
                    currLineMessage = 1
                    if currOrderingidx >= len(currOrdering):
                        break
                    currMessage = currOrdering[currOrderingidx]
                    currOrderingidx += 1
                    insideMessage = True
                    messageValuesToTypes[currBlockHex] = currMessage
                    messageTypeToValues[currMessage] = currBlockHex
                    messageCounts[currMessage] += 1
                    print(lineNum, currMessage, file = sys.stderr)
                if currBlockHex not in messageTypeToValues.values() and insideMessage:
                    currLineMessage += 1
                    if currLineMessage == messageLength[currMessage]:
                        insideMessage = False
    except FileNotFoundError:
        print("file not found", file = sys.stderr)
        break
    orderingsidx += 1

print("\nfinal answer:\n", file = sys.stderr)

try:
    with open(filename, 'rb') as file:
        while True:
            currBlock = file.read(16)
            if not currBlock:
                break
            currBlockHex = currBlock.hex()
            if currBlockHex in messageValuesToTypes:
                print(messageValuesToTypes[currBlockHex])
except FileNotFoundError:
    print("file not found", file = sys.stderr)