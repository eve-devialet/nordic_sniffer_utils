import time
from SnifferAPI import Sniffer

nPackets = 0
mySniffer = None

def setup(device_address):
    global mySniffer
    
    # Initialize the sniffer on COM port COM19.
    mySniffer = Sniffer.Sniffer("/dev/ttyACM0")
    # Or initialize and let the sniffer discover the hardware.
    # mySniffer = Sniffer.Sniffer()
    # Start the sniffer module. This call is mandatory.
    mySniffer.start()

    # Wait to allow the sniffer to discover device mySniffer.
    time.sleep(10)
    # Retrieve list of discovered devicemySniffer.
    d = mySniffer.getDevices()
    if device_address == None:
        for i, dev_found in enumerate(d.asList()):
            addr = ["%2x"%num for num in dev_found.address]
            addr = addr[:-1]
            addr = ':'.join(addr)
            addr = addr.replace(" ", "0")
            print("%d: device found %s with address %s"%(i, dev_found.name,
                                                         addr))
    else:
        # Find device with name "Example".
        #dev = d.find('Phantom')
        dev = d.find(device_address)
        if dev is not None:
            # Follow (sniff) device "Example". This call sends a REQ_FOLLOW command over UART.
            mySniffer.follow(dev)
        else:
            print "Could not find device"

def select_dev():
    global mySniffer
    
    # Initialize the sniffer on COM port COM19.
    mySniffer = Sniffer.Sniffer("/dev/ttyACM0")
    # Or initialize and let the sniffer discover the hardware.
    # mySniffer = Sniffer.Sniffer()
    # Start the sniffer module. This call is mandatory.
    mySniffer.start()

    # Wait to allow the sniffer to discover device mySniffer.
    time.sleep(10)
    # Retrieve list of discovered devicemySniffer.
    d = mySniffer.getDevices()
    for i, dev_found in enumerate(d.asList()):
        addr = ["%2x"%num for num in dev_found.address]
        addr = addr[:-1]
        addr = ':'.join(addr)
        addr = addr.replace(" ", "0")
        print("%d: device found %s with address %s"%(i, dev_found.name,
                                                     addr))
    retry = True
    while(retry):
        retry = False
        print("Choose a device:")
        choice = input("> ")
        try:
            choice = int(choice)
        except:
            print("Invalid choice")
            retry = True

    address = d.asList()[choice].address
    return(address)

def loop(duration = None):
    # Enter main loop
    if duration != None:
        start = time.time()
    nLoops = 0
    while True:
        time.sleep(0.1)
        # Get (pop) unprocessed BLE packets.
        packets = mySniffer.getPackets()
        
        processPackets(packets) # function defined below
        
        nLoops += 1
        
        # print diagnostics every so often
        if nLoops % 20 == 0:
            print mySniffer.getDevices()
            print "inConnection", mySniffer.inConnection
            print "currentConnectRequest", mySniffer.currentConnectRequest
            print "packetsInLastConnection", mySniffer.packetsInLastConnection
            print "nPackets", nPackets
        if time != None:
            if time.time() - start >= duration:
                break
        
# Takes list of packets
def processPackets(packets):
    for packet in packets:
        # packet is of type Packet
        # packet.blePacket is of type BlePacket
        global nPackets
        # if packet.OK:
        # Counts number of packets which are not malformed.
        nPackets += 1
