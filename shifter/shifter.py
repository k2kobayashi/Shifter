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

import numpy as np
from scipy.interpolate import interp1d


class Shifter:

    """Shifter class
    This class offers to transform f0 of input waveform sequence
    based on WSOLA and resampling

    Attributes
    ---------
    wsolaed : shape (`len(data) * f0rate`)
        Array of wsolaed waveform sequence

    : shape (`len(data) * f0rate`)
        Array of wsolaed waveform sequence

    """

    def __init__(self, fs, f0rate, frame_ms=20, shift_ms=10,):
        self.fs = fs
        self.f0rate = f0rate

        self.frame_ms = frame_ms  # frame length [ms]
        self.shift_ms = shift_ms  # shift length [ms]
        self.sl = int(self.fs * self.shift_ms / 1000)  # of samples in a shift
        self.fl = int(self.fs * self.frame_ms / 1000)  # of samples in a frame
        self.epstep = int(self.sl / self.f0rate)  # step size for WSOLA
        self.win = np.hanning(self.fl)  # window function for a frame
        self.searchl = self.fl  # search length

    def transform(self, data):
        """Transform F0 of given waveform signals using

        Parameters
        ---------
        data : array, shape ('len(data)')
            array of waveform sequence

        Returns
        ---------
        transformed : array, shape (`len(data)`)
            Array of F0 transformed waveform sequence

        """

        wsolaed = self.duration_modification(data)
        transformed = self.resampling(wsolaed)

        return transformed

    def duration_modification(self, data):
        """Duration modification based on WSOLA

        Parameters
        ---------
        data : array, shape ('len(data)')
            array of waveform sequence

        Returns
        ---------
        wsolaed: array, shape (`int(len(data) * f0rate)`)
            Array of WSOLAed waveform sequence

        """

        wlen = len(data)
        wsolaed = np.zeros(int(wlen * self.f0rate), dtype='d')

        # initialization
        sp = self.sl
        rp = sp + self.sl
        ep = sp + self.epstep
        outp = 0

        while wlen > ep + self.fl:
            if ep - self.fl < self.sl:
                sp += self.epstep
                rp = sp + self.sl
                ep += self.epstep
                continue

            # cspy wavform
            ref = data[rp - self.sl:rp + self.sl] * self.win
            buff = data[ep - self.fl:ep + self.fl]

            # search minimum distance bepween ref and buff
            delta = self._search_minimum_distance(ref, buff)
            epd = ep + delta

            # store WSOLAed waveform using over-lap add
            spdata = data[sp:sp + self.sl] * self.win[self.sl:]
            epdata = data[epd - self.sl: epd] * self.win[:self.sl]
            wsolaed[outp:outp + self.sl] = spdata + epdata
            outp += self.sl

            # transtion to next frame
            sp = epd
            rp = sp + self.sl
            ep += self.epstep

        return wsolaed

    def resampling(self, data):
        """Resampling

        Parameters
        ---------
        data : array, shape ('int(len(data) * f0rate)')
            array of wsolaed waveform

        Returns
        ---------
        wsolaed: array, shape (`len(data)`)
            Array of resampled (F0 transformed) waveform sequence

        """

        # interpolate
        wedlen = len(data)
        intpfunc = interp1d([i for i in range(wedlen)], data, kind=1)
        x_new = np.arange(0.0, wedlen - 1, self.f0rate)
        resampled = intpfunc(x_new)

        return resampled

    def _search_minimum_distance(self, ref, buff):
        cc, maxcc = -1, -1
        for t in range(self.fl):
            tar = buff[t:t + self.fl] * self.win
            cc = self._cross_correration(ref, tar)
            if cc > maxcc:
                maxcc = cc
                delta = t
        return delta - self.sl

    def _cross_correration(self, org, tar):
        return np.correlate(org, tar)
