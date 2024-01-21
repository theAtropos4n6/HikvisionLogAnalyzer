import time
import os
import scripts.html_report_files as hrf
#cur_time = time.time()
#cur_time_in_ms = int(cur_time*1000)
cur_time = time.strftime("%Y-%m-%d_%H-%M-%S")

def html_report_parsed(dict_log,report_path,log_filename,time_zone_opt,rtype="Generic"):
	# if rtype == "Generic":
	# 	prefix = ""
	# else:
	prefix = rtype
	filename = os.path.basename(log_filename)
	report_dir = f'{report_path}\\Reports_{cur_time}\\HTML\\Report_Files'
	if not os.path.exists(report_dir):
		os.makedirs(report_dir)
	if time_zone_opt == "DVR-Selected Time Zone":
		time_zone = "Time (DVR-Selected Time Zone)"
	else:
		time_zone = "Time (DVR-Selected Time Zone)"
	try:
		#Here the HTML report is being created
		with open(f'{report_dir}\\Report_{prefix}_{filename}.html',"w", encoding="utf-8") as html_file:
			html_output = ""
			html_output += f'\n<!DOCTYPE html>'
			html_output += f'\n<html lang="en">'
			html_output += f'\n<head>'
			html_output += f'\n<meta charset="utf-8">'
			html_output += f'\n<title>{prefix}</title>'
			html_output += f'\n<link rel="icon" type="image/x-icon" href="icons/myfavicon.ico">'
			html_output += f'\n<link rel="stylesheet" href="style.css">'
			html_output += f'\n</head>'
			html_output += f'<p> Logfile: {log_filename}</p>'
			html_output += f'<p> There are currently {len(dict_log)} records within the log provided.</p>'
			html_output += '\n<table border = "1" width=100%>'
			html_output += '\n<thead>'
			html_output += f'\n<nav>'
			html_output += f'\n<a href="../index.html">Home Page</a>'
			html_output += f'\n</nav>'	
			html_output += '\n<tr>'
			html_output += '\n<th>Number of Record</th>'
			html_output += f'\n<th style="width:10%">{time_zone}</th>'
			html_output += '\n<th>Major Type</th>'
			html_output += '\n<th style="width:15%">Minor Type</th>'
			html_output += '\n<th>Channel No.</th>'
			html_output += '\n<th>Local/Remote User</th>'
			html_output += '\n<th>Remote Host IP</th>'
			html_output += '\n<th style="width:75%">Details</th>'
			html_output += '\n</tr>'
			html_output += "\n</thead>"
			html_output += '\n<tbody>'
			for k,v in dict_log.items():
				if prefix in ["Generic","Hardware","Antiforensics"]:
					html_output += '<tr>'
					html_output += f'<td>{k}</td>'
					html_output += f'<td>{v["Time"]}</td>'
					html_output += f'<td>{v["Major Type"]}</td>'
					html_output += f'<td>{v["Minor Type"]}</td>'
					html_output += f'<td>{v["Channel No."]}</td>'
					html_output += f'<td>{v["Local/Remote User"]}</td>'
					html_output += f'<td>{v["Remote Host IP"]}</td>'
					html_output += '<td>'
					#all this trouble just to remove the trailing comma 
					html_detail_output = ""
					for item in v["Details"]:
						html_detail_output += f'{item}, '
					details_data = html_detail_output.rstrip(", ")
					html_output += details_data
					html_output += '</td>'
					html_output += '\n</tr>'
				elif prefix == "Logon":
					html_output += set_tr_class(v["Minor Type"])
					html_output += f'<td>{k}</td>'
					html_output += f'<td>{v["Time"]}</td>'
					html_output += f'<td>{v["Major Type"]}</td>'
					html_output += f'<td>{v["Minor Type"]}</td>'
					html_output += f'<td>{v["Channel No."]}</td>'
					html_output += f'<td>{v["Local/Remote User"]}</td>'
					html_output += f'<td>{v["Remote Host IP"]}</td>'
					html_output += '<td>'
					#all this trouble just to remove the trailing comma 
					html_detail_output = ""
					for item in v["Details"]:
						html_detail_output += f'{item}, '
					details_data = html_detail_output.rstrip(", ")
					html_output += details_data
					html_output += '</td>'
					html_output += '\n</tr>'	
			html_output += "\n</tbody>"
			html_output += '\n</table>'
			html_output += f'\n<nav>'
			html_output += f'\n<a href="../index.html">Home Page</a>'
			html_output += f'\n</nav>'
			html_file.write(html_output)
	except Exception as e:
		hrf.mylogger(f"Error while creating html report file. The error message was {e}")


