import binascii
import datetime
from datetime import timezone
import codecs
import re
import csv
import time
import os
import scripts.html_report_files as hrf

#Supported_log_types
global minor_type_dict,last_update
last_update = "2024-06-18 10:00:00 UTC+00:00"
minor_type_dict = {
"Operation":{
	"4100":["Power On", "Parsed"], #Parsed #Parsed
	"4200":["Local: Shutdown", "Parsed"], #Parsed #Parsed
	"4300":["Local: Abnormal Shutdown", "Parsed"], #Parsed #Parsed
	"5000":["Local: Login", "Parsed"], #Parsed #Parsed 
	"5100":["Local: Logout", "Parsed"], #Parsed #Parsed 
	"5200":["Local: Configure Parameters", "Details field is currently not parsed"],  #Skipped
	"5c00":["Local: Initialize HDD", "Partially Parsed"], ##Partially Parsed #Partially Parsed
	"6e00":["HDD Detect", "Partially Parsed"], ##Partially Parsed #Partially Parsed
	"7000":["Remote: Login", "Parsed"], #Parsed #Parsed
	"7100":["Remote: Logout", "Parsed"], #Parsed #Parsed
	"7600":["Remote: Get Parameters", "Parsed"],#Parsed #Parsed
	"7700":["Remote: Configure Parameters","Details field is currently not parsed"],  #Skipped
	"7800":["Remote: Get Working Status", "Parsed"], #Parsed #Parsed
	"7900":["Remote: Alarm Arming", "Parsed"], #Parsed #Parsed
	"7a00":["Remote: Alarm Disarming", "Parsed"], #Parsed #Parsed
	"8000":["Remote: Playback by Time","Details field is currently not parsed"],  #Skipped
	"8200":["Remote: Initialize HDD","Partially Parsed"], #Partially Parsed #Partially Parsed
	"8600":["Remote: Export Config File", "Parsed"] #Parsed #Parsed
	},
"Information":{
	"a000":["Time Sync.","Details field is currently not parsed"], #Skipped - More data reside in log entry than is extracted by Hikvision DVR
	"a100":["HDD Information", "Parsed"], #Parsed #Parsed
	"a200":["S.M.A.R.T. Information", "Partially Parsed"], ##Partially Parsed #Partially Parsed
	"a300":["Start Record", "Partially Parsed"], ##Partially Parsed #Partially Parsed
	"a400":["Stop Record", "Partially Parsed"], ##Partially Parsed #Partially Parsed
	"aa00":["System Running State","Details field is currently not parsed"],  #Skipped
	"b800":["b800 - Unknown Minor Type","Details field is currently not parsed"]  #Skipped
	},
"Alarm":{
	"0300":["Start Motion Detection", "Parsed"], #Parsed #Parsed
	"0400":["Stop Motion Detection", "Parsed"], #Parsed #Parsed
	"0500":["Start Video Tampering", "Parsed"], #Parsed #Parsed
	"0600":["Stop Video Tampering", "Parsed"] #Parsed #Parsed
	},
"Exception":{
	"2200":["Illegal Login", "Parsed"], #Parsed #Parsed 
	"2400":["HDD Error","Details field is currently not parsed"],  #Skipped
	"2700":["Network Disconnected","Details field is currently not parsed"], #Skipped - Falsy parsed from Hikvision DVR itself. It sais Nic:LAN1 whereas the log entry stated eth0
	"5400":["Hik-Connect Offline Exception","Details field is currently not parsed"]   #Skipped
	}
}
#######################################################################################################
"""The following block of code holds the basic carving method for image files"""
#######################################################################################################


