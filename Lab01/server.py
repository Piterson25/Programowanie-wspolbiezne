import os

while True:
    if os.path.isfile("data.txt") and os.path.getsize("data.txt") > 0:
        print("File was received")
        file = open("data.txt", 'r')
        data = int(file.readline())
        file.close()
        os.remove("data.txt")

        result = data * data * data
        result_file = open("result.txt", 'w')
        result_file.write(str(result))
        result_file.close()
