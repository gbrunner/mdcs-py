import os
import logging
import shutil
import time
import datetime

today = datetime.datetime.now()
d = today.strftime("%Y%m%d_%H%M%S")

log_location = "C:\\PROJECTS\\NASA\\0MD"
prod_gdb = "C:\\PROJECTS\\NASA\\0MD\\Production.gdb"
master_gdb = "C:\\PROJECTS\\NASA\\0MD\\Master.gdb"

start_time = time.time()
try:
    logging.basicConfig(filename=os.path.join(log_location,'processing_' + d + '.log'),
                    filemode='w',
                    level='INFO',
                    format='%(name)s - %(levelname)s - %(message)s')
    if os.path.exists(prod_gdb):
        print("rmtree")
        shutil.rmtree(prod_gdb)
        print('removed old ' + prod_gdb)
        logging.info('removed old ' + prod_gdb)
    production = shutil.copytree(master_gdb, prod_gdb)
    print('copied ' + master_gdb + ' to ' + prod_gdb)
    logging.info('copied ' + master_gdb + ' to ' + prod_gdb)
    print('success on ' + d)
    logging.info('success on ' + d)
    print("process took %s seconds" % (time.time() - start_time))
    logging.info("process took %s seconds" % (time.time() - start_time))


except:
    logging.basicConfig(filename=os.path.join(log_location,'failure_' + d + '.log'),
                        filemode='w',
                        level='INFO',
                        format='%(name)s - %(levelname)s - %(message)s')
    print('failure on ' + d)
    logging.warning('failure on ' + d)
    print("process took %s seconds" % (time.time() - start_time))
    logging.info("process took %s seconds" % (time.time() - start_time))
