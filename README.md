# BaumerLaser
 Python interface for Baumer OM70 Laser Distance Sensor  OM70-P1500.HV1500.EK
https://www.baumer.com/us/en/product-overview/distance-measurement/laser-distance-sensors-/high-performance/c/37027
https://www.baumer.com/ch/en/product-overview/distance-measurement/laser-distance-sensors-/high-performance/large-measuring-distances-up-to-1500-mm/om70-p1500-hv1500-ek/p/42057

High performance distance sensor with Ethernet and web interface
Device has built in web server for configuration and supports a variety of network protocols
We use UDP point:point protocol for this demo, and later integration into our Trio/Python async code

BaumerOM70 subfolder holds the Data object that is extracted from the UDP packet.
Documentation on the format is in the manual available from above links
The python struct module makes the parsing from binary array nearly trivial

Two tidbits NOT mentioned in the manual:
1) Baumer uses Little Endian binary format for the data packets, while "network format" standard is BigEndian. Easy enough for struct module to handle
2) Web interface provides IP address/port for UDP - this is the TARGET device for 1:1 communication. NOT broadcast.

 