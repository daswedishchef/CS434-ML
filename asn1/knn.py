import csv, numpy

k = 5

def load_arr(file):
    data = numpy.genfromtxt(file, dtype = float, delimiter = ',', skip_header=1)
    print(numpy.shape(data))
    return data

#equal to using linalg.norm but much slower
# def distance(x, xi):
#     d = 0.00000000000
#     temp = xi[1:-1]
#     tempx = x[1:]
#     c = tempx - temp
#     numpy.power(c, 2)
#     index = 0
#     for i in numpy.nditer(c):
#         d += i
#     return numpy.sqrt(d)


def distance(x, xi):
    temp = xi[1:-1]
    tempx = x[1:]
    d = numpy.linalg.norm(temp - tempx)
    return d   

def classify(test, train):
    avg = 0.00000000000
    dist = list()
    index = 0
    for case in train:
        #issue here - dist array not being updated it seems
        val = distance(test, case)
        #print(val)
        dist.append(val)
        index += 1
    #sort array by index
    dex = numpy.argsort(dist)
    #print k neartest neighbors
    near = list()
    for i in range(0,k):
        avg += train[dex[i], 86]
    avg /= k
    ident = round(avg)
    return ident




def main():
    train = load_arr("train.csv")
    test_pub = load_arr("test_pub.csv")
    #test case loop
    index = 0
    output = open("output.txt", "w")
    for test in test_pub:
        print("Test Number: ", index)
        output.write(str(index))
        output.write(",")
        output.write(str(classify(test,train)))
        output.write("\n")
        index += 1
    output.close()

main()