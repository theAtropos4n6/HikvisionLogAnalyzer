import csv
import os
import time 
import scripts.html_report_files as hrf
cur_time = time.strftime("%Y-%m-%d_%H-%M-%S")

def csv_report_for_parsed(file,output_file_dir,carved_results,rtype="Generic"):
	#Here the Report Folder is being created
	if rtype == "Generic":
		prefix = ""
	else:
		prefix = rtype
	filename = os.path.basename(file)
	report_filedir = f'{output_file_dir}\\Reports_{cur_time}\\CSV'
	if not os.path.exists(report_filedir):
		os.makedirs(report_filedir)
	try:
		#Here the CSV report is being created
		with open(f'{report_filedir}\\Report_{prefix}_{filename}.csv',"w",newline="", encoding="utf-8") as csv_file:
			writer = csv.writer(csv_file,delimiter=';')
			top_cell = "LogFile: ;"+file+"\n"
			csv_file.write(top_cell)
			csv_header = ["Number of Record","Time (DVR-Selected Time Zone)","Major Type","Minor Type","Channel No.","Local/Remote User","Remote Host IP","Details"]
			writer.writerow(csv_header)
			for k,v in carved_results.items():
				csv_detail_records = ""
				csv_detail_output = ""
				for i in v["Details"]:
					csv_detail_records += f'{i}, '
				details_data = csv_detail_records.rstrip(", ")
				csv_detail_output += details_data
				fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],csv_detail_output]
				writer.writerow(fieldnames)
	except Exception as e:
		hrf.mylogger(f"Error while creating csv report file. The error message was {e}")

def csv_report_for_carved_all(file,output_file_dir,carved_results):
	filename = os.path.basename(file)
	report_filedir = f'{output_file_dir}\\Reports_{cur_time}\\CSV'
	if not os.path.exists(report_filedir):
		os.makedirs(report_filedir)
	try:
		with open(f'{report_filedir}\\Report_{filename}.csv',"w",newline="", encoding="utf-8") as csv_file: ##<---fix path/file
			writer = csv.writer(csv_file,delimiter=';')
			top_cell = "Image File: ;"+file+"\n"
			csv_file.write(top_cell)
			csv_header = ["Number of Record","Time (UTC+00:00)","Major Type","Minor Type","Channel No.","Local/Remote User","Remote Host IP","Details","Parsing Status","Entry Offset"]
			writer.writerow(csv_header)
			for k,v in carved_results.items():
				item = v.split("#;#")
				fieldnames = [k,item[0][:-6],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]] #item[0][:-6] -6 removes the slice "+00:00" from the datetime
				writer.writerow(fieldnames)
	except Exception as e:
		hrf.mylogger(f"Error while creating csv report file. The error message was {e}")

def csv_report_for_carved_supported(file,output_file_dir,carved_results):
	filename = os.path.basename(file)
	report_filedir = f'{output_file_dir}\\Reports_{cur_time}\\CSV'
	if not os.path.exists(report_filedir):
		os.makedirs(report_filedir)
	try:
		with open(f'{report_filedir}\\Report_{filename}.csv',"w",newline="", encoding="utf-8") as csv_file: ##<---fix path/file
			writer = csv.writer(csv_file,delimiter=';')
			top_cell = "Image File: ;"+file+"\n"
			csv_file.write(top_cell)
			csv_header = ["Number of Record","Time (UTC+00:00)","Major Type","Minor Type","Channel No.","Local/Remote User","Remote Host IP","Details","Parsing Status","Entry Offset"]
			writer.writerow(csv_header)
			for k,v in carved_results.items():
				item = v.split("#;#")
				if item[7] == "Parsed" or item[7] == "Partially Parsed":
					fieldnames = [k,item[0][:-6],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]] #item[0][:-6] -6 removes the slice "+00:00" from the datetime
					writer.writerow(fieldnames)
	except Exception as e:
		hrf.mylogger(f"Error while creating csv report file. The error message was {e}")

#[log_start_offset, size_of_system_logs_le,int(disk_size_in_mb),int(size_of_system_logs_in_b),init_time,fs_sig]
def csv_report_fs_info(file,output_file_dir,carved_results):
	filename = os.path.basename(file)
	report_filedir = f'{output_file_dir}\\Reports_{cur_time}\\CSV'
	if not os.path.exists(report_filedir):
		os.makedirs(report_filedir)
	try:
		with open(f'{report_filedir}\\Report_FS_Info_{filename}.csv',"w",newline="", encoding="utf-8") as csv_file: ##<---fix path/file
			writer = csv.writer(csv_file,delimiter=';')
			top_cell = f"Image File: ; {file} \n"
			csv_file.write(top_cell)
			csv_header = ["Type of Information","Details"]
			writer.writerow(csv_header)
			writer.writerow(["Filesystem Signature:",str(carved_results[-1])])
			writer.writerow(["Filesystem Initialization Time (UTC):",str(carved_results[-2])])
			writer.writerow(["Disk size is (in MB):",str(carved_results[2])])
			writer.writerow(["Logfiles beginning offset:",str(carved_results[0])])
			writer.writerow(["Logfiles size in bytes:",str(carved_results[-3])])
	except Exception as e:
			hrf.mylogger(f"Error while creating csv report file. The error message was {e}")

