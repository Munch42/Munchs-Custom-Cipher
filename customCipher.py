import random;
import string;
import math;

decryptFromFile = input("Would you like to decrypt a message from a file? (Y/n): ")

fileKey = ""
textToDecrypt = ""

if decryptFromFile.lower() == "y":
    print("If the file is in the current directory, please input the filename plus the extension such as .txt")
    print("If the file is located in another directory, please enter the ENTIRE path such as D:\\myFiles\\texttodecrypt.txt")
    filePath = input("Please enter path:\n")

    fileToDecrypt = open(filePath, "r")
    # We must remove the first 5 characters from the first line a.k.a the "Key: " section
    fileKey = fileToDecrypt.readline()[5:];
    fileKey = fileKey[:len(fileKey) - 1]
    # We must remove the first   characters from the second line a.k.a the "Encrypted or Decrypted Message: "
    textToDecrypt = fileToDecrypt.readline()[19:]
    textToDecrypt = textToDecrypt[:len(textToDecrypt) - 1]

    fileToDecrypt.close()

userKey = "";
createNewKeyInput = ""

if fileKey == "":
    createNewKeyInput = input("Would you like to create a new unique encryption key? (Y/n): ")
else:
    userKey = fileKey

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
# Note: for below with the \\ when it is printed, it comes out as two \ but it is actually stored as just one so it should not matter
inverseCharacters = ['~', '}', '|', '{', '`', '_', '^', ']', "\\", '[', '@', '?', '>', '=', '<', ';', ':', '/', '.', '-', ' ', ',', '+', '*', ')', '(', "'", '&', '%', '$', "#", '"', '!']

# Fix error and then go through all / 95 sections and change to the length of the string which should = 95
allCharactersString = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + " "
for number in numbers:
    allCharactersString += number

allCharactersStringLength = len(allCharactersString)
# print(len(allCharactersString)) = 85 without numbers or 95 With
# print(allCharactersString)

# These are the same so we can just use ascii_letters for both combined
# print(string.ascii_letters + "\n")
# print(string.ascii_lowercase + string.ascii_uppercase + "\n")
# This is just punctuation such as !@#$%^&*()-=
# print(string.punctuation);

def createUserKey(length):
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    # It takes a random character from a list created with the ascii characters and the digits for the length of n
    key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation + " ") for _ in range(length))
    return key

def getAlphabetLocation(character):
    char_pos = string.ascii_lowercase.find(character.lower())
    # We add 1 to get its original value in the alphabet
    char_pos += 1

    return char_pos

def getSymbolLocationInverse(symbol):
    symbol_pos = inverseCharacters.index(symbol)
    # We add 1 because it gives us its array position
    symbol_pos += 1

    return symbol_pos

def getAlphabetCharacterFromLocation(location):
    # Basically do the location / 26 - the whole number portion which has been multiplied by 26 to get the remaining position
    # For example, 65 / 26 = 2.5 - 2 = 0.5 x 26 = 13
    letterPos = (location / 26) - int((location / 26))
    letterPos = round(letterPos * 26)

    # Test Key: yICs%f,ov0/1,|dU
    # print(letterPos)
    # print(location)

    letter = string.ascii_uppercase[letterPos]

    return letter

def invertOffsets(offsetList):
    # This is a function to flip the sign of all offsets in a list
    editedOffsets = []

    for offset in offsetList:
        modifiedOffset = offset * -1
        editedOffsets.append(modifiedOffset)

    return editedOffsets

def addXToAllOffsets(offsetList, amount):
    # This is a function to add a specified amount (it may be negative so it may subtract said amount) to/from each offset in a list
    editedOffsets = []

    for offset in offsetList:
        changedOffset = offset + amount
        editedOffsets.append(changedOffset)

    return editedOffsets

