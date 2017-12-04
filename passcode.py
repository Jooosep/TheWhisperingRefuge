
password =int(input("Give passcode: "))
tries = 1
passcode = 72054
while (password != passcode and tries < 5):
    
    print("Incorrect passcode")
    password =int(input("Give passcode: "))
    tries+=1
if password == passcode:
    print("Correct password.")
    print("The gate opens making a huge screech.")
else:
    print("You have maxed your try limit. The gate has been locked for an hour.")
