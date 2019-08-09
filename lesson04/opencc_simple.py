import logging
import sys
from opencc import OpenCC
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)
'''
    conver data from traditional to simplize by opencc.
'''
def help():
    print("Usage: python opencc_simple.py zhwiki.txt zhwiki_simple.txt")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        help()
        sys.exit(1)
    logging.info("running %s" % ' '.join(sys.argv))
    inp, outp = sys.argv[1:3]
    i = 0

    output = open(outp, 'w', encoding='utf8')
    input = open(inp, 'r', encoding='utf8')
    cc = OpenCC('t2s')
    for line in input:
        converted = cc.convert(line)
        output.write(converted + "\n")
        i = i + 1
        if (i % 10000 == 0):
            logging.info("Save "+str(i) + " articles")
    output.close()
    logging.info("Finished saved "+str(i) + "articles")
