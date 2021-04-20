import random;
import string;

createNewKeyInput = input("Would you like to create a new unique encryption key? (Y/n): ");
userKey = "";

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

def convertKeyToOffsets(key):
    offsets = []
    # Follow rules laid out in CipherIdea.txt to convert all of the characters in the key to valid offsets for the text.
    return offsets

if createNewKeyInput.lower() == "y":
    userKey = createUserKey(16);
    print("Your new key is: " + userKey);

if userKey == "":
    userKey = input("Please input your user key to begin the encryption or decryption process:\n");

operationType = input("Would you like to encrypt (1) or decrypt (2) some text?\n")

print("------- Initiating Process -------")
if operationType == "1":
    textToEncrypt = input("Please enter the text that you would like to encrypt in accordance with your key:\n")
elif operationType == "2":
    textToDecrypt = input("Please enter the encrypted text that you would like to decrypt with your key:\n")
else:
    print("Please restart the cipher process, selecting a valid option.")

