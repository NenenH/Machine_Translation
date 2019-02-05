import re

def database():
    with open('Eng_Fil_2.csv') as fp:
        line = fp.readline()
        fp1 = open('Plural.txt', 'w')


        while line:
            temp = re.findall(r"[\w']+|[-+|/]", line)

            x = 0

            if temp[1] == 'mga':
                print(temp[0], ': ', temp[1])
                fp1.write(temp[0] + ',' + temp[2] +',NNS')
                fp1.write('\n')


            # while x < len(temp):
            #     fp1.write(temp[x] + ' ')
            #     print("FP1: ", temp[x])
            #     x += 1


            line = fp.readline()

        fp1.close()

print("Start")
database()
print("Done")