#! /usr/local/bin/python
# -*- coding: utf-8 -*-
#
# wsola.py
#   First edition: 2017-04-26
#
#   Copyright 2017
#       Kazuhiro KOBAYASHI <kazuhiro-k@is.naist.jp>
#
#   Distributed under terms of the MIT license.
#

"""


"""

import numpy as np
from scipy.interpolate import interp1d


class WSOLAClass:

    def __init__(self, fs):
        self.shift_ms = 10  # shift length [ms]
        self.frame_ms = 20  # frame length [ms]
        self.sl = int(fs * self.shift_ms / 1000)  # of samples in a shift
        self.fl = int(fs * self.frame_ms / 1000)  # of samples in a frame
        self.win = np.hanning(self.fl)  # window function for a frame
        self.searchl = self.fl  # search length

    def set_f0rate(self, f0rate):
        self.f0rate = f0rate  # f0 transformation ratio
        self.epstep = int(self.sl / self.f0rate)  # step size for WSOLA

    def set_data(self, data):
        self.data = data  # input waveform
        self.wlen = len(data)
        self.wsolaed = np.zeros(int(self.wlen * self.f0rate), dtype='d')

    def duration_modification(self):
        # initialization
        sp = self.sl
        rp = sp + self.sl
        ep = sp + self.epstep
        outp = 0

        while self.wlen > ep + self.fl:
            if ep - self.fl < self.sl:
                sp += self.epstep
                rp = sp + self.sl
                ep += self.epstep
                continue

            # cspy wavform
            ref = self.data[rp - self.sl:rp + self.sl] * self.win
            buff = self.data[ep - self.fl:ep + self.fl]

            # search minimum distance bepween ref and buff
            delta = self.search_minimum_distance(ref, buff)
            epd = ep + delta

            # store WSOLAed waveform using over-lap add
            spdata = self.data[sp:sp + self.sl] * self.win[self.sl:]
            epdata = self.data[epd - self.sl: epd] * self.win[:self.sl]
            self.wsolaed[outp:outp + self.sl] = spdata + epdata
            outp += self.sl

            # transtion to next frame
            sp = epd
            rp = sp + self.sl
            ep += self.epstep

    def search_minimum_distance(self, ref, buff):
        cc, maxcc = -1, -1
        for t in range(self.fl):
            tar = buff[t:t + self.fl] * self.win
            cc = self.cross_correration(ref, tar)
            if cc > maxcc:
                maxcc = cc
                delta = t
        return delta - self.sl

    def cross_correration(self, org, tar):
        return np.correlate(org, tar)

    def resampling(self):
        # interpolate
        wedlen = len(self.wsolaed)
        intpfunc = interp1d([i for i in range(wedlen)], self.wsolaed, kind=1)
        x_new = np.arange(0.0, wedlen - 1, self.f0rate)
        resampled = intpfunc(x_new)
        return resampled
