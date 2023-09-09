import scripts.html_report_files as hrf

def parse_logon_info(input_dict):
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if input_dict[k]["Minor Type"] in ["Illegal Login","Remote: Login","Remote: Logout","Local: Login","Local: Logout"]:
				output_dict[counter] = v
				counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while parsing logon info. The error message was {e}") 

def parse_hw_info(input_dict):
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if input_dict[k]["Minor Type"] in ["Power On","HDD Detect","HDD Information","HDD Error","Time Sync.","S.M.A.R.T. Information","Local: Shutdown","Local: Abnormal Shutdown","System Running State","Remote: Initialize HDD","Local: Initialize HDD"]:
				output_dict[counter] = v
				counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while parsing hardware info. The error message was {e}") 

def parse_antiforensics_info(input_dict):
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if input_dict[k]["Minor Type"] in ["Local: Configure Parameters","Remote: Configure Parameters","Remote: Initialize HDD","Local: Initialize HDD","Remote: Export Config File"]:
				output_dict[counter] = v
				counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while parsing antiforensics info. The error message was {e}") 

def retrieve_carved_dict(carved_results):
	try:
		output_dict = {}
		for k,v in carved_results.items():
			item = v.split("#;#")
			output_dict[k] = {	
							"Time": "", 
							"Major Type" : "", 
							"Minor Type": "", 
							"Channel No." : "", 
							"Local/Remote User" : "", 
							"Remote Host IP": "", 
							"Details" : "",
							"Parsing Status" : "",
							"Entry Offset":""
							}
			output_dict[k]['Time'] = item[0]#[:-6] if you want to remove time zone offset
			output_dict[k]['Major Type'] = item[1]
			output_dict[k]['Minor Type'] = item[2]
			output_dict[k]['Channel No.'] = item[3]
			output_dict[k]['Local/Remote User'] = item[4]
			output_dict[k]['Remote Host IP'] = item[5]
			output_dict[k]['Details'] = item[6]
			output_dict[k]['Parsing Status'] = item[7]
			output_dict[k]['Entry Offset'] = item[8]
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while retrieving carved dict (retrieve_carved_dict). The error message was {e}") 

def retrieve_carved_dict_supported(input_dict) :
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if input_dict[k]["Parsing Status"] == "Parsed" or v["Parsing Status"] == "Partially Parsed":
						output_dict[counter] = v
						counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while retrieving carved dict supported (retrieve_carved_dict_supported). The error message was {e}") 	

def carve_logon_info(input_dict,rtype="ALL"):
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if rtype == "ALL":
				if input_dict[k]["Minor Type"] in ["Illegal Login","Remote: Login","Remote: Logout","Local: Login","Local: Logout"]:
					output_dict[counter] = v
					counter += 1
			else:
				if input_dict[k]["Parsing Status"] == "Parsed" or v["Parsing Status"] == "Partially Parsed":
					if input_dict[k]["Minor Type"] in ["Illegal Login","Remote: Login","Remote: Logout","Local: Login","Local: Logout"]:
						output_dict[counter] = v
						counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while carving logon info (carve_logon_info). The error message was {e}") 

def carve_hw_info(input_dict,rtype="ALL"):
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if rtype == "ALL":
				if input_dict[k]["Minor Type"] in ["Power On","HDD Detect","HDD Information","HDD Error","Time Sync.","S.M.A.R.T. Information","Local: Shutdown","Local: Abnormal Shutdown","System Running State","Remote: Initialize HDD","Local: Initialize HDD"]:
					output_dict[counter] = v
					counter += 1
			else:
				if input_dict[k]["Parsing Status"] == "Parsed" or v["Parsing Status"] == "Partially Parsed":
					if input_dict[k]["Minor Type"] in ["Power On","HDD Detect","HDD Information","HDD Error","Time Sync.","S.M.A.R.T. Information","Local: Shutdown","Local: Abnormal Shutdown","System Running State","Remote: Initialize HDD","Local: Initialize HDD"]:
						output_dict[counter] = v
						counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while carving hardware info (carve_hw_info). The error message was {e}") 

def carve_antiforensics_info(input_dict,rtype="ALL"):
	try:
		output_dict = {}
		counter = 1
		for k,v in input_dict.items():
			if rtype == "ALL":
				if input_dict[k]["Minor Type"] in ["Local: Configure Parameters","Remote: Configure Parameters","Remote: Initialize HDD","Local: Initialize HDD","Remote: Export Config File"]:
					output_dict[counter] = v
					counter += 1
			else:
				if input_dict[k]["Parsing Status"] == "Parsed" or v["Parsing Status"] == "Partially Parsed":
					if input_dict[k]["Minor Type"] in ["Local: Configure Parameters","Remote: Configure Parameters","Remote: Initialize HDD","Local: Initialize HDD","Remote: Export Config File"]:
						output_dict[counter] = v
						counter += 1
		return output_dict
	except Exception as e:
		hrf.mylogger(f"Error occured while carving antiforensics info (carve_antiforensics_info). The error message was {e}") 
