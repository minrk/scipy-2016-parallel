import os
import shutil
from glob import glob
import pandas as pd
import json
from fakestockdata import generate_stocks


if not os.path.exists('data'):
    os.mkdir('data')


minute = os.path.join('data', 'minute')
if not os.path.exists(minute):
    os.mkdir(minute)
    generate_stocks(freq=pd.Timedelta(minutes=10),
                    directory=minute)


js = os.path.join('data', 'json')
if not os.path.exists(js):
    os.mkdir(js)
    directories = sorted(glob(os.path.join(minute, '*')))
    for d in directories:
        filenames = sorted(glob(os.path.join(d, '*')))[-365:]
        with open(d.replace('minute', 'json') + '.json', 'w') as f:
            for fn in filenames:
                df = pd.read_csv(fn)
                for rec in df.to_dict(orient='records'):
                    json.dump(rec, f)
                    f.write(os.linesep)
