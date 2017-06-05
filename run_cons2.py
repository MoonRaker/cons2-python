
import logging

logging.basicConfig(filename='cons2.log', 
                    level=logging.DEBUG,
                    # level=logging.INFO,
                    # level=logging.CRITICAL,
                    # level=logging.WARNING,
                    format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')
logger = logging.getLogger('run_cons2')

import cons2

logger.info('finished loading cons2')


def main():

    cons2.main.run()

if __name__=='__main__':
        try:
            main()
        except Exception as err:
            logger.exception('Error occurred in main():')
            raise