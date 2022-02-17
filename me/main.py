from Me import Me
import time
from logger import MeLogger

if __name__ == '__main__':
    aa = Me()
    log = MeLogger(name=__name__)

    while True:
        time.sleep(0.2)
        log.flush()
        command = input('?> ')
        aa.execute(command)