def carved_logfiles(input_file):
	try:
		offset = 0
		blocksize = 512
		fs_signature ='48494b564953494f4e4048414e475a484f55' #HIKVISION@HANGZHOU

		with open(input_file,'rb') as img_file:
			global offsets
			global log_start_offset
			global log_size
			global alt_test
			global alt_offset
			global fs_info
			log_start_offset = 0
			log_size = 0
			offsets = ['']
			alt_offset = 41472
			# alt_test = False
			while True:
				if offset == alt_offset: #checks if log start at offset 41472 regardless of where the fs header states
					log_data = img_file.read(10*log_size) # read the whole block where the logs reside || the number 10 needs to be formalised since is a made up number. We need to identify exactly the size of logs in this case
					log_data_to_str = binascii.hexlify(log_data).decode('utf-8') #convert to big string
					if log_data_to_str.startswith("52415453"):
						# alt_test = True
						log_start_offset = offset
						# hrf.mylogger(f"The start offset now is {log_start_offset}")
						# hrf.mylogger(f"The log size now is {log_size}")
						fs_info[0] = offset
						# hrf.mylogger(len(log_data_to_str))
						carved_info = parse_log_data(log_data_to_str,log_start_offset,"Alternative") #if mytest == True else parse_log_data(log_data_to_str,log_start_offset,"Alternative")# pass it on for parsing -> returned value is a dictionary where key is the no. of log entry and value is the extracted data
						break#searching finishes as soon as the dict returns
					img_file.seek(offset)
				data = img_file.read(blocksize) # read image per blocksize
				blk_to_str = binascii.hexlify(data).decode('utf-8')
				if not data:
					hrf.mylogger("Searched the whole image and no HikVision File System was found!\n")
					break #continues till the end of image
				if fs_signature in blk_to_str: # if == HIKVISION@HANGZHOU
					offsets = parse_fs_info(blk_to_str) #retrieves fs info, offset etc.
					log_start_offset = offsets[0]
					log_size = offsets[1]
					fs_info = offsets
				offset += blocksize
				if log_size > 0 and offset == log_start_offset: #when reading iteration reach the offset where the logs begin
					log_data = img_file.read(log_size) # read the whole block where the logs reside
					log_data_to_str = binascii.hexlify(log_data).decode('utf-8') #convert to big string
					carved_info = parse_log_data(log_data_to_str,log_start_offset) #if mytest == True else parse_log_data(log_data_to_str,log_start_offset,"Alternative")# pass it on for parsing -> returned value is a dictionary where key is the no. of log entry and value is the extracted data
					break#searching finishes as soon as the dict returns
				
		return [carved_info,fs_info]
	except Exception as e:
		hrf.mylogger(f"Error occured while reading image file. The error message was {e}\n")



#######################################################################################################
"""The following block of code holds all the methods used in carving logs from image files"""
#######################################################################################################

#File System Information 
def parse_fs_info(blck):
	fs_sig = bytes.fromhex(blck[32:68]).decode('ASCII') #hrf.mylogger FS SIGNATURE
	fs_version = bytes.fromhex(blck[96:124]).decode('ASCII')

	disk_size_in_hex = bytearray.fromhex(blck[144:160])
	disk_size_le = int.from_bytes(disk_size_in_hex,"little")
	disk_size_in_mb = (disk_size_le/1024)/1024
	
	offset_to_system_logs_in_hex = bytearray.fromhex(blck[192:208])
	offset_to_system_logs_le = int.from_bytes(offset_to_system_logs_in_hex,"little")

	size_of_system_logs_in_hex = bytearray.fromhex(blck[208:224])
	size_of_system_logs_le = int.from_bytes(size_of_system_logs_in_hex,"little")
	size_of_system_logs_in_b = size_of_system_logs_le #already in bytes

	init_time = convert_date(blck[480:488])

	log_start_offset = offset_to_system_logs_le
	log_end_offset = log_start_offset+size_of_system_logs_le

	# hrf.mylogger(f'The size of disk is: {int(disk_size_in_mb)} MB')
	# hrf.mylogger(f"The size of system logs' space is: {int(size_of_system_logs_in_b)} Bytes")
	# hrf.mylogger(f"The system initialisation time is: {init_time} UTC+00:00")
	return [log_start_offset, size_of_system_logs_le,int(disk_size_in_mb),int(size_of_system_logs_in_b),str(init_time),str(fs_sig)]

