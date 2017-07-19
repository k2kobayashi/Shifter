#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
#   First edition: 2017-04-25
#
#   Copyright 2017
#       Kazuhiro KOBAYASHI <kobayashi.kazuhiro@g.sp.m.is.nagoya-u.ac.jp>
#
#   Distributed under terms of the MIT license.
#

import argparse
import numpy as np
from scipy.io import wavfile

from shifter import Shifter

def main():
    # Options for python
    dcp = "shifter: F0 transformation of .wav file"
    parser = argparse.ArgumentParser(description=dcp)
    parser.add_argument('-nmsg', '--nmsg', default=True, action='store_false',
                        help='Print no message')
    parser.add_argument('-f0rate', '--f0rate', type=float, default=1.0,
                        help='F0 transformation ratio [1.0]')
    parser.add_argument('iwavf', type=str,
                        help='Input .wav file')
    parser.add_argument('owavf', type=str,
                        help='Output .wav file')
    args = parser.parse_args()

    if args.nmsg:
        print "### Arguments ###"
        print "F0 transformation rate: ", args.f0rate
        print "Input .wav file : ", args.iwavf
        print "Output .wav file : ", args.owavf

    # read input .wav file
    fs, x = wavfile.read(args.iwavf)

    # F0 transoformation based on WSOLA and resampling
    f0trans = Shifter(fs, args.f0rate, frame_ms=20, shift_ms=10)
    transformed = f0trans.transform(x)

    # write output .wav file
    wavfile.write(args.owavf, fs, np.array(transformed, dtype=np.int16))

if __name__ == '__main__':
    main()
