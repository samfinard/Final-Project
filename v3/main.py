import sys
import datetime

def main():
    start, end = datetime.datetime.strptime(sys.argv[1], "%m/%d/%Y"), datetime.datetime.strptime(sys.argv[2], "%m/%d/%Y")
    print(start, end)

if __name__ == "__main__":
    main()