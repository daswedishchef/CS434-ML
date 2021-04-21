import csv, numpy

def load_arr(file):
    data = numpy.genfromtxt(file, dtype = float, delimiter = ',', skip_header=1)
    print(numpy.shape(data))
    return data

def classify(test, train):
    dist = list()
    for case in train:
        dist.append(distance(test, case))
    near = numpy.argsort(dist)[:k]


def main():
    train = load_arr("train.csv")
    test_pub = load_arr("test_pub.csv")

    #test case loop
    index = 0
    output = open("output.txt", "w")
    for test in test_pub:
        output.write(index)
        output.write(",")
        output.write(str(classify(test,train)))
        output.write("\n")
    output.close()

main()