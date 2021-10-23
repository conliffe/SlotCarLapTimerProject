# if Statement
#ifCondition = input("Enter 'yes' to execute loop: ")
#if ifCondition == "yes":
#    print("You seleceted yes to go into if statement")
#else:
#    print("You did not select to go into if statement")

loopValue = int(input("How many iterations do you want in your loop? "))
# For loop
#print("This is a for loop")
#for i in range(loopValue):
#    print("Iteration number: ", i)
#print("Loop for", i+1 ,"iterations are done.")

# While loop
i = 1
while i <= loopValue :
    print("Iteration number: ", i)
    i = i + 1
    pass
print("Loop for", i-1 ,"iterations are done.")
