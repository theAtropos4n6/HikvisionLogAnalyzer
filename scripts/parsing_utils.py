#Based on the major type of the log is structured differenetly
#Here I try to map data from each list index to the corresponding column within the log.
import scripts.html_report_files as hrf
def parse_Operation(current_log,curent_dict):
	try:
		if current_log[3] == "HDD Detect":
			curent_dict["Minor Type"] = current_log[3]
			if current_log[4].startswith("HDD"):
				curent_dict["Details"].append(current_log[4])
			else:
				curent_dict["Local/Remote User"] = current_log[4]
				curent_dict["Details"].append(current_log[5])
		elif current_log[3] == "Local: Configure Parameters":
			curent_dict["Minor Type"] = current_log[3]
			if 0 < len(current_log[4]) <= 3:
				curent_dict["Channel No."] = current_log[4]
				curent_dict["Local/Remote User"] = current_log[5]
				curent_dict["Details"].append(current_log[6])
			else:
				curent_dict["Local/Remote User"] = current_log[4]
				if len(current_log) > 5:
					curent_dict["Details"].append(current_log[5])
				else:
					pass#No Details data within entry
		elif current_log[3] == "Local: Initialize HDD":
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Local/Remote User"] = current_log[4]
			curent_dict["Details"].append(current_log[5])
		elif current_log[3] == "Remote: Initialize HDD":
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Channel No."] = current_log[4]
			curent_dict["Local/Remote User"] = current_log[5]
			curent_dict["Remote Host IP"] = current_log[6]
			curent_dict["Details"].append(current_log[7])
		elif current_log[3] in ["Local: Login","Local: Logout","Local: Reboot","Local: Shutdown"]:
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Local/Remote User"] = current_log[4]
		elif current_log[3] == "Power On":
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Details"].append(current_log[4])
		elif current_log[3] in ["Remote: Alarm Arming","Remote: Export Config File","Remote: Get Parameters","Remote: Get Working Status","Remote: Login","Remote: Logout"]:
			curent_dict["Minor Type"] = current_log[3]
			if current_log[4] == "P2P":
				curent_dict["Local/Remote User"] = current_log[4]
			else:
				curent_dict["Local/Remote User"] = current_log[4]
				curent_dict["Remote Host IP"] = current_log[5]
		elif current_log[3] == "Remote: Alarm Disarming":
			curent_dict["Minor Type"] = current_log[3]
			if len(current_log) > 4:
				curent_dict["Local/Remote User"] = current_log[4]
				curent_dict["Remote Host IP"] = current_log[5]
			else:
				pass#No other data available within entry
		elif current_log[3] in ["Remote: Configure Parameters","Remote: Playback by Time"]:
			curent_dict["Minor Type"] = current_log[3]
			if 0 < len(current_log[4]) <= 3:
				curent_dict["Channel No."] = current_log[4]
				curent_dict["Local/Remote User"] = current_log[5]
				curent_dict["Remote Host IP"] = current_log[6]
				curent_dict["Details"].append(current_log[7])
			else:
				curent_dict["Local/Remote User"] = current_log[4]
				curent_dict["Remote Host IP"] = current_log[5]
				if len(current_log) == 7:
					curent_dict["Details"].append(current_log[6])
				else:
					pass#No Details data within entry
		elif current_log[3] == "Local: Abnormal Shutdown":
			curent_dict["Minor Type"] = current_log[3]	
		else:
			hrf.mylogger("Unknown Operation=> Unidentified Minor Type Found. Check Entry: "+str(current_log))
	except Exception as e:
		hrf.mylogger(f"An error occured during parse_Operation. Check Entry: {str(current_log)}. The error message was {e}")

def parse_Information(current_log,curent_dict):
	try:
		if current_log[3] in ["S.M.A.R.T. Information","Start Record","Stop Record","HDD Information"]:
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Channel No."] = current_log[4]
			curent_dict["Details"].append(current_log[5])
		elif current_log[3] == "System Running State":
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Details"].append(current_log[4])
		elif current_log[3].startswith("CIVIL alarm time interval:"):
			curent_dict["Details"].append(current_log[3])
		elif current_log[3].startswith("Time Sync."):
			curent_dict["Minor Type"] = current_log[3]			
		else:
			hrf.mylogger("Unknown Information=> Unidentified Minor Type Found. Check Entry: "+str(current_log))
	except Exception as e:
		hrf.mylogger(f"An error occured during parse_Information. Check Entry: {str(current_log)}. The error message was {e}")

def parse_Exception(current_log,curent_dict):
	try:
		if current_log[3] == "Illegal Login":
			curent_dict["Minor Type"] = current_log[3]
			if len(current_log)> 4:
				curent_dict["Local/Remote User"] = current_log[4]
				curent_dict["Remote Host IP"] = current_log[5]
			else:
				pass#No other data within entry
		elif current_log[3] == "System Running State":
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Details"].append(current_log[4])
		elif current_log[3] in ["Hik-Connect Offline Exception","Network Disconnected"]:
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Details"].append(current_log[4])
		elif current_log[3] == "HDD Error":
			curent_dict["Minor Type"] = current_log[3]
			if 0 < len(current_log[4]) <= 3:
				curent_dict["Channel No."] = current_log[4]
				curent_dict["Details"].append(current_log[5])
			else:
				curent_dict["Details"].append(current_log[4])
		else:
			hrf.mylogger("Unknown Exception=> Unidentified Minor Type Found. Check Entry: "+str(current_log))
	except Exception as e:
		hrf.mylogger(f"An error occured during parse_Exception. Check Entry: {str(current_log)}. The error message was {e}")	
		
def parse_Alarm(current_log,curent_dict):
	try:
		if current_log[3] in ["Start Motion Detection","Stop Motion Detection","Start Video Tampering","Stop Video Tampering"]:
			curent_dict["Minor Type"] = current_log[3]
			curent_dict["Channel No."] = current_log[4]
		else:
			hrf.mylogger("Unknown Alarm=> Unidentified Minor Type Found. Check Entry: "+str(current_log))
	except Exception as e:
		hrf.mylogger(f"An error occured during parse_Alarm. Check Entry: {str(current_log)}. The error message was {e}")	