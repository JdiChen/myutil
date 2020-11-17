def demo():
    a = [1,2]
    for i in a:
        print("befor yilid")
        yield 4
        print("end yield")

if __name__ == '__main__':
    b = demo()
    for i in b:
        print(i)
    print(b.send(3))
    print(b)
    # print(b.__next__())
    # print(b.__next__())
    # print(b.__next__())