def parse_log_data(blck,current_offset,rtype="Generic"):
	file_signature = "52415453" #magic bytes 'RATS' of logfiles.
	logs_list = blck.split(file_signature)  #A list is created where each index is a logfile
	# hrf.mylogger(len(logs_list[0])/2)
	if rtype == "Generic":
		entry_offset = current_offset+len(logs_list[0])//2#+len(file_signature)
	elif rtype == "Alternative":
		entry_offset = current_offset
	hrf.mylogger(f'There are {len(logs_list)-1} log entries\n') #-1 because the 1st list item is not needed e.g. 0000000,52415453
	counter = 1
	log_results = {}
	try:
		for log_entry in logs_list:
			if log_entry.startswith("14") or log_entry.startswith("01"): # All slicing needs to take into account the 14 00 00 00 or older 01 00 00 00 that resides before the beginning of date bytes and after the magic bytes header
				log_date = convert_date(log_entry[8:16]) #Parses log date. Standard offset
				major_type = get_MajorType(log_entry[16:20]) #Parses major type. Standard offset
				minor_type = get_MinorType(major_type,log_entry[20:24]) #Parses minor type. Standard offset
				try:
					decription = get_Description(major_type,minor_type,log_entry[24:]) #Attempt to parse details field. Variable offset
					log_results[counter] = str(log_date)+"#;#"+major_type+"#;#"+minor_type+"#;#"+str(decription[0])+"#;#"+decription[1]+"#;#"+decription[2]+"#;#"+decription[3]+"#;#"+decription[4]+"#;#"+str(int(entry_offset))
				except Exception as e:
					hrf.mylogger(f"Error parsing log entry at {entry_offset} offset. The error is: {e}\n")
					decription = f'Error occured while parsing this record'
					log_results[counter] = str(log_date)+"#;#"+major_type+"#;#"+minor_type+"#;#"+""+"#;#"+""+"#;#"+""+"#;#"+decription+"#;#"+""+"#;#"+str(int(entry_offset))
				entry_offset += int(len(file_signature)/2+len(log_entry)/2)
				counter+=1
				#hrf.mylogger(f'Log Date: {log_date} Major type: {major_type} Minor type: {minor_type} Details: {decription[0]} {decription[1]}')
		return log_results
	except Exception as e:
		hrf.mylogger(f"Error occured while creating dict from carved image file (parse_log_data). The error message was {e}\n")

#Major Type Mapping
def get_MajorType(major_type):
	if major_type == "0100":
		mtype = "Alarm"
	elif major_type == "0200":
		mtype = "Exception"
	elif major_type == "0300":
		mtype = "Operation"
	elif major_type == "0400":
		mtype = "Information"
	else:
		mtype = "Unknown Major Type"+f'{major_type}'
	return mtype

#Minor Type Mapping 
def get_MinorType(major_type,minor_type):
	#if major_type in minor_type_dict.keys():
	if major_type in minor_type_dict:
		#if minor_type in minor_type_dict[major_type].keys():
		if minor_type in minor_type_dict[major_type]:
			minor_type_code = minor_type_dict[major_type][minor_type][0]
		else:
			minor_type_code = f"Unknown Minor Type: {minor_type}"
	else:
		minor_type_code = f"Unknown Major Type: {major_type}"
	return minor_type_code


#IP Extraction - currently support IPv4 IPs
def parse_IP(ip_string): 
	try:
		IP_hex = []
		IP = ""
		IP_str = ""
		IP_hex.append(bytearray.fromhex(ip_string[0:2]))# first_IP_part 
		IP_hex.append(bytearray.fromhex(ip_string[2:4]))# second_IP_part
		IP_hex.append(bytearray.fromhex(ip_string[4:6]))# third_IP_part
		IP_hex.append(bytearray.fromhex(ip_string[6:8]))# fourth_IP_part
		for i in IP_hex:
			IP_str += str(int.from_bytes(i,"little"))+"."
		IP = "" if IP_str == "0.0.0.0." else IP_str.rstrip(".") 
		return IP
	except:
		hrf.mylogger("Error while extraction IP info. Check method parse_IP")

