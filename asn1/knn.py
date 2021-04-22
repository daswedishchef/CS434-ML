import csv, numpy, sys
k = 8
#k values for k-fold to try
hp = [1, 3, 5, 7, 9, 99, 999, 8000]
#kfold flag
flag = 0

#data loading funciton - loads csv data into matrix
def load_arr(file):
    data = numpy.genfromtxt(file, dtype = float, delimiter = ',', skip_header=1)
    return data

#distance function - calculates euclidean distance between two 1D data point arrays
def distance(x, xi):
    temp = xi[1:-1]
    if flag == 1:
        tempx = x[1:-1]
    else:
        tempx = x[1:]
    return numpy.linalg.norm(temp - tempx)  

#classifier function - takes 1D array test and training data matrix
#returns class of test case based on given data
def classify(test, train):
    avg = 0.00000000000
    dist = list()
    #test against every case
    for case in train:
        dist.append(distance(test, case))
    dex = numpy.argsort(dist)
    #select k nearest neighbors
    global k
    if flag == 1 and k == 8000:
        k = 6000
    for i in range(0,k):
        avg += train[dex[i], -1]
    avg = numpy.divide(avg,k)
    ident = round(avg)
    return ident

#main k-fold function - takes training data and returns highest performing k value
def kmain(train):
    print("Doing 4-fold cross validation")
    global flag
    flag = 1
    #test case loop
    output = open("kcross.txt", "w")
    perf = list()
    #loop over possible k values
    for hype in hp:
        global k
        k = hype
        output.write("K = ")
        output.write(str(k))
        output.write("\n")
        print("k = ", k)
        vmean = 0.0000000000
        var = list()
        #loop over subset valdation blocks
        for i in range(0,4):
            print("subset ", (i+1))
            output.write("Subset #")
            output.write(str(i+1))
            nacc = 0.00
            start = i * 2000
            end = (i+1) * 2000
            cases = train[start:end]
            if i == 0:
                tcases = train[end:]
            elif i == 3:
                tcases = train[:start]
            else:
                t1 = train[:start]
                t2 = train[end:]
                tcases = numpy.vstack((t1,t2))
            res = list() 
            #test validation data against the rest of data and store result     
            for test in cases:
                res.append(classify(test, tcases))
            index = 0
            #calculate validation performance
            for case in cases:
                if case[-1] == res[index]:
                    nacc += 1
                index += 1
            acc = nacc/2000.0
            vmean += acc
            var.append(acc)
            output.write(" Validation Accuracy: ")
            print("Validation: ", acc)
            output.write(str(acc))
            vd = list()
            #test validation data against all of the data and store result
            for test in cases:
                vd.append(classify(test, train))
            nacc = 0.00
            #calculate training performance
            index = 0
            for case in cases:
                if case[-1] == vd[index]:
                    nacc += 1
                index += 1
            acc = nacc/2000.0
            print("training:", acc)
            output.write(" Training Accuracy: ")
            output.write(str(acc))
            output.write("\n")
        #calculate varience and mean
        vmean /= 4
        v = numpy.var(var)
        output.write("Mean = ")
        output.write(str(vmean))
        output.write("  Varience")
        output.write(str(v))
        output.write("\n")
        perf.append(vmean)
        print("mean", vmean)
        print("var", v)
    #determine highest performing k
    output.close()
    dex = numpy.argsort(perf)
    return hp[dex[-1]]

#main - uses highest performing k value to generate results for the testing data
def main():
    train = load_arr("train.csv")
    test_pub = load_arr("test_pub.csv") 
    if sys.argv[1] == "validate":
        global k
        k = kmain(train)
    print("generating output based on best performance")
    index = 0
    res = open("result.txt", "w")
    res.write("id,income\n")
    #test case loop
    for test in test_pub:
        print("Test Number: ", index)
        res.write(str(index))
        res.write(",")
        res.write(str(classify(test,train)))
        res.write("\n")
        index += 1
    res.close()

main()