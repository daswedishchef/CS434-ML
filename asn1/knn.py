import csv, numpy
k = 7
hp = [1, 3, 5, 7, 9, 99, 999, 8000]
flag = 0

def load_arr(file):
    data = numpy.genfromtxt(file, dtype = float, delimiter = ',', skip_header=1)
    return data

def distance(x, xi):
    temp = xi[1:-1]
    if flag == 1:
        tempx = x[1:-1]
    else:
        tempx = x[1:]
    return numpy.linalg.norm(temp - tempx)  

def classify(test, train):
    avg = 0.00000000000
    dist = list()
    for case in train:
        dist.append(distance(test, case))
    #sort array by index
    dex = numpy.argsort(dist)
    #select k nearest neighbors
    global k
    if flag == 1 and k == 8000:
        k = 6000
    for i in range(0,k):
        avg += train[dex[i], -1]
    avg /= k
    ident = round(avg)
    return ident

def kmain(train):
    print("Doing 4-fold cross validation")
    global flag
    flag = 1
    #test case loop
    output = open("kcross.txt", "w")
    output.write("id,income\n")
    perf = list()
    for hype in hp:
        global k
        k = hype
        output.write("K = ")
        output.write(str(k))
        output.write("\n")
        print("k = ", k)
        vmean = 0.0000000000
        var = list()
        for i in range(0,4):
            print("subset ", (i+1))
            output.write("Subset #")
            output.write(str(i+1))
            nacc = 0
            start = i * 2000
            end = (i+1) * 2000
            cases = train[start:end]
            if start == 0:
                tcases = train[end:]
            elif end == 8000:
                tcases = train[:start]
            else:
                t1 = train[:start]
                t2 = train[end:]
                tcases = numpy.vstack((t1,t2))
            res = list()      
            for test in cases:
                res.append(classify(test, tcases))
            index = 0
            for r in res:
                if cases[index, -1] == r:
                    nacc += 1
            acc = nacc/2000.0
            vmean += acc
            var.append(acc)
            output.write(" Validation Accuracy: ")
            output.write(str(acc))
            vd = list()
            for test in cases:
                vd.append(classify(test, train))
            nacc = 0
            for r in vd:
                if cases[index, 86] == r:
                    nacc += 1
            acc = nacc/2000.0
            output.write(" Training Accuracy: ")
            output.write(str(acc))
            output.write("\n")
        vmean /= 4
        v = numpy.var(var)
        output.write("Mean = ")
        output.write(str(vmean))
        output.write("  Varience")
        output.write(str(var))
        output.write("\n")
        perf.append(vmean)
        print("mean", vmean)
        print("var", var)
    output.close()
    dex = numpy.argsort(perf)
    return hp[dex[-1]]

def main():
    train = load_arr("train.csv")
    test_pub = load_arr("test_pub.csv") 
    global k
    k = kmain(train)
    #test case loop
    print("generating output based on best performance")
    index = 0
    res = open("result.txt", "w")
    res.write("id,income\n")
    for test in test_pub:
        print("Test Number: ", index)
        res.write(str(index))
        res.write(",")
        res.write(str(classify(test,train)))
        res.write("\n")
        index += 1
    res.close()

main()