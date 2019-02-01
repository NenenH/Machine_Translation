import re

def database():
    with open('db.csv') as fp:
        line = fp.readline()
        fp1 = open('Fil_Eng_1.txt', 'w')
        fp2 = open('Fil_Eng_2.txt', 'w')
        x = 0

        while line:
            temp = re.findall(r"[\w']+|[-+|/]", line)
            print(temp)
            x = 0
            if len(temp) > 2:
                print(len(temp))
                while x < len(temp):
                    fp1.write(temp[x] + ' ')
                    print("FP1: ", temp[x])
                    x += 1
                fp1.write('\n')
            else:
                print(len(temp))
                fp2.write(temp[0] + ' ' + temp[1] + '\n')
                print("FP2: ", temp[1])
            line = fp.readline()

        fp1.close()
        fp2.close()

print("Start")
database()
print("Done")