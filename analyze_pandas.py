#!/usr/bin/env python

import argparse
import sys
import json
from math import log2
from datetime import timedelta, datetime as dt
import munch
import glob
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import collections
import time
import pprint
from IPython import embed

HINTS = """
print('\n'.join(gdf.columns))

gdf.ix[:,['power_batteryTemperature', 'general_devTemperature', 'power_battChargeLevel']].plot()
plt.show()

gdf.power_batteryVoltage.plot()
plt.show()

f, axarr = plt.subplots(2, sharex=True)
ax = gdf.power_batteryVoltage.plot(ax=axarr[0])
gdf.wwan_dataUsage_generic_dataTransferred.diff().plot(ax=axarr[1])
plt.show()

# Show the negative) correlation between current datarate and battery voltage:
df = gdf.ix[:,['power_batteryVoltage', 'wwan_dataUsage_generic_dataTransferred']]
df['diffdata'] = gdf.wwan_dataUsage_generic_dataTransferred.diff()
df.corr()['diffdata']['power_batteryVoltage']
# gives -0.4

gdf.ix[:,['wwan_signalStrength_rsrp','wwanadv_radioQuality']].plot()
plt.show()

gdf.wwan_signalStrength_bars.plot()
plt.show()

gdf.ix[:,['wwanadv_rxLevel','wwanadv_txLevel']].plot()
plt.show()

numeric_columns = ('wwan_dataTransferredRx', 'wwan_dataTransferredTx')
for numeric_column in numeric_columns:
    gdf[numeric_column] = gdf[numeric_column].convert_objects(convert_numeric=True)

# MiBs transferred
(gdf.ix[:,['wwan_dataTransferredRx', 'wwan_dataTransferredTx']] / 1024**2).plot()
plt.show()

# Calculate Timedeltas
gdf['ts'] = gdf.index
gdf['ts_delta'] = (gdf['ts']-gdf['ts'].shift())
#gdf['ts_delta'] = gdf['ts_delta'].fillna(0)
gdf['ts_delta'] /= np.timedelta64(1,'s')

# MBit/s
df = gdf.ix[:,['wwan_dataTransferredRx', 'wwan_dataTransferredTx']]
df = (df / 1024.0**2).diff() * 8
df['wwan_dataTransferredRx'] = df['wwan_dataTransferredRx'] / gdf['ts_delta']
df['wwan_dataTransferredTx'] = df['wwan_dataTransferredTx'] / gdf['ts_delta']
df['wwan_dataTransferredRx'][df['wwan_dataTransferredRx'] < 0] = float('nan')
df['wwan_dataTransferredTx'][df['wwan_dataTransferredTx'] < 0] = float('nan')
df.plot()
plt.show()

"""

def flatten(d, parent_key='', sep='_'):
    # http://stackoverflow.com/a/6027615/183995
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def main():
    parser = argparse.ArgumentParser(description='Analyzing the Netgear AirCard JSON status.')
    parser.add_argument('log-folder', help='The folder where the JSON logs are stored')
    args = parser.parse_args()

    gdf = pd.DataFrame()
    for fname in glob.glob(sys.argv[1] + '/*.json'):
        try:
            f = open(fname, 'r')
            context = json.loads(f.read())
        except Exception as e:
            print("could not read the file {}:\n{}".format(fname, str(e)))
        f.close()
        #context = munch.Munch.fromDict(context)
        fcontext = flatten(context)
        del fcontext['general_supportedLangList']
        del fcontext['router_clientList']
        del fcontext['wwan_profileList']
        del fcontext['wwan_bandRegion']
        del fcontext['sms_msgs']
        #pprint.pprint(fcontext)
        #embed()
        try:
            df = pd.DataFrame.from_dict(fcontext)
            gdf = gdf.append(df)
        except Exception as e:
            print(e)
    gdf = gdf.set_index(gdf.general_currTime.apply(dt.fromtimestamp))
    for col in gdf.columns:
        try:
            descr = gdf[col].describe()
        except:
            print('Could not describe ' + col)
        interesting = False
        if 'std' in descr and descr['std'] > 0.0:
            interesting = True
        if 'unique' in descr and descr['unique'] > 1:
            interesting = True
        if interesting:
            print(descr)
            print('-------------')
    print(HINTS)
    embed()

if __name__ == "__main__":
    main()

