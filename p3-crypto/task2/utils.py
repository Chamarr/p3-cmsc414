import sys
import itertools

messageTypes = ["BALANCE", "TRANSFER", "INVOICE"]

def getOrderings(messages):
    return list(itertools.permutations(list(messages)))

messageLength = {
    "BALANCE": 2,
    "TRANSFER": 5,
    "INVOICE": 4 }


def getMessageValuesToTypes(filename):
    success = False

    orderings = getOrderings(messageTypes)
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
                    if currBlockHex in messageValuesToTypes and insideMessage:
                        break
                    if currBlockHex in messageValuesToTypes and not insideMessage:
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

    return messageValuesToTypes

def getMessageTypesFromSession(filename, messageValuesToTypes):
    arr = []
    try:
        with open(filename, 'rb') as file:
            while True:
                currBlock = file.read(16)
                if not currBlock:
                    break
                currBlockHex = currBlock.hex()
                if currBlockHex in messageValuesToTypes:
                    arr.append(messageValuesToTypes[currBlockHex])
    except FileNotFoundError:
        print("file not found", file = sys.stderr)

    return arr


# print("\nfinal answer:\n", file = sys.stderr)

