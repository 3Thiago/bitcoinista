
import bitcoinista

demo_mode = False
if __name__ == '__main__':
    try:
        bitcoinista.main(demo_mode)
    except Exception as e:
        print 'An error occurred: {0}'.format(e)
