
import bitcoinista.main

if __name__ == '__main__':
    try:
        bitcoinista.main.main()
    except Exception as e:
        print 'An error occurred: {0}'.format(e)