def csv_report_for_carved_intel_all(file,output_file_dir,carved_results,rtype="Generic"):
	#Here the Report Folder is being created
	if rtype == "Generic":
		prefix = ""
	else:
		prefix = rtype
	filename = os.path.basename(file)
	report_filedir = f'{output_file_dir}\\Reports_{cur_time}\\CSV'
	if not os.path.exists(report_filedir):
		os.makedirs(report_filedir)
	try:
		#Here the CSV report is being created
		with open(f'{report_filedir}\\Report_{prefix}_{filename}.csv',"w",newline="", encoding="utf-8") as csv_file:
			writer = csv.writer(csv_file,delimiter=';')
			top_cell = "Image File: ;"+file+"\n"
			csv_file.write(top_cell)
			csv_header = ["Number of Record","Time (DVR-Selected Time Zone)","Major Type","Minor Type","Channel No.","Local/Remote User","Remote Host IP","Details","Parsing Status","Entry Offset"]
			writer.writerow(csv_header)
			for k,v in carved_results.items():
				# csv_detail_records = ""
				# csv_detail_output = ""
				# for i in v["Details"]:
				# 	csv_detail_records += f'{i}, '
				# details_data = csv_detail_records.rstrip(", ")
				# csv_detail_output += details_data
				if rtype == "Logon":
					if carved_results[k]["Minor Type"] in ["Illegal Login","Remote: Login","Remote: Logout","Local: Login","Local: Logout"]:
						fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],v["Details"],v["Parsing Status"],v["Entry Offset"]]
				elif rtype == "Hardware":
					if carved_results[k]["Minor Type"] in ["Power On","HDD Detect","HDD Information","HDD Error","Time Sync.","S.M.A.R.T. Information","Local: Shutdown","Local: Abnormal Shutdown","System Running State","Remote: Initialize HDD"]:
						fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],v["Details"],v["Parsing Status"],v["Entry Offset"]]
				elif rtype == "Antiforensics":
					if carved_results[k]["Minor Type"] in ["Local: Configure Parameters","Remote: Configure Parameters","Remote: Alarm Disarming","Remote: Initialize HDD","Remote: Export Config File","Stop Record"]:
						fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],v["Details"],v["Parsing Status"],v["Entry Offset"]]
				writer.writerow(fieldnames)
	except Exception as e:
		hrf.mylogger(f"Error while creating csv report file. The error message was {e}")

def csv_report_for_carved_intel_supported(file,output_file_dir,carved_results,rtype="Generic"):
	#Here the Report Folder is being created
	if rtype == "Generic":
		prefix = ""
	else:
		prefix = rtype
	filename = os.path.basename(file)
	report_filedir = f'{output_file_dir}\\Reports_{cur_time}\\CSV'
	if not os.path.exists(report_filedir):
		os.makedirs(report_filedir)
	try:
		#Here the CSV report is being created
		with open(f'{report_filedir}\\Report_{prefix}_{filename}.csv',"w",newline="", encoding="utf-8") as csv_file:
			writer = csv.writer(csv_file,delimiter=';')
			top_cell = "Image File: ;"+file+"\n"
			csv_file.write(top_cell)
			csv_header = ["Number of Record","Time (DVR-Selected Time Zone)","Major Type","Minor Type","Channel No.","Local/Remote User","Remote Host IP","Details","Parsing Status","Entry Offset"]
			writer.writerow(csv_header)
			for k,v in carved_results.items():
				# csv_detail_records = ""
				# csv_detail_output = ""
				# for i in v["Details"]:
				# 	csv_detail_records += f'{i}, '
				# details_data = csv_detail_records.rstrip(", ")
				# csv_detail_output += details_data
				if carved_results[k]["Parsing Status"] == "Parsed" or carved_results[k]["Parsing Status"] == "Partially Parsed":
					if rtype == "Logon":
						if carved_results[k]["Minor Type"] in ["Illegal Login","Remote: Login","Remote: Logout","Local: Login","Local: Logout"]:
							fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],v["Details"],v["Parsing Status"],v["Entry Offset"]]
					elif rtype == "Hardware":
						if carved_results[k]["Minor Type"] in ["Power On","HDD Detect","HDD Information","HDD Error","Time Sync.","S.M.A.R.T. Information","Local: Shutdown","Local: Abnormal Shutdown","System Running State","Remote: Initialize HDD"]:
							fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],v["Details"],v["Parsing Status"],v["Entry Offset"]]
					elif rtype == "Antiforensics":
						if input_dict[k]["Minor Type"] in ["Local: Configure Parameters","Remote: Configure Parameters","Remote: Alarm Disarming","Remote: Initialize HDD","Remote: Export Config File","Stop Record"]:
							fieldnames = [k,v["Time"],v["Major Type"],v["Minor Type"],v["Channel No."],v["Local/Remote User"],v["Remote Host IP"],v["Details"],v["Parsing Status"],v["Entry Offset"]]
				writer.writerow(fieldnames)
	except Exception as e:
		hrf.mylogger(f"Error while creating csv report file. The error message was {e}")