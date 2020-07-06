#			
# 			   			  Plitecnico Di Milano
#
#  						Wireless Internet Project 
# 					on Counting how many people are 
# 				present in a classroom via traffic sniffing
#
# 								Professor:  
#			 		 ALESSANDRO ENRICO CESARE REDONDI 
# 
# 						 		 Student:
# 							    Hiva Amiri
# 								 10696153


from collections import Counter
from scapy.all import *
import time 
from datetime import datetime
from threading import Thread, Lock
import csv
import os.path
from os import path
from datetime import datetime
import csv



# A list of MAC list
maclist = []
# A list of stored records
mlist = [[" Time   ", " MAC Adress      ","dBm","Serached for SSID"]]

# 888888888888888888888888888888888888888888888888888888888888

# class of thread
class MonitoringThread(Thread):
	def __init__(self, iface):
		Thread.__init__(self)
		self.iface = iface
		print 'Ready to monitoring'
		print '>>>>>>>>>>>>>>>>>>>'
		print '<<<<<<<<<<<<<<<<<<<'
# 888888888888888888888888888888888888888888888888888888888888	
	# Time function to return current time
	def timee(self):
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		return current_time
# 888888888888888888888888888888888888888888888888888888888888
	# function of reading packets
	def PacketHandler(self,pkt):
		# if rceived packet is a Probe Request
		if pkt.haslayer(Dot11ProbeReq):
			# if Probe Request has SSID; some probe requests has no SSID in its payload, we don't consider them
			if len(pkt.info) > 0:
				testcase = pkt.addr2 + '---' + pkt.info
				testmac = pkt.addr2
				# add MAC address of recived packet to the list if it's not on the list already
				if testmac not in maclist:
					print "\nNew User Found  >>> " + pkt.addr2 + "  " + pkt.info
					maclist.append(testmac)
					#add some other information of the received packet to the list
					mlist.append([self.timee(), pkt.addr2,pkt.dBm_AntSignal, pkt.info])
					print '\n======================> Probes in List <======================\n'
					counter = 0
					
					#print MAC address in the list
					for macs in range(0, len(mlist)):
						print str(counter)+" |  "\
						+  str(mlist[macs][0])+" |  "\
						+str(mlist[macs][1])+" |  "\
						+str(mlist[macs][2])+" |    "\
						+str(mlist[macs][3])
						counter += 1
						
					print '\n================> Devices around:'+ str(len(mlist)-1) +' Device(s) <================\n'
					print '\n>> Press Ctrl+Z to terminate monitoring'					
					print '>> Monitoring result will be saved at source folder as a .CSV file.\n'					

					#write list of MAC addresses to a csv file
					with open('export.csv', 'wb') as myfile:
						wr = csv.writer(myfile)
						for rows in range (0, len(mlist)):
							wr.writerow(mlist[rows])
# 888888888888888888888888888888888888888888888888888888888888
	def run(self):
		# calling sniff function of Scapy to sniff packets from iface which its value defined by user
		# while starting the script from command line
		sniff(iface = sys.argv[1], prn = self.PacketHandler)


# 888888888888888888888888888888888888888888888888888888888888
#defining thread
thread1 = MonitoringThread(sys.argv[1])
thread1.start()
