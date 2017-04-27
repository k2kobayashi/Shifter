#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#   wave
# Copyright 2015
#    Kazuhiro KOBAYASHI <kazuhiro-k@is.naist.jp>
#
# Distributed under terms of the MIT license.

"""
wav class handles wave format and FILE IO

"""

import pyaudio
import wave as wv
import scipy as sp


class WavClass:

    def __init__(self, nmsg, iwavf):
        # open .wav file and get properties
        self.wf = wv.open(iwavf, 'rb')
        self.c = self.wf.getnchannels()
        self.fs = self.wf.getframerate()
        self.bit = self.wf.getsampwidth()
        self.nlen = self.wf.getnframes()
        self.x = sp.fromstring(self.wf.readframes(self.n), dtype=sp.int16)
        self.d = self.x / 32767.0
        self.t = self.n / float(self.fs)

        if nmsg:
            print "File name:", iwavf
            self.print_wav_info()

    def __del__(self):
        self.wf.close()

    # print wave information
    def print_wav_info(self):
        print "Properties of .wav file"
        print "# Channels:", self.c
        print "# Sampling rate:", self.fs
        print "# Quontized bit rate:", self.bit
        print "# Sample flames:", self.nlen
        print "# Time:", self.t

    # play wave file
    def play_wav_data(self):
        self.wf.rewind()
        chunk = 1024
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.c,
                        rate=self.fs,
                        output=True)
        data = self.wf.readframes(chunk)
        while data != '':
            stream.write(data)
            data = self.wf.readframes(chunk)
        stream.close()
        p.terminate()

    # save wave file
    def write_wave_data(self, owavf):
        self.d *= 32767
        fp = wv.open(owavf, 'wb')
        fp.setnchannels(self.c)
        fp.setframerate(self.fs)
        fp.setsampwidth(self.wf.getsampwidth())
        fp.writeframes(sp.int16(self.d).tostring())
        fp.close()