#User Extraction
def parse_User(user_string):
	try:
		user_in_hex = user_string
		user_in_bytes = bytes(user_in_hex,encoding='utf-8')
		user_decode_str = codecs.decode(user_in_bytes,"hex")
		user_str = str(user_decode_str,'utf-8').replace("\x00","")
		return user_str
	except:
		hrf.mylogger("Error while extraction user info. Check method parse_User")



##############################################################################################################################################################################################################
#The core of the parser. This is the result of our reverse engineering of the log files structure. This section needs regular refinement to extend support
##############################################################################################################################################################################################################

def get_Description(major_type,minor_type,description):
	details_field = [] # Results of the parsing function is returned as list: 0-> Channel No. 1->user info 2->IP info 3-> Details 4->Parsing Status
	if major_type == "Operation" and minor_type in ['Remote: Login','Remote: Logout','Remote: Alarm Disarming','Remote: Alarm Disarming','Remote: Get Working Status','Remote: Export Config File','Remote: Get Parameters']:
		channel_no = ""
		user_info = parse_User(description[:32])
		ip_info = parse_IP(description[32:40])
		details_info = ""
		parsing_status = "Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	elif major_type == "Information" and minor_type == "S.M.A.R.T. Information":
		channel_no = ""
		user_info = ""
		ip_info = ""
		parsing_status = "Partially Parsed"

		serial_in_bytes = bytes(description[-44:],encoding='utf-8')
		serial_decode_str = codecs.decode(serial_in_bytes,"hex")
		serial_str = str(serial_decode_str,'utf-8').replace("\x00","")
		#ip_info = "Serial = "+serial_str

		model_in_bytes = bytes(description[-128:-44],encoding='utf-8')
		model_decode_str = codecs.decode(model_in_bytes,"hex")
		model_str = str(model_decode_str,'utf-8').replace("\x00","")

		firm_in_bytes = bytes(description[-144:-128],encoding='utf-8')
		firm_decode_str = codecs.decode(firm_in_bytes,"hex")
		firm_str = str(firm_decode_str,'utf-8').replace("\x00","")	

		#details_info = "Serial = "+serial_str+", Model = "+model_str + ", Firmware = "+ firm_str
		details_info = f"Serial = {serial_str}, Model = {model_str}, Firmware = {firm_str}"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)

	elif major_type == "Information" and minor_type == "HDD Information":
		channel_no = ""
		user_info = ""
		ip_info = ""
		parsing_status = "Parsed"

		hdd_in_bytes = bytes(description[88:90],encoding='utf-8')
		hdd_decode_str = codecs.decode(hdd_in_bytes,"hex")
		hdd_str = str(hdd_decode_str,'utf-8').replace("\x00","")		

		serial_in_bytes = bytes(description[-144:-112],encoding='utf-8')
		serial_decode_str = codecs.decode(serial_in_bytes,"hex")
		serial_str = str(serial_decode_str,'utf-8').replace("\x00","")

		model_in_bytes = bytes(description[-80:-48],encoding='utf-8')
		model_decode_str = codecs.decode(model_in_bytes,"hex")
		model_str = str(model_decode_str,'utf-8').replace("\x00","")	
		
		firm_in_bytes = bytes(description[-104:-94],encoding='utf-8')
		firm_decode_str = codecs.decode(firm_in_bytes,"hex")
		firm_str = str(firm_decode_str,'utf-8').replace("\x00","")	

		#details_info = "HDD: "+hdd_str+", Serial: "+serial_str+", Firmware: "+ firm_str + ", Model: "+model_str
		details_info = f"HDD: {hdd_str}, Serial: {serial_str}, Firmware: {firm_str}, Model: {model_str}"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)

	elif major_type == "Operation" and minor_type == "Power On":
		channel_no = ""
		user_info = ""
		ip_info = ""
		parsing_status = "Parsed"

		#Model: Located at offset 0x60 
		model_in_bytes = bytes(description[160:224],encoding='utf-8')
		model_decode_str = codecs.decode(model_in_bytes,"hex")
		model_str = str(model_decode_str,'utf-8').replace("\x00","")

		#Serial No.:Located at 0xA0
		serial_in_bytes = bytes(description[-144:-80],encoding='utf-8')
		serial_decode_str = codecs.decode(serial_in_bytes,"hex")
		serial_str = str(serial_decode_str,'utf-8').replace("\x00","")

		#Firmware version: Located at 0xD0 Build 0xD4, Encoding version: 0xD8, Build 0xDC
		firm_in_bytes = [bytearray.fromhex(description[-48:-44]),bytearray.fromhex(description[-44:-42]),bytearray.fromhex(description[-42:-40])]
		firm_str = [int.from_bytes(firm_in_bytes[0],"little"),int.from_bytes(firm_in_bytes[1],"little"),int.from_bytes(firm_in_bytes[2],"little")]

		fbuild_in_bytes = [bytearray.fromhex(description[-40:-38]),bytearray.fromhex(description[-38:-36]),bytearray.fromhex(description[-36:-32])]
		fbuild__str = [int.from_bytes(fbuild_in_bytes[0],"little"),int.from_bytes(fbuild_in_bytes[1],"little"),int.from_bytes(fbuild_in_bytes[2],"little")]
		
		encoding_in_bytes = [bytearray.fromhex(description[-32:-28]),bytearray.fromhex(description[-28:-26])]
		encoding__str = [int.from_bytes(encoding_in_bytes[0],"little"),int.from_bytes(encoding_in_bytes[1],"little")]
		
		sbuild_in_bytes = [bytearray.fromhex(description[-24:-22]),bytearray.fromhex(description[-22:-20]),bytearray.fromhex(description[-20:-18])]
		sbuild__str = [int.from_bytes(sbuild_in_bytes[0],"little"),int.from_bytes(sbuild_in_bytes[1],"little"),int.from_bytes(sbuild_in_bytes[2],"little")]

		# details_info = "Model: "+model_str+", "+\
		# 			"Serial No.: "+serial_str+", "\
		# 			"Firmware: V"+ str(firm_str[0])+"."+str(firm_str[1])+"."+str(firm_str[2])+","+\
		# 			"Build: "+str(fbuild__str[2])+str(fbuild__str[1]).zfill(2)+str(fbuild__str[0])+\
		# 			", Encoding version: V"+str(encoding__str[1])+"."+str(encoding__str[0])+\
		# 			", Build: "+str(sbuild__str[2])+str(sbuild__str[1]).zfill(2)+str(sbuild__str[0])
		details_info = f"Model: {model_str}, Serial No.: {serial_str}, Firmware: V{firm_str[0]}.{firm_str[1]}.{firm_str[2]}, Build: {str(fbuild__str[2])}{str(fbuild__str[1]).zfill(2)}{str(fbuild__str[0])}, Encoding version: V{str(encoding__str[1])}.{str(encoding__str[0])}, Build: {str(sbuild__str[2])}{str(sbuild__str[1]).zfill(2)}{str(sbuild__str[0])}"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	elif major_type == "Exception" and minor_type == "Illegal Login":
		channel_no = ""
		user_info = parse_User(description[:32])
		ip_info = parse_IP(description[40:48])
		details_info = ""
		parsing_status = "Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	elif major_type == "Operation" and minor_type in ["Local: Login","Local: Logout"]:
		channel_no = ""
		user_info = parse_User(description[:32])
		ip_info = ""
		details_info = ""
		parsing_status = "Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)

	elif major_type == "Operation" and minor_type == "Remote: Initialize HDD":
		channel_no = ""
		user_info = parse_User(description[:32])
		ip_info = parse_IP(description[32:40])
		details_info = ""
		parsing_status = "Partially Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)

	elif major_type == "Operation" and minor_type == "Local: Initialize HDD":
		channel_no = ""
		user_info = parse_User(description[:32])
		ip_info = ""
		details_info = ""
		parsing_status = "Partially Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)

	elif major_type == "Alarm" and minor_type in ["Start Motion Detection","Stop Motion Detection","Start Video Tampering","Stop Video Tampering"]:
		camera = description[:2]
		camera_hex = bytearray.fromhex(camera)
		camera_le = int.from_bytes(camera_hex,"little")
		channel_no = camera_le
		user_info = ""
		ip_info = ""
		details_info = ""
		parsing_status = "Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	elif major_type == "Operation" and minor_type == "HDD Detect":
		channel_no = ""
		user_info = ""
		ip_info = ""
		parsing_status = "Partially Parsed - 'HDD No.:' field is not parsed"

		test_method_hex = description[-8:-6]
		if test_method_hex == "01":
			test_method = "Short Test"
		elif test_method_hex == "02":
			test_method = "Expanded Test"
		else:
			test_method = "Unknown"

		test_type_hex = description[-96:-94]
		if test_type_hex == "B2":
			test_type = "Repair Database Start"
		elif test_type_hex == "B3":
			test_type = "Repair Database End"
		else:
			test_type = "Unknown"
		hdd_no = "Unknown"
		details_info = f"HDD No.: {hdd_no}, Test type: {test_type}, Test method: {test_method}"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	elif major_type == "Operation" and minor_type == "Local: Shutdown":
		channel_no = ""
		user_info = parse_User(description[:32])
		ip_info = ""
		details_info = ""
		parsing_status = "Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	elif major_type == "Operation" and minor_type == "Local: Abnormal Shutdown":
		channel_no = ""
		user_info = ""
		ip_info = ""
		details_info = ""
		parsing_status = "Parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	elif major_type == "Information" and minor_type in ["Start Record","Stop Record"]: 
		user_info = ""
		ip_info = ""
		parsing_status = "Partially Parsed"

		status =  "starts" if minor_type == "Start Record" else "stops"
		camera = description[-96:-94] #Camera: A2
		camera_hex = bytearray.fromhex(camera)
		camera_le = int.from_bytes(camera_hex,"little")
		stream_type = description[-72:-70]
		record_enabled = "Yes" if description[-80:-78] == "01" else "No"#Record enabled: Yes,
		event_params = "Enabled" if description[-78:-76] == "01" else "Disabled"#Event parameters: Enabled, 
		record_type_status = description[-76:-74]#Record type: Event, 
		if record_type_status == "09":
			record_type = "Event"
		elif record_type_status ==  "00":
			record_type = "Continuous"
		else:
			record_type = "Unknown"

		motion_detection_status = description[-64:-62]#Motion detected on camera: None,
		if motion_detection_status == "00":
			motion_detection_le = "None"
		else:			
			motion_detection_cam = bytearray.fromhex(motion_detection_status)
			motion_detection_le = int.from_bytes(motion_detection_cam,"little")

		if stream_type == "01": #0x01 denote =>Stream type: Sub-Stream whereas 0x00 => Stream type: Main Stream
			stream = ", Stream type: Sub-Stream"
		elif stream_type == "00":
			stream = ", Stream type: Main Stream"
		else:
			stream = ", Stream type: Unknown Stream"
		channel_no = str(camera_le)
		#details_info = "Camera: "+ str(camera_le)+" "+status+" recording."+", Record enabled: "+record_enabled+", Event parameters: "+event_params+", Record type: "+record_type+", Stream type: Main Stream"+stream+", Motion detected on camera: "+str(motion_detection_le)
		details_info = f"Camera: {str(camera_le)} {status} recording. Record enabled: {record_enabled}, Event parameters: {event_params}, Record type: {record_type}, Stream type: Main Stream{stream}, Motion detected on camera: {str(motion_detection_le)}"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	
	else: 
		channel_no = ""
		user_info = ""
		ip_info = ""
		details_info = ""
		parsing_status = "Details field is currently not parsed"
		multiple_values = [channel_no,user_info,ip_info,details_info,parsing_status]
		details_field.extend(multiple_values)
	return details_field

def convert_date(hex_date): #date is stored in hex is stored in utc but when exporting logs they are exported in configured time zone
	log_date_hex = bytearray.fromhex(hex_date)
	log_date_le = int.from_bytes(log_date_hex,"little")
	log_date = datetime.datetime.utcfromtimestamp(log_date_le)#,tz=timezone.utc) #If UTC is needed add ,tz=timezone.utc) 
	return log_date



