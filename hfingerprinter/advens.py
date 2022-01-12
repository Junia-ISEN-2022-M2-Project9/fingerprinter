import logging
import os
import tempfile
import traceback

from hfinger import tshark_wrappers, hreader
from hfinger.analysis import hfinger_analyze


def get_logger(logger_name, create_file=False):
    """
    Instantiate given name logger at INFO level, output a log file and handle console show
    Args:
        logger_name:
        create_file:

    Returns:

    """
    # create logger for prd_ci
    log = logging.getLogger(logger_name)
    log.setLevel(level=logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if create_file:
        # create file handler for logger.
        fh = logging.FileHandler('files/output.log')
        fh.setLevel(level=logging.INFO)
        fh.setFormatter(formatter)
    # create console handler for logger.
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.INFO)
    ch.setFormatter(formatter)

    # add handlers to logger.
    if create_file:
        log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = get_logger('hfinger', create_file=True)
logger.info("Logger initiated")

path = "files/bigFileHttp.pcap"

"""
This block aims to take a pcap entry and output found fingerprints in a file.
It should :
- Handle multithread
- Catch errors and pursue process
"""
# Start fingerprinting (legititimacy > tshark version & path > tshark > tmp json > parse
results = hfinger_analyze(path, reportmode=4)
file = open("output.txt","w+")
try:
    for result in results:
        logger.info("Entry tshark formatted : {}".format(result.get("fingerprint")))
        file.write(result.get("fingerprint") + "\n")
except IOError:
    logger.exception("Error opening file to write output in")
finally:
    file.close()
logger.info("Program successfully exited")

"""
# Could be interesting, fix a json if tshark version below 2.2.6
# tmp = tshark_wrappers.repair_json("3.6.1", jsonn)
try:
    tshark_json = "file/tshark.json"
    tmp = hreader.reader_wrapper(tshark_json, 4)
    print(tmp)
except:
    logger.exception("Well it doesnt work")
"""
