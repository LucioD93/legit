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
        c.sendFile(argv[2], argv[3])
    elif argv[1] == 'update':
        if len(argv[2:]) != 3:
            show_usage()
        c = Commit(argv[2:], None)
        c.updateOperation(argv[2], "Update", argv[3], argv[4])
    elif argv[1] == 'checkout':
        if len(argv[2:]) != 3:
            show_usage()
        c = Commit(argv[2:], None)
        c.updateOperation(argv[2], "Checkout", argv[3], argv[4])
    else:
        show_usage()

if __name__ == '__main__':
    main(sys.argv)
