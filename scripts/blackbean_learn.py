"""BlackBean Learning Mode

Copyright (c) 2018 Daisuke IMAI

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""
import sys
import time
import broadlink

def main():
    print 'Start Discovering...(wait 15 sec.)...',
    sys.stdout.flush()
    devices = broadlink.discover(timeout=15)
    print 'done'
    if len(devices) > 0:
        print 'Found a BlackBean'
        device = devices[0]
        device.auth()
        print 'Entering Learning Mode...',
        sys.stdout.flush()
        device.enter_learning()
        print 'done'
        print 'Please push IR button once within 5 sec.(And wait 15 sec.)'
        time.sleep(15)
        learned_data = device.check_data()
        if learned_data is None:
            print 'Error: No learning data.'
        else:
            print "Success.(Data is below.)"
            print learned_data.encode('hex')
    else:
        print 'Error: Not found BlackBeans.'

if __name__ == '__main__':
    main()
