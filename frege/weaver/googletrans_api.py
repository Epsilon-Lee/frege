"""
Author: Guanlin Li
Date  : Jan. 9 2019
"""

from googletrans import Translator
import argparse
import time

class GoogleTransAPI():
    def __init__(self):
        self.translator = Translator()

    def translate(self, s, src='en', dest='zh-CN'):
        t = self.translator.translate(s, src=src, dest=dest)
        return t.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Script for translate an input text file to an output text file.')
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--src', type=str, default='en')
    parser.add_argument('--dest', type=str, default='zh-CN')
    args = parser.parse_args()

    saveto = args.input_file + '.trans.{}'.format(args.dest)
    api = GoogleTransAPI()
    with open(args.input_file, 'r') as f:
        with open(saveto, 'w') as f_saveto:
            cnt = 0
            start = time.time()
            for line in f:
                cnt += 1
                line = line.strip()
                new_line = api.translate(line, args.src, args.dest) + '\n'
                f_saveto.write(new_line)
                if cnt % 20 == 0:
                    print('%.2f (s) per 20 sentences' % (time.time()- start))
                    start = time.time()