def convertKeyToOffsets(key):
    # [5, 3, 16, 6, 2, 9, 4, 5, 30, 39, 13, 1, 26, 3, 29, 5] Same Key
    # [5, 3, 16, 6, 2, 9, 4, 5, 30, 39, 13, 1, 26, 3, 29, 5] Same Key
    # [-37, 28, 15, -37, 9, -36, 1, 8, 20, -2, -3, -35, 4, -28, 11, 28] Different Key

    offsets = []
    finalOffsets = []
    # Follow rules laid out in CipherIdea.txt to convert all of the characters in the key to valid offsets for the text.
    symbolCount = 0
    lowercaseCount = 0
    uppercaseCount = 0
    numberSum = 0

    for character in key:
        if character in string.ascii_lowercase:
            lowercaseCount += 1
        elif character in string.ascii_uppercase:
            uppercaseCount += 1
        elif character in string.punctuation + " ":
            symbolCount += 1
        elif character in numbers:
            num = int(character)
            numberSum += num

    # print(symbolCount)
    # print(lowercaseCount)
    # print(uppercaseCount)
    # print(numberSum)

    for character in key:
        if character in string.ascii_lowercase:
            # Lowercase Character
            # print("Lowercase")
            char_pos = getAlphabetLocation(character)

            # We then add 0.5 times the symbol count rounded off to the character position to get the offset for this portion
            offset = char_pos + round((0.5 * symbolCount))

            offsets.append(offset)
        elif character in string.ascii_uppercase:
            # Uppercase Character
            # print("Upper")
            char_pos = getAlphabetLocation(character)

            # We then add (pi * (the sum of all numbers in the key - half of the keys length) rounded to the char_pos
            offset = round(char_pos + (math.pi * (numberSum - len(key))))

            offsets.append(offset)
        elif character in numbers:
            # Number
            # print("Number")
            number = int(character)

            offset = number - round(0.5 * lowercaseCount)

            offsets.append(offset)
        elif character in string.punctuation + " ":
            # Punctuation
            # print("Symbol")
            symbol_pos = getSymbolLocationInverse(character)

            # We then divide the the symbol's location by pi and round it
            offset = round(symbol_pos / math.pi)

            offsets.append(offset)

    # Now we possibly inverse the output
    # If the total number of uppercase letters is even then it stays the same while if it is odd, it inverses the offsets
    if (uppercaseCount % 2) != 0:
        # It is odd. If it was == to 0 then it would be even
        for offset in offsets:
            finalOffsets.append((offset * -1))
    else:
        finalOffsets = offsets

    return finalOffsets

def applyOffsets(offsetList, text):
    finalText = ""

    # We start at -1 because it adds one at the beginning no matter what and we want to start at 0
    curOffsetPos = -1
    maxOffsetPos = len(offsetList) - 1
    totalCharactersMoved = 0
    # previousSwapCharNum = 0
    # If charType = -1 then it is alphabet
    # If charType = 1 then it is symbols
    # charType = -1
    # We take the value of the last offset and then make sure that it is positive and not equal to 0
    # swapCharactersThreshold = offsetList[-1]

    # if swapCharactersThreshold < 0:
    #    swapCharactersThreshold *= -1
    # elif swapCharactersThreshold == 0:
    #    swapCharactersThreshold = 1

    for character in text:
        if curOffsetPos >= maxOffsetPos:
            curOffsetPos = 0
        else:
            curOffsetPos += 1

        # XTU9rpk"$jHrsm3<
        # print(allCharactersString)

        originalPos = allCharactersString.find(character)
        # print(originalPos)
        offsetPos = originalPos + offsetList[curOffsetPos]
        # print(offsetPos)
        offsetPos = (offsetPos / allCharactersStringLength) - int((offsetPos / allCharactersStringLength))
        offsetPos = round(offsetPos * allCharactersStringLength)
        letter = allCharactersString[offsetPos]

        finalText += letter

        # print(allCharactersString)
        # print(originalPos)
        # print(offsetPos)
        # print(letter)
        # print(finalText)

        totalCharactersMoved += 1

        # if swapCharactersThreshold == 1:
        # If it is every character, we just swap it
        # charType *= -1
        # Otherwise, we check to see if we have reached the next threshold and then if we do we add to the previous threshold number and swap the type
        # elif (totalCharactersMoved / swapCharactersThreshold).is_integer():
        #    if (totalCharactersMoved / swapCharactersThreshold) > previousSwapCharNum:
        #        previousSwapCharNum += 1
        #        charType *= -1

        # if charType == -1:
        #    # Alphabet
        #    if character in string.ascii_letters:
        #        # This is the position in the alphabet and the new position that it will be at in the alphabet
        #        position = getAlphabetLocation(character)
        #        position += offsetList[curOffsetPos]

        #        letter = getAlphabetCharacterFromLocation(position)

        #        finalText += letter

        #        print(finalText)
        #   elif character in string.punctuation:
        #        # This is some arbitrary position
        #        position = 6
        # elif charType == 1:
        #    # Symbols
        #    print("Symbols")

    return finalText

