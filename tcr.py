#!/usr/bin/python

# Test Case Redux v1.0 - (c) Dem 2013

import sys,os,subprocess,time,re

def main():

  if len(sys.argv) != 6:
    print
    print "[*] Test Case Redux v1.0 (C) Dem 2013"
    print
    print "[*] Usage: " + sys.argv[0] + " application original-file mutated-file crashreporter_name delay"
    print
    sys.exit(1)
  
  app = sys.argv[1]
  ori = sys.argv[2]
  mut = sys.argv[3]
  name = sys.argv[4]
  delay = int(sys.argv[5])
  temp = "/private//var/www/temp.mov"
  listdir = "/private/var/mobile/Library/Logs/CrashReporter"
  if os.path.exists(ori):
    fa = open(ori, "rb")
  else:
    print "\n" + ori + " not found\n"
    sys.exit(1)  
  if os.path.exists(mut):
    fb = open(mut, "rb")
  else:
    print "\n" + mut + " not found\n"
    sys.exit(1)
  size = os.path.getsize(ori)
  crashatstart = 0
  crash = 0

  ba = bytearray(fa.read())
  fa.close()
  bb = bytearray(fb.read())
  fb.close()
  dir = os.listdir(listdir)
  for f in dir:
    match = re.search(name, f)
    if match:
      crashatstart += 1
  print "\nTesting Different Offsets"
  print "-------------------------\n"  
  for i in range(size):
    bite = ba[i]
    bote = bb[i]
    if bite != bote:
      print "offset: " + hex(i)
      ba[i] = bb[i]
      if os.path.exists(temp):
        os.remove(temp)
      fc = open(temp, "wb")
      fc.write(ba)
      fc.close()
      subprocess.call(["sbopenurl", "http://localhost/temp.mov"])
      time.sleep(delay)
      subprocess.call(["killall", app])
      crash = 0
      dir = os.listdir(listdir)
      for f in dir:
        match = re.search(name, f)
        if match:
          crash += 1
      if crash > crashatstart:
        print "\nmagic offset: " + hex(i) + "\n"
        sys.exit(0)

  if os.path.exists(temp):
    os.remove(temp)
  sys.exit(0)

if __name__ == "__main__":
    main()