def html_report_carved(img_filename,report_path,carved_results,splitn=2000,rtype="Generic"): 
	prefix = rtype
	dict_len = len(carved_results)
	num_input = int(splitn)
	split_input = num_input if not num_input == 2000 else 2000
	if num_input == 0:
		page_number = 1
	elif int(dict_len%num_input) == 0:
		page_number = int(dict_len/num_input)
	else:
		page_number = int(dict_len/num_input)+1
	filename = os.path.basename(img_filename)
	report_dir = f'{report_path}\\Reports_{cur_time}\\HTML\\Report_files'
	if not os.path.exists(report_dir):
		os.makedirs(report_dir)
	time_zone = "Time (UTC)"
	try:
		counter = 0
		key_holder = 0
		#heading = ""
		for i in range(1,page_number+1):
			with open(f'{report_dir}\\Report_{prefix}_{filename}_{i}.html',"w", encoding="utf-8") as html_file:
				html_output = ""
				html_output += f'\n<!DOCTYPE html>'
				html_output += f'\n<html lang="en">'
				html_output += f'\n<head>'
				html_output += f'\n<meta charset="utf-8">'
				html_output += f'<meta name="viewport" content="width=device-width">'
				html_output += f'\n<title>{prefix}</title>'
				html_output += f'\n<link rel="icon" type="image/x-icon" href="icons/myfavicon.ico">'
				html_output += f'\n<link rel="stylesheet" href="style.css">'
				html_output += f'\n</head>'
				html_output += f'<p> Image file: {img_filename}</p>'
				heading = f'<p> There are currently {len(carved_results)} records within the image file provided.</p>' if rtype == "Generic" else f'<p> There are currently {len(carved_results)} records exported from the image file provided.</p>'
				html_output += heading
				html_output += f'\n<nav>'
				html_output += f'\n<a href="../index.html">Home Page</a>'
				for j in range(1,page_number+1):
					html_output += f'\n<a href="Report_{prefix}_{filename}_{j}.html">{j}</a>'
				html_output += f'\n</nav>'
				html_output += '\n<table border = "1" width=100%>'
				html_output += '\n<thead>'
				html_output += '\n<tr>'
				html_output += '\n<th>Number of Log Record</th>'
				html_output += f'\n<th style="width:10%">{time_zone}</th>'
				html_output += '\n<th>Major Type</th>'
				html_output += '\n<th style="width:15%">Minor Type</th>'
				html_output += '\n<th>Channel No.</th>'
				html_output += '\n<th>Local/Remote User</th>'
				html_output += '\n<th>Remote Host IP</th>'
				html_output += '\n<th style="width:70%">Details</th>'
				html_output += '\n<th style="width:15%">Parsing Status</th>'
				html_output += '\n<th style="width:15%">Entry Offset</th>'
				html_output += '\n</tr>'
				html_output += "\n</thead>"
				html_output += '\n<tbody>'
				for k,v in carved_results.items():
					if int(k) >= key_holder:
						if not split_input == 0 and counter <= split_input: #if input_dict[k]["Minor Type"] in ["Illegal Login","Remote: Login","Remote: Logout","Local: Login","Local: Logout"]:
							html_output += set_tr_class(v["Minor Type"]) if prefix =="Logon" else f'<tr>'
							#html_output += '<tr>'
							html_output += f'<td>{k}</td>'
							html_output += f'<td>{v["Time"]}</td>'
							html_output += f'<td>{v["Major Type"]}</td>'
							html_output += f'<td>{v["Minor Type"]}</td>'
							html_output += f'<td>{v["Channel No."]}</td>'
							html_output += f'<td>{v["Local/Remote User"]}</td>'
							html_output += f'<td>{v["Remote Host IP"]}</td>'
							html_output += f'<td>{v["Details"]}</td>'
							html_output += f'<td>{v["Parsing Status"]}</td>'
							html_output += f'<td>{v["Entry Offset"]}</td>'
							counter += 1 #iterate as long as the split_input and then exits loop
						elif split_input == 0:
							html_output += set_tr_class(v["Minor Type"]) if prefix =="Logon" else f'<tr>'
							html_output += f'<td>{k}</td>'
							html_output += f'<td>{v["Time"]}</td>'
							html_output += f'<td>{v["Major Type"]}</td>'
							html_output += f'<td>{v["Minor Type"]}</td>'
							html_output += f'<td>{v["Channel No."]}</td>'
							html_output += f'<td>{v["Local/Remote User"]}</td>'
							html_output += f'<td>{v["Remote Host IP"]}</td>'
							html_output += f'<td>{v["Details"]}</td>'
							html_output += f'<td>{v["Parsing Status"]}</td>'
							html_output += f'<td>{v["Entry Offset"]}</td>'
				key_holder += counter
				html_output += "\n</tbody>"
				html_output += '\n</table>'
				html_output += f'\n<nav>'
				html_output += f'\n<a href="../index.html">Home Page</a>'
				for j in range(1,page_number+1):
					html_output += f'\n<a href="Report_{prefix}_{filename}_{j}.html">{j}</a>'
				html_output += f'\n</nav>'
				html_file.write(html_output)
			counter = 0
	except Exception as e:
		hrf.mylogger(f"Error while creating html report file (ALL LOGFILE ENTRIES). The error message was {e}")