def decodeText(keys, encText):
    # This is a list of lists with the offsets for each key-
    reversedKeyOffsets = []
    characterCount = 0
    offsetCount = 0
    decodedMessage = ""

    for key in keys:
        offsets = convertKeyToOffsets(key)
        reversedKeyOffsets.append(invertOffsets(offsets))

    keyLength = len(reversedKeyOffsets[0])
    # print(reversedKeyOffsets[0][0])

    for char in encText:
        currentPositionInChars = allCharactersString.find(char)
        if int(characterCount / keyLength) > (len(reversedKeyOffsets) - 1):
            # If we are on the 11th key or more which don't exist we reset to 0 character count
            characterCount = 0

        # We get the current position and then the key that we are on which is the whole number portion of the char count divided by the key length
        # From there, we can then get the offset we want which is just the offset we are on starting at 0 and then incremented until 15 where we reset it
        # print(keys)
        # print("/")
        # print(reversedKeyOffsets)
        # print("|")
        # print(offsetCount)
        # print("||")
        # print(reversedKeyOffsets[int(characterCount / keyLength)])
        # print("|||")
        # print(reversedKeyOffsets[int(characterCount / keyLength)][offsetCount])
        # print("||||")

        originalPosition = currentPositionInChars + reversedKeyOffsets[int(characterCount / keyLength)][offsetCount]
        originalLetterPos = (originalPosition / allCharactersStringLength) - int((originalPosition / allCharactersStringLength))
        originalLetterPos = round(originalLetterPos * allCharactersStringLength)
        letter = allCharactersString[originalLetterPos]

        # <Wx1&!\:3[])N>W\
        # Hello there my cat named Phinei!
        # K}wnu7vlktg5IB:e95_j8idb[OhfEd_Z

        decodedMessage += letter

        # If we are on the last offset, then we go back to the next offset as we also go to the next key
        if offsetCount >= (keyLength - 1):
            offsetCount = 0
        else:
            offsetCount += 1

        characterCount += 1

    return decodedMessage

if createNewKeyInput.lower() == "y":
    userKey = createUserKey(16);
    print("Your new key is: " + userKey);

if userKey == "":
    userKey = input("Please input your user key to begin the encryption or decryption process:\n");

saveKey = input("Would you like to save your key and message to a file? (Y/n): ")
fileName = ""

if saveKey.lower() == "y":
    fileName = input("What would you like the file to be named including the file extension such as .txt?\n")
    global resultFile
    resultFile = open(fileName, "w")
    resultFile.write("Key: " + userKey + "\n")

operationType = ""

if fileKey == "":
    operationType = input("Would you like to encrypt (1) or decrypt (2) some text?\n")
else:
    operationType = "2"

# keyOffsets = convertKeyToOffsets(userKey)
# print(keyOffsets)

# Key: hF&T9qq&xaPG%%&r
# Output: KlLBKYZQ)MEwVWX*!B"R!/:']#5|lmnzq2rhqEFwOskcBCDPGhHx7klcu91^h0i?9,}!*\b.~-"T/3> {Y[*@7
# Second Key Try: KlLBKYZQ)MEwVWX*!B"R!/:']#5|lmnzq2rhqEFwOskcBCDPGhHx7klcu91^h0i?9,}!*\b.~-"T/3> {Y[*@7
# Key 2: XL_BsW<;g_hd@;>~
# Output 2: a E]"eLMTLWTQSSPqfU8<u"#*"mjgiif\-k%H`rszrCzwyyv7{A?n(89f8ifc6d!&P\g_D}*;,>;*~/-SC:p6T
# Second Key Try 2: a E]"eLMTLWTQSSPqfU8<u"#*"mjgiif\-k%H`rszrCzwyyv7{A?n(89f8ifc6d!&P\g_D}*;,>;*~/-SC:p6T

# text = applyOffsets(keyOffsets, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12345678910!~`@#$%^%&*()&_+-=/.,:?")
# print(text)

# keyList = [userKey]

# decodedText = decodeText(keyList, text)
# print(decodedText)

keys = []
firstKey = False

