import sys
from commit import Commit


def show_usage():
    print('usage:')
    exit()


def main(argv):
    if argv[1] == 'commit':
        if argv[2:] == []:
            print ('Empty')
            show_usage()
        print('commit')
        c = Commit(argv[2:], None)
        c.printFiles()
    elif argv[1] == 'update':
        print('update')
    elif argv[1] == 'checkout':
        print('checkout')
    else:
        show_usage()


if __name__ == '__main__':
    main(sys.argv)