def html_report_carved_fsinfo(img_filename,report_path,carved_results):
	filename = os.path.basename(img_filename)
	report_dir = f'{report_path}\\Reports_{cur_time}\\HTML\\Report_files'
	if not os.path.exists(report_dir):
		os.makedirs(report_dir)
	try:
		with open(f'{report_dir}\\Report_FS_Info_{filename}.html',"w", encoding="utf-8") as html_file:
			html_output = ""
			html_output += f'\n<head>'
			html_output += f'\n<meta charset="utf-8">'
			html_output += f'\n<title>File System Information</title>'
			html_output += f'\n<link rel="icon" type="image/x-icon" href="icons/myfavicon.ico">'
			html_output += f'\n<link rel="stylesheet" href="style.css">'
			html_output += f'<p> Image file: {img_filename}</p>'
			html_output += '\n<table border = "1" width=100%>'
			html_output += '\n<thead>'
			html_output += f'\n<nav>'
			html_output += f'\n<a href="../index.html">Home Page</a>'
			html_output += f'\n</nav>'	
			html_output += '\n<tr>'
			html_output += '\n<th>Type of Information</th>' 
			html_output += '\n<th>Details</th>'
			html_output += '\n</tr>'
			html_output += "\n</thead>"
			html_output += '\n<tbody>'
			html_output += '<tr>'
			html_output += f'<td>Filesystem Signature:</td>'
			html_output += f'<td>{str(carved_results[-1])}</td>'
			html_output += '</tr>'
			html_output += '<tr>'
			html_output += f'<td>Filesystem Initialization Time (UTC):</td>'
			html_output += f'<td>{str(carved_results[-2])}</td>'
			html_output += '</tr>'			
			html_output += '<tr>'
			html_output += f'<td>Disk size is (in MB):</td>'
			html_output += f'<td>{str(carved_results[2])}</td>'
			html_output += '</tr>'			
			html_output += '<tr>'
			html_output += f'<td>Logfiles beginning offset:</td>'
			html_output += f'<td>{str(carved_results[0])}</td>'
			html_output += '</tr>'			
			html_output += '<tr>'
			html_output += f'<td>Logfiles size in bytes:</td>'
			html_output += f'<td>{str(carved_results[-3])}</td>'
			html_output += '</tr>'				
			html_output += "\n</tbody>"
			html_output += '\n</table>'
			html_file.write(html_output)
	except Exception as e:
		hrf.mylogger(f"Error while creating html report file. The error message was {e}")


def set_tr_class(cur_entry):
	html_output = ""
	if cur_entry in ["Local: Login","Remote: Login"]:
		html_output += f'<tr class="login">' 
	elif cur_entry in ["Local: Logout","Remote: Logout"]:
		html_output += f'<tr class="logout">'
	elif cur_entry == "Illegal Login":
		html_output += f'<tr class="illegal_login">'
	return html_output