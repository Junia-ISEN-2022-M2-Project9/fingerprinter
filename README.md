# Fingerprinter

This project aims to improve usability of the library hfinger https://github.com/CERT-Polska/hfinger
The main goal is to reuse functions (with improvements) to generate fingerprints from json keys.

# To date

Current progress is in _advens.py_. This file reads a pcap and output a list of fingerprints in a txt file. Actions are
logged but still uneffective in case a fingerprint can't be generated, the program then crash and abort every previous
fingerprint found.

## Hfinger

Research were made on how hfinger process pcap, functions were used one by one to decompose behavior :

1. Init logger
2. Parse args
3. Run tshark and output to json
4. Fix tmp json if needed
5. Read json > format keys
6. Call functions to hash infos
7. Return a whole line

# Devlopment

- pcap fingerprinting
    - Multithread
    - Handle errors and pursue process
- json entry
    - Check legitimacy of entry first
    - Read needed keys
    - Format for usability
    - Process

# Usage example
> hfingerprinter.py -f files/onlyhttp.pcap -ot out -l test

> python3 sortFingerprint.py /files/GlobeImposter /files/wannaCry /files/Phobos
