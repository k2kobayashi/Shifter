NAME
----

Shifter - a command line tool for F0 transformation of a waveform based on WSOLA and resampling

DESCRIPTION
-----------

Shifter is a command line tool to transform F0 without using a vocoding framework.
The F0 transformation is implemented with WSOLA (Waveform Similarity-based Over-Lap Add) [1] and resampling.

-  [1] W. Verhelst and M. Roelands, “An overlap-add technique based on waveform similarity (WSOLA) for
  high quality time-scale modification of speech,” Proc. ICASSP, pp. 554–557 vol.2, Apr. 1993.

USAGE
-----

When the F0 transformation rate set to 2.0, please run following command

    python shifter/main.py -f0rate 2.0 in.wav out.wav

INSTALLATION
------------

### REQUIREMENTS

- Linux or MAC
  - Python v2.7.12
      - numpy
      - scipy


### MANUAL

Grab a copy of Shifter:

    git clone git://github.com/k2kobayashi/shifter.git
KNOWN ISSUES
------------

- Implement setup script
- This tool takes a long time to complete


REPORTING BUGS
--------------

For any questions or issues please visit:

    https://github.com/k2kobayashi/shifter/issues

AUTHORS
-------

Shifter was originally written by Kazuhiro KOBAYASHI.

COPYRIGHT
---------

Copyright © 2017 Kazuhiro KOBAYASHI

Released under the MIT license

https://opensource.org/licenses/mit-license.php