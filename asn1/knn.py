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
    c = numpy.power(tempx-temp, 2)
    d = numpy.linalg.norm(c)
    #print(d)
    if d == 0.0:
        #print cases when distance is 0
        print(temp)
        print(tempx)
        print("match made")
        exit
    return d   

def classify(test, train):
    avg = 0.0
    dist = numpy.empty((1,8000))
    for case in train:
        #issue here - dist array not being updated it seems
        numpy.append(dist, distance(test, case))
    #sort array by index
    dex = numpy.argsort(dist)
    #print(dex)
    #print k neartest neighbors
    for i in range(0,k):
        print(dex[0, i])
        print(dist[0, dex[0, i]])




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