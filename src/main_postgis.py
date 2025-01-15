import time
import os

from consumer import OsmComsumer

print('BOARA LAAAAAAAAAA')
execute = OsmComsumer()

while True:
    if os.path.isfile(os.path.join('OSMs', 'ok.txt')):
        execute.run_file()
        break
    else:
        print('aguardando o arquivo')