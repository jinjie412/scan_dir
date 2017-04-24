'''
@author: xiaoye
'''
#coding: utf-8
import Queue
import sys
import threading
from optparse import OptionParser

import requests

from config import get_header

'''reload(sys)
sys.setdefaultencoding('utf8')'''

class Doscan(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self._que = que

    def getStatus(self, url):
        try:
            r = requests.get(url, headers=get_header(), timeout=5)
            return int(r.status_code)
        except:
            print 'error open url'
        return -1

    def saveToFile(self, url):
        with open(option.outfile, 'a') as f:
            f.write(url + '\n')
    def run(self):
        while not self._que.empty():
            d = self._que.get()
            try:
                x1 = str(d).rfind('.')
                x2 = str(d).rfind('/')
                nowurl = url + d
                if x2 > x1:
                    try:
                        http = self.getStatus(nowurl)
                        sys.stdout.write(d + ' is scan  status:' + str(http) + '\n')
                        if http == 200:
                            if self.getStatus(nowurl[:-1] <> 200):
                                self.saveToFile(nowurl)
                        elif http == 403:
                            self.saveToFile(nowurl)
                    except:
                        print ('x2>x1: %s' % http)
                else:
                    try:
                        http = self.getStatus(nowurl)
                        sys.stdout.write(d + ' is scan  status:' + str(http) + '\n')
                        if 200 == http:
                            temp = nowurl[:x2] + '%20' + nowurl[x2:]
                            sys.stdout.write(temp)
                            filecode = self.getStatus(temp)
                            if filecode <> 200:
                                self.saveToFile(nowurl)
                        elif http == 403:
                            self.saveToFile(nowurl)
                    except:
                        print ('x2 < x1: %s' % http)


            except:
                pass
    
def main():
    thread = []
    thread_count = option.threadcount
    que = Queue.Queue()

    sp = str(option.dictname).split(',')
    print sp
    for _ in sp:
        with open(_, 'r') as f:
            for d in f.readlines():
                d = d.strip('\n')
                que.put(d)

    for i in range(thread_count):
        thread.append(Doscan(que))
    
    for i in thread:
        i.start()
    
    for i in thread:
        i.join()
        
if __name__ == '__main__':
    parse = OptionParser()
    parse.add_option('-u', '--url', dest='input_url', type='string', help='the url you wan to scan dir')
    parse.add_option('-o', '--out', dest='outfile', type='string', help='output filename', default='result.txt')
    parse.add_option('-s', '--speed', dest='threadcount', type='int', default=60, help='the thread_count')
    parse.add_option('-d', '--dict', dest='dictname', type='string', help='dict filename')
    (option, args) = parse.parse_args()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    url = option.input_url
    print (option, args)
    main()


