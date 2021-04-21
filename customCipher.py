import random;
import string;
import math;

createNewKeyInput = input("Would you like to create a new unique encryption key? (Y/n): ");
userKey = "";
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
# Note: for below with the \\ when it is printed, it comes out as two \ but it is actually stored as just one so it should not matter
inverseCharacters = ['~', '}', '|', '{', '`', '_', '^', ']', "\\", '[', '@', '?', '>', '=', '<', ';', ':', '/', '.', '-', ' ', ',', '+', '*', ')', '(', "'", '&', '%', '$', "#", '"', '!']

# Fix error and then go through all / 95 sections and change to the length of the string which should = 95
allCharactersString = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + " "
for num in numbers:
    allCharactersString += num

allCharactersStringLength = len(allCharactersString)
# print(len(allCharactersString)) = 85 without numbers or 95 With

# These are the same so we can just use ascii_letters for both combined
# print(string.ascii_letters + "\n")
# print(string.ascii_lowercase + string.ascii_uppercase + "\n")
# This is just punctuation such as !@#$%^&*()-=
# print(string.punctuation);

def createUserKey(length):
    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    # It takes a random character from a list created with the ascii characters and the digits for the length of n
    key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
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
    editedOffsets = []

    for offset in offsetList:
        modifiedOffset = offset * -1
        editedOffsets.append(modifiedOffset)

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
        elif character in string.punctuation:
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
        elif character in string.punctuation:
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
        originalPosition = currentPositionInChars + reversedKeyOffsets[int(characterCount / keyLength)][offsetCount]
        originalLetterPos = (originalPosition / allCharactersStringLength) - int((originalPosition / allCharactersStringLength))
        originalLetterPos = round(originalLetterPos * allCharactersStringLength)
        letter = allCharactersString[originalLetterPos]

        decodedMessage += letter

        # If we are on the last offset, then we go back to the next offset as we also go to the next key
        if offsetCount == (keyLength - 1):
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

operationType = input("Would you like to encrypt (1) or decrypt (2) some text?\n")

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



print("------- Initiating Process -------")
if operationType == "1":
    textToEncrypt = input("Please enter the text that you would like to encrypt in accordance with your key:\n")
elif operationType == "2":
    textToDecrypt = input("Please enter the encrypted text that you would like to decrypt with your key:\n")
else:
    print("Please restart the cipher process, selecting a valid option.")
