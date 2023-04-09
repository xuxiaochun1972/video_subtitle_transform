import os
import sys
import argparse
import re
from datetime import datetime,date,timedelta

transform_mode = "None"
dt = 0.0
ts0 = datetime.strptime('00:00:00,000', '%H:%M:%S,%f')

def transform(ts):
    if(transform_mode == "NTSC_to_PAL"):
        ts1 = NTSC_to_PAL(ts)
    elif(transform_mode == "PAL_to_NTSC"):
        ts1 = PAL_to_NTSC(ts)
    else:
        ts1 = ts
    ts2 = delay(ts1)
    return ts2

def delay(ts):
    return ts + dt

def NTSC_to_PAL(ts):
    ts1 = ((ts - ts0) * 24.0) / 25.0 + ts0
    return ts1

def PAL_to_NTSC(ts):
    ts1 = ((ts - ts0) * 25.0) / 24.0 + ts0
    return ts1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--transform", type=str, choices = ['None', 'NTSC_to_PAL', 'PAL_to_NTSC'], default = 'None', help="video signal format transform")
    parser.add_argument("-d", "--delay", type=float, default = 0.0, help="delay in second")
    parser.add_argument("file_in", type=argparse.FileType("r", encoding='utf-8'), help="name of input file")
    parser.add_argument("file_out", type=argparse.FileType("w", encoding='utf-8'), help="name of output file")
    args = parser.parse_args()
    transform_mode = args.transform
    dt = timedelta(seconds = float(args.delay))

    for line_no, line in enumerate(args.file_in):
        m = re.match('(\d\d:\d\d:\d\d,\d\d\d)(\s-->\s)(\d\d:\d\d:\d\d,\d\d\d)',line)
        if m:
            ts1_str, f1, ts2_str = m.groups()
            ts1 = datetime.strptime(ts1_str, '%H:%M:%S,%f')
            ts2 = datetime.strptime(ts2_str, '%H:%M:%S,%f')
            ts1 = transform(ts1)
            ts2 = transform(ts2)
            ts1_str = ts1.strftime('%H:%M:%S,%f')[:-3]
            ts2_str = ts2.strftime('%H:%M:%S,%f')[:-3]
            args.file_out.write("".join([ts1_str, f1, ts2_str]))
            args.file_out.write("\n")
        else:
            args.file_out.write(line.strip())
            args.file_out.write("\n")
