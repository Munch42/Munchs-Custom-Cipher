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

if createNewKeyInput.lower() == "y":
    userKey = createUserKey(16);
    print("Your new key is: " + userKey);

if userKey == "":
    userKey = input("Please input your user key to begin the encryption or decryption process:\n");

print("------- Initiating Process -------")
print(userKey)