for x in range(10):
    if x == 0:
        firstKey = True
    else:
        firstKey = False

    previousKey = ""

    if firstKey:
        previousKey = userKey
    else:
        previousKey = keys[x - 1]

    previousOffsets = convertKeyToOffsets(previousKey)
    newKey = ""

    offsetToCheck = -2

    if len(previousOffsets) <= 1:
        offsetToCheck = -1

    if (previousOffsets[offsetToCheck] / 3).is_integer():
        # Inverse the order of the offsets of the previous key and apply them back to previous key
        reversedPreviousOffsets = invertOffsets(previousOffsets)

        newKey = applyOffsets(reversedPreviousOffsets, previousKey)
    elif previousOffsets[offsetToCheck] % 2 != 0:
        # It is odd so add 2 to all offsets and apply to previous key
        addedPreviousOffsets = addXToAllOffsets(previousOffsets, 2)

        newKey = applyOffsets(addedPreviousOffsets, previousKey)
    else:
        # Use the offsets made by the key to get a new key
        newKey = applyOffsets(previousOffsets, previousKey)

    keys.append(newKey)

# print("Keys: ")
# print(keys)
# print("^^^^^")

# +^Y{d:"9,KaU{OgA
# ["&^X|8-T4'X8X|X8X", '/`q}f=i8:qfq}qfq', ')^7|7/74+777|777', '=|f f[f0>fff fff', '/{7^7>7d:777^777', '[~f|f^fm[fff|fff', '>~7{7\\77>777{777', '^1f~f{ff^fff~fff', '`|n~n|nn`nnn~nnn', '~ G1G GG~GGG1GGG']
# ["&^X|8-T4'X8X|X8X", '/`q}f=i8:qfq}qfq', ')^7|7/74+777|777', '=|f f[f0>fff fff', '/{7^7>7d:777^777', '[~f|f^fm[fff|fff', '>~7{7\\77>777{777', '^1f~f{ff^fff~fff', '`|n~n|nn`nnn~nnn', '~ G1G GG~GGG1GGG']

# print(convertKeyToOffsets("&^X|8-T4'X8X|X8X"))
# print("----------------------------------")
# print(convertKeyToOffsets('/`q}f=i8:qfq}qfq'))

print("------- Initiating Process -------")
if operationType == "1":
    encryptFromFile = input("Would you like to encrypt a message from a file? (Y/n): ")

    textToEncrypt = ""

    if encryptFromFile.lower() == "y":
        print("If the file is in the current directory, please input the filename plus the extension such as .txt")
        print("If the file is located in another directory, please enter the ENTIRE path such as D:\\myFiles\\texttoencrypt.txt")
        filePath = input("Please enter path:\n")

        fileToEncrypt = open(filePath, "r")
        textToEncrypt = fileToEncrypt.read();

        fileToEncrypt.close()
    else:
        textToEncrypt = input("Please enter the text that you would like to encrypt in accordance with your key:\n")

    totalSections = len(textToEncrypt) / len(userKey)
    if not totalSections.is_integer():
        totalSections = int(totalSections) + 1
    totalSections = int(totalSections)

    keyRepeats = totalSections

    currentKey = 0
    currentPos = 0
    encryptedText = ""
    for i in range(keyRepeats):
        keyToUse = keys[currentKey]
        keyOffsetsToUse = convertKeyToOffsets(keyToUse)
        currentEncryptingPhrase = ""

        for y in range(len(userKey)):
            if currentPos >= len(textToEncrypt):
                break

            currentEncryptingPhrase += textToEncrypt[currentPos]

            currentPos += 1

        encryptedText += applyOffsets(keyOffsetsToUse, currentEncryptingPhrase)

        if currentKey >= 9:
            currentKey = 0
        else:
            currentKey += 1

    print("Your encrypted text is: " + encryptedText)

    try:
        resultFile
    except NameError:
        resultFile = None
    else:
        resultFile.write("Encrypted Message: " + encryptedText + "\n")
        resultFile.close()

elif operationType == "2":
    if decryptFromFile.lower() == "n":
        textToDecrypt = input("Please enter the encrypted text that you would like to decrypt with your key:\n")

    decryptedText = decodeText(keys, textToDecrypt)

    print("Your decrypted text is: " + decryptedText)

    try:
        resultFile
    except NameError:
        resultFile = None
    else:
        resultFile.write("Decrypted Message: " + decryptedText + "\n")
        resultFile.close()
else:
    print("Please restart the cipher process, selecting a valid option.")

input()

# V-oRmzWVLMBCI19+
# Hi there my cat Phinei! Something else was 42 * 3 + 9 / (pi + 3) & 2 #cats4life
# La}xfcvi4qC4g9r\ssr1nrD*v2 ]7jk~D^7Ik7mTxPmqo}()f\+c9 `c?Cvc\}1)^1 ` #64ml|eb98
