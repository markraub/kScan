# K-Mart Photo and Scan Center, or kScan
## For CSH Members, check the [wiki](https://wiki.csh.rit.edu/wiki/KScan) for a guide on how to set up your scan folder in your homedir

* kScan is a service that allows users who have iButtons to scan a document using an Epson Perfection 1670 and send them right to their Computer Science House home directories

* kScan is written in python2.7, and currently runs from the kscan.py file

```
sudo python kscan.py
```

* It will require sudo access in order to listen for iButtons on the 1-wire pin

* kScan reads iButtons independant of any other software or system, it reads it right onto the Raspberry Pi into the following document

```
/sys/devices/w1_bus_master1/w1_master_slaves
```


