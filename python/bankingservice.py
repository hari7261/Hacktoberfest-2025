def login():
    print("Enter Credentials to Login")
    for i in range(6):
        if i>=5:
            return 0
            
        else:
            username=input("Enter your Username: ")
            password=input("Enter your Password: ")
            if username==dbuser:
                if password==dbpass:
                    print("Login Successful\n")
                    return 1
                    break
                else:
                    print("Incorrect Password\n")
            else:
                print("Username not Found\n")


def menu():
    choice = 0
    while(choice!=4):
        print("\nYour Banking Services are: ")
        print("\n1. Credit \n2. Debit \n3. Check Balance \n4. Log Out")
        choice=input("Enter your Choice: ")
        if choice=="1":
            credit()
        elif choice=="2":
            debit()
        elif choice=="3":
            chkblc()
        elif choice=="4":
            logout()
        else:
            print("Invalid Input")

def credit():
    global curamt
    cramt=float(input("Enter the Amount to be Credited: "))
    curamt=curamt+cramt
    print("Balance after Transaction: ",curamt)
    return curamt
    

def debit():
    global curamt
    acnum=input("Enter Account Number to transfer Amount: ")
    acname1=input("Enter Receiver's Name: ")
    acname = acname1.upper()
    dbamt=float(input("Enter Amount to be Debited: "))
    tpin=input("Enter Your Transaction PIN: ")
    if tpin==dbtpin:
             print("Amount {} Transferred to {} Successfully to bank account number {} ".format(dbamt,acname, acnum))
             curamt=curamt-dbamt
             print("Remaining Balance",curamt)
             return curamt
    else:
        print("Invalid Inputs!!")

def chkblc():
    global curamt
    tpin=input("Enter Your Transaction PIN: ")
    if tpin==dbtpin:
             print("Fetching Balance.....")
             print(curamt)
    else:
        print("Invalid PIN!!")

def logout():
    a=input("Are you sure to Logout?? (Y/N): ")
    if a=="Y" or "y":
        print("Exitting......")
        exit()
    else:
        pass

dbuser = "admin"
dbpass="admin@123"
dbtpin="000000"
curamt = 5000
m=login()
if m==1:
    print("Hello!! ",dbuser)
    menu()
else:
    print("Account Blocked!!! Please try again after 24 hrs")
