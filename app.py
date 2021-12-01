import argparse

def test():
    pass

def main():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test')
    args = parser.parse_args()

    if args.test:
        test()
    else:
        main()