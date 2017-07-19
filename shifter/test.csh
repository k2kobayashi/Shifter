#! /bin/csh
#
# test.csh
#   First edition: 2017-04-26
#
#   Copyright (C) 2017
#        Kazuhiro KOBAYASHI <kazuhiro-k@is.naist.jp>
#
#   Distributed under terms of the MIT license.
#

set pydir = .

rm $pydir/*.pyc

set f0rates = (0.5 0.75 1.0 1.5 2.0)

foreach f0rate ($f0rates)
    python main.py \
        -nmsg \
        -f0rate $f0rate \
        $pydir/data/in.wav \
        $pydir/data/out_$f0rate.wav
    echo $pydir/data/out_$f0rate.wav
end
