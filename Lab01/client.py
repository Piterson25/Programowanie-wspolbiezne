import os

data = input("Hello! Please insert your integer: ")
data_file = open("data.txt", 'w')
data_file.write(data)
data_file.close()

while True:
    if os.path.isfile("result.txt") and os.path.getsize("result.txt") > 0:
        result_file = open("result.txt", 'r')
        print("Here is your result:", result_file.readline())
        result_file.close()
        os.remove("result.txt")
        break
