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

"""


"""


import argparse

import wavio
import wsola

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
    wav = wavio.WavClass(args.iwavf)
    if args.nmsg:
        wav.print_wav_info()

    # duration modification with WSOLA
    f0trans = wsola.WSOLAClass(wav.fs)
    f0trans.set_f0rate(args.f0rate)
    f0trans.set_data(wav.d)
    f0trans.duration_modification()

    # wav.d = f0trans.wsolaed

    # F0 transfomation using re-sampling
    wav.d = f0trans.resampling()

    # write output .wav file
    wav.write_wave_data(args.owavf)

if __name__ == '__main__':
    main()
