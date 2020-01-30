def test(b):
    b[0][0] = 222



def main():
    a = tuple([1, 2, 3])
    a[2] = 22
    print(a)


if __name__ == "__main__":
    main()
