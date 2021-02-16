# Python

Script created in order to check a list of switches for directlty connected devices on specific ports in order to learn their mac address and configure it on the specified port statically.

Usually you can just apply mac sticky and write configuration to memory once the MAC address is learned, in our case we want to discover the device and add its MAC address on the port and set it as sticky without waiting for normal traffic to kick off the MAC Learning process.


version 1.7 added exception handling
