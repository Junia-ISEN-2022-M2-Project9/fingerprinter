# Fingerprinter

This project aims to improve usability of the library hfinger https://github.com/CERT-Polska/hfinger
The main goal is to reuse functions (with improvements) to generate fingerprints from json keys.

# To date

There is two entry points.
_hfingerprinter.py_ reads a pcap, filters usable HTTP request through Tshark and output a list of fingerprints in a txt file. Everything is logged if the parameter is set.

_sortfingerprint.py_ reads a fingerprint list and build clusters of fingerprint using machine learning depending on a given threshold. Each cluster is grouped by an algorithm which calculate distances between every fingerprints (can be displayed). 

## Hfinger

Research were made on how hfinger process pcap, functions were used one by one to decompose behavior :

1. Init logger
2. Parse args
3. Run tshark and output to json
4. Fix tmp json if needed
5. Read json > format keys
6. Call functions to hash infos
7. Return a whole line

# Development

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

> sortfingerprint.py files/legitimeFirefox files/legitimeFirefox2 files/wannaCry