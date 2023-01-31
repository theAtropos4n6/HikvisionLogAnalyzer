#######################################################################################################
"""The following block of code holds all the methods used in parsing logs from text files"""
#######################################################################################################
import datetime
import os
import re
import scripts.parsing_utils as parutils
import scripts.html_report_files as hrf

#The txt logfile is ugly. Within the logfile multiple lines may refer to the same record. Therefore here I iterate through it and assing its entries to a list.
#All the potential extra lines that a record may have will hold their records' ID so as to be easier to distinguish
def log_to_list(opened_logfile):
	global number, header_counter
	number = 1
	new_log = []
	header_counter = 0
	for line in opened_logfile:
		try:
			if ("Time" and "Major Type" and "Minor Type" and "Details") in line and header_counter == 0:
					header = re.split(r'\s\s+', "Number of Record"+line.rstrip())
					new_log.append(header)
					header_counter +=1
			elif line.startswith(str(number),0,len(str(number))):
				new_log.append(re.split(r'\s\s+', line.rstrip()))
				number+=1
			else:
				extra_line = re.split(r'\s\s+', str(number-1)+"#,#"+line.rstrip())
				if len(extra_line) == 1:
					if extra_line[0].endswith("#,#"):
						pass#Empty line
					else:
						new_log.append(extra_line[0].split("#,#"))
				elif len(extra_line) > 1:
					merged_list = ' '.join(extra_line)
					new_log.append(merged_list.split("#,#"))
				else:
					hrf.mylogger("Input logfile was not recognised as a HikVision log file and therefore was not parsed. Check line: "+str(line))
		except Exception as e:
			hrf.mylogger(f"Error occured while parsing logfile (log_to_list method). Check entry: {str(line)}. The error message was {e}")
	return new_log

#Here I iterate through the list and create a dictionary which combines all available data for each (logfile) record into one key:value pair. 

def list_log_to_dict(list_log):
	new_dict = {}#"Number of Record": 0, "Values" : {"Time" : "", "Major Type" : "", "Minor Type": "", "Channel No." : "", "Local/Remote User" : "", "Remote Host IP": "", "Details" : []}}
	for item in range(1,len(list_log)): # 0 entry contains log headers
		try:
			# 1 # If list index holds date data then it should be the 1st line of corresponding log and therefore needs to be parsed.
			if list_log[item][1].startswith("202"): #Date format 2022-11-06 20:08:46 datetime.datetime.strptime(list_log[item][1], '%Y-%m-%d %H:%M:%S'): 
				current_log_record = list_log[item][0]
				#For each entry within the log a new dict is created and populated accordingly
				new_dict[current_log_record] = {	
				"Time": "", 
				"Major Type" : "", 
				"Minor Type": "", 
				"Channel No." : "", 
				"Local/Remote User" : "", 
				"Remote Host IP": "", 
				"Details" : []
				}
				new_dict[current_log_record]["Time"] = list_log[item][1]
				new_dict[current_log_record]["Major Type"] = list_log[item][2]

				# All entries have Major Type field. From then, the parsing differentiate based on minor type mapping. Hence, we use seperate parsers
				if list_log[item][2] == "Operation":
					parutils.parse_Operation(list_log[item],new_dict[current_log_record])
				elif list_log[item][2] == "Information":
					parutils.parse_Information(list_log[item],new_dict[current_log_record])
				elif list_log[item][2] == "Exception":
					parutils.parse_Exception(list_log[item],new_dict[current_log_record])
				elif list_log[item][2] == "Alarm":
					parutils.parse_Alarm(list_log[item],new_dict[current_log_record])
				else:
					hrf.mylogger("Unknown Major Type Found. Check Entry: "+str(item))
			# 1 # if list index doesn't hold date data then it contains the extra entries from previous log record
			elif not list_log[item][1].startswith("202"):
				new_dict[current_log_record]["Details"].append(list_log[item][1])
			# 1 # needs to be replaces with error catching
			else:
				hrf.mylogger("A new kind of Information popped up at entry: "+str(list_log[item]))
		except Exception as e:
			hrf.mylogger(f"Error occured while creating dictionary from parsed logfile (list_log_to_dict method). Check entry: {str(list_log[item])}. The error message was {e}")
	return new_dict

def parse_logfile(input_file): #returns dict_log
	try:	
		with open(input_file,'r',encoding='utf-8') as logfile:
			list_log = log_to_list(logfile)
			dict_log = list_log_to_dict(list_log)
		return dict_log
	except Exception as e:
		hrf.mylogger(f"Error occured while reading logfile. The error message was {e}")

def parse_logfile_dir(input_file_dir): #returns dict_log
	ext = ('.txt')
	dir_dict = {}
	for file in os.listdir(input_file_dir):
		if file.endswith(ext):
			try:	
				with open(input_file_dir+"\\"+file,'r',encoding='utf-8') as logfile:
					list_log = log_to_list(logfile)
					dict_log = list_log_to_dict(list_log)
					dir_dict[file] = dict_log
			except Exception as e:
				hrf.mylogger(f"Error occured while reading logfiles directory. The error message was {e}")
	return dir_dict

