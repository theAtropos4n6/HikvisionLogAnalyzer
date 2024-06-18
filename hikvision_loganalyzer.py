import PySimpleGUI as sg 
import time
import os
import base64
from pathlib import Path
import scripts.parsing_logfile as parlog
import scripts.carving_utils as carlog
import scripts.csv_reporting as scsv
import scripts.html_reporting as hr
import scripts.html_report_files as hrf
import scripts.intel_methods as im

#System time is used for logging purposes
cur_time = time.time()
cur_time_in_ms = int(cur_time*1000)
validation_status = []
version = "1.1.1" #=> parser_last_update = "2024-06-18"

#######################################################################################################
#                                """atropos icon BEGIN"""
#######################################################################################################
myfavicon = hrf.get_icon()
#######################################################################################################
#                                """atropos icon FINISH"""
#######################################################################################################
#######################################################################################################
#                                """USER Parsing function BEGIN"""
#######################################################################################################

#This method is the most important in this file. It takes the user GUI inputs and sends the commands to the rest of the parsers/carvers etc.
def parse_user_input(values,input_choice):
	hrf.mylogger(f"------------------------------------------------------------------------------------\n")
	hrf.mylogger(f'{cur_time}=>Evaluating user input:\n')
	filename = os.path.basename(values['-INPUT-F-'])
	window['-PROGRESS-BAR-'].UpdateBar(55,100)
	if input_choice == "Folder": 
		hrf.mylogger(f'{cur_time}=>User chose folder as an input\n')
		hrf.mylogger(f'{cur_time}=>Begin parsing folder items\n')
		dir_dicto = parlog.parse_logfile_dir(values['-INPUT-F-'])
		hrf.mylogger(f'{cur_time}=>Finished parsing folder items\n')
		if values['-LCSVRESULTS-'] == True:
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting CSV results for parsed folder items\n')
			time_zone = "DVR-Selected Time Zone"
			for k,v in dir_dicto.items():
				scsv.csv_report_for_parsed(values['-INPUT-F-']+'/'+k,values['-OUTPUT-FOLDER-'],v)
				if values['-LLOGONINFO-'] == True:
					logon_info = im.parse_logon_info(v)
					scsv.csv_report_for_parsed(values['-INPUT-F-']+'/'+k,values['-OUTPUT-FOLDER-'],logon_info,"Logon")
				if values['-LHWINFO-'] == True: 
					parse_hw_info = im.parse_hw_info(v)
					scsv.csv_report_for_parsed(values['-INPUT-F-']+'/'+k,values['-OUTPUT-FOLDER-'],parse_hw_info,"Hardware")
				if values['-LANTIFORENSICS-'] == True: 
					antif_info = im.parse_antiforensics_info(v)
					scsv.csv_report_for_parsed(values['-INPUT-F-']+'/'+k,values['-OUTPUT-FOLDER-'],antif_info,"Antiforensics")
			hrf.mylogger(f'{cur_time}=>Finished reporting CSV results for parsed folder items\n')
		if values['-LHTMLRECORDS-'] == True:
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting HTML results for parsed folder items\n')
			time_zone = "DVR-Selected Time Zone"
			options = ["folder",values['-LHWINFO-'],values['-LLOGONINFO-'],values['-LANTIFORENSICS-']]
			for k,v in dir_dicto.items():
				hr.html_report_parsed(v,values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone)
				if values['-LLOGONINFO-'] == True:
					logon_info = im.parse_logon_info(v)
					hr.html_report_parsed(logon_info,values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"Logon")
					hrf.create_report_folder_results(values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],dir_dicto,"Logon")
				if values['-LHWINFO-'] == True:
					parse_hw_info = im.parse_hw_info(v)
					hr.html_report_parsed(parse_hw_info,values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"Hardware")
					hrf.create_report_folder_results(values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],dir_dicto,"Hardware")
				if values['-LANTIFORENSICS-'] == True:
					antif_info = im.parse_antiforensics_info(v)
					hr.html_report_parsed(antif_info,values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"Antiforensics")
					hrf.create_report_folder_results(values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],dir_dicto,"Antiforensics")
			hrf.create_report_icons(values['-OUTPUT-FOLDER-'])
			hrf.create_report_stand_html(values['-OUTPUT-FOLDER-'])
			hrf.create_report_folder_results(values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],dir_dicto)
			hrf.create_report_index(values['-OUTPUT-FOLDER-'],version,options)
			hrf.mylogger(f'{cur_time}=>Finished reporting HTML results for parsed folder items\n')
	elif input_choice.endswith("txt"):
		hrf.mylogger(f'{cur_time}=>User chose logfile as an input\n')
		hrf.mylogger(f'{cur_time}=>Begin parsing logfile\n')
		dict_log = parlog.parse_logfile(values['-INPUT-F-'])
		hrf.mylogger(f'{cur_time}=>Finished parsing logfile\n')
		if values['-LLOGONINFO-'] == True:
			logon_info = im.parse_logon_info(dict_log)
		if values['-LHWINFO-'] == True: 
			parse_hw_info = im.parse_hw_info(dict_log)
		if values['-LANTIFORENSICS-'] == True: 
			antif_info = im.parse_antiforensics_info(dict_log)
		if values['-LCSVRESULTS-'] == True:
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting CSV results for parsed logfile\n')
			scsv.csv_report_for_parsed(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],dict_log)
			if values['-LLOGONINFO-'] == True:
				scsv.csv_report_for_parsed(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],logon_info,"Logon")
			if values['-LHWINFO-'] == True: 
				scsv.csv_report_for_parsed(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],parse_hw_info,"Hardware")
			if values['-LANTIFORENSICS-'] == True:
				scsv.csv_report_for_parsed(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],antif_info,"Antiforensics") 
			hrf.mylogger(f'{cur_time}=>Finished reporting CSV results for parsed logfile\n')
		if values['-LHTMLRECORDS-'] == True:
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting HTML results for parsed logfile\n')
			#filename = os.path.basename(values['-INPUT-F-'])
			options = ["log",values['-LHWINFO-'],values['-LLOGONINFO-'],values['-LANTIFORENSICS-'],filename]
			time_zone = "DVR-Selected Time Zone"
			# scsv.csv_report_for_parsed(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],dict_log)
			hr.html_report_parsed(dict_log,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone)
			if values['-LLOGONINFO-'] == True:
				hr.html_report_parsed(logon_info,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"Logon")
			if values['-LHWINFO-'] == True:
				hr.html_report_parsed(parse_hw_info,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"Hardware")
			if values['-LANTIFORENSICS-'] == True:
				hr.html_report_parsed(antif_info,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"Antiforensics")
			hrf.create_report_icons(values['-OUTPUT-FOLDER-'])
			hrf.create_report_stand_html(values['-OUTPUT-FOLDER-'])
			hrf.create_report_index(values['-OUTPUT-FOLDER-'],version,options)
			hrf.mylogger(f'{cur_time}=>Finished reporting HTML results for parsed logfile\n')
	else:
		hrf.mylogger(f'{cur_time}=>User chose image file as an input\n')
		hrf.mylogger(f'{cur_time}=>Begin parsing image file\n')
		carved_results = carlog.carved_logfiles(values['-INPUT-F-'])
		dict_carved_log = im.retrieve_carved_dict(carved_results[0])
		hrf.mylogger(f'{cur_time}=>Finished parsing image file')
		if values['-ICSVRESULTS-'] == True and values['-RECORDSCARVING-'] == True:	#CSV All available logs
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting CSV results for parsed image file (ALL LOGFILE ENTRIES)\n')
			scsv.csv_report_for_carved_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],carved_results[0])
			#scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],dict_log)
			if values['-IFSINFO-'] == True:
				scsv.csv_report_fs_info(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],carved_results[1])	
			if values['-IHWINFO-'] == True:
				parse_hw_info = im.carve_hw_info(dict_carved_log)
				scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],parse_hw_info,"Hardware")
			if values['-ILOGONINFO-'] == True:
				logon_info = im.carve_logon_info(dict_carved_log)
				scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],logon_info,"Logon")
			if values['-IANTIFORENSICS-'] == True:
				antif_info = im.carve_antiforensics_info(dict_carved_log)
				scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],antif_info,"Antiforensics")
			hrf.mylogger(f'{cur_time}=>Finished reporting CSV results for parsed image file\n')
		elif values['-ICSVRESULTS-'] == True and values['-RECORDSCARVING-'] == False: #CSV Only Supported  logs
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting CSV results for parsed image file (SUPPORTED LOGFILE ENTRIES)\n')
			scsv.csv_report_for_carved_supported(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],carved_results[0])
			#scsv.csv_report_for_carved_intel_supported(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],dict_log)
			if values['-IFSINFO-'] == True:
				scsv.csv_report_fs_info(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],carved_results[1])
			if values['-IHWINFO-'] == True:
				parse_hw_info = im.carve_hw_info(dict_carved_log,"Supported")
				scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],parse_hw_info,"Hardware")
			if values['-ILOGONINFO-'] == True:
				logon_info = im.carve_logon_info(dict_carved_log,"Supported")
				scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],logon_info,"Logon")
			if values['-IANTIFORENSICS-'] == True:
				antif_info = im.carve_antiforensics_info(dict_carved_log,"Supported")
				scsv.csv_report_for_carved_intel_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],antif_info,"Antiforensics")
		if values['-IHTMLRECORDS-'] == True and values['-RECORDSCARVING-'] == True:	 #HTML All available logs
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting HTML results for parsed image file (ALL LOGFILE ENTRIES)\n')
			options = ["image",values['-IFSINFO-'],values['-IHWINFO-'],values['-ILOGONINFO-'],values['-IANTIFORENSICS-'],filename]
			#hr.html_report_carved_all(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],dict_log,values['-SPLITRECORDS-'])
			hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],dict_carved_log,values['-SPLITRECORDS-'])
			if values['-IFSINFO-'] == True:
				hr.html_report_carved_fsinfo(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],carved_results[1])
			if values['-IHWINFO-'] == True:
				parse_hw_info = im.carve_hw_info(dict_carved_log)
				hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],parse_hw_info,values['-SPLITRECORDS-'],"Hardware")
			if values['-ILOGONINFO-'] == True:
				logon_info = im.carve_logon_info(dict_carved_log)
				hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],logon_info,values['-SPLITRECORDS-'],"Logon")
			if values['-IANTIFORENSICS-'] == True:
				antif_info = im.carve_antiforensics_info(dict_carved_log)
				hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],antif_info,values['-SPLITRECORDS-'],"Antiforensics")
			hrf.create_report_icons(values['-OUTPUT-FOLDER-'])
			hrf.create_report_stand_html(values['-OUTPUT-FOLDER-'])
			hrf.create_report_index(values['-OUTPUT-FOLDER-'],version,options)
			hrf.mylogger(f'{cur_time}=>Finished reporting HTML results for parsed image file (ALL LOGFILE ENTRIES)\n')	
		elif values['-IHTMLRECORDS-'] == True and values['-RECORDSCARVING-'] == False:	#HTML Only Supported  logs
			hrf.mylogger(f"------------------------------------------------------------------------------------\n")
			hrf.mylogger(f'{cur_time}=>Begin reporting HTML results for image file (SUPPORTED LOGFILE ENTRIES)\n')
			options = ["image",values['-IFSINFO-'],values['-IHWINFO-'],values['-ILOGONINFO-'],values['-IANTIFORENSICS-'],filename]
			supp_dict = im.retrieve_carved_dict_supported(dict_carved_log)
			hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],supp_dict,values['-SPLITRECORDS-'])
			if values['-IFSINFO-'] == True:
				hr.html_report_carved_fsinfo(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],carved_results[1])
			if values['-IHWINFO-'] == True:
				parse_hw_info = im.carve_hw_info(dict_carved_log,"Supported")
				hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],parse_hw_info,values['-SPLITRECORDS-'],"Hardware")
			if values['-ILOGONINFO-'] == True:
				logon_info = im.carve_logon_info(dict_carved_log,"Supported")
				hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],logon_info,values['-SPLITRECORDS-'],"Logon")
			if values['-IANTIFORENSICS-'] == True:
				antif_info = im.carve_antiforensics_info(dict_carved_log,"Supported")
				hr.html_report_carved(values['-INPUT-F-'],values['-OUTPUT-FOLDER-'],antif_info,values['-SPLITRECORDS-'],"Antiforensics")
			hrf.create_report_icons(values['-OUTPUT-FOLDER-'])
			hrf.create_report_stand_html(values['-OUTPUT-FOLDER-'])
			hrf.create_report_index(values['-OUTPUT-FOLDER-'],version,options)
			hrf.mylogger(f'{cur_time}=>Finished reporting HTML results for parsed image file\n')
	window['-PROGRESS-BAR-'].UpdateBar(80,100)
#######################################################################################################
#									"""USER Parsing function FINISH"""
#######################################################################################################
#######################################################################################################
#									"""GUI Code section BEGIN"""
#######################################################################################################
def make_window(version):
	sg.theme('Reddit')
	logging_output= []
	right_click_menu_def = [[],['About']]


	input_files_frame = [[sg.Input(s=(87,2),key='-INPUT-F-'), sg.FileBrowse(button_text='File Browser'),sg.FolderBrowse(button_text='Folder Browser',target = (sg.ThisRow,-2))]]

	output_files_frame = [[sg.Input(s=(100,2),key='-OUTPUT-FOLDER-'),sg.FolderBrowse('Folder Browser')]]

	image_options_frame_inner = [
							[sg.Radio('Carve all available logs',"RadioButton", default=True, k='-RECORDSCARVING-')],
							[sg.Radio('Carve only currently supported logs',"RadioButton", default=True, k='-RECORDSCARVING-')],
							[sg.Checkbox('Parse File System information', default=True, k='-IFSINFO-')],
							[sg.Checkbox('Parse Hardware information', default=True, k='-IHWINFO-')],
							[sg.Checkbox('Parse Login/Logout information', default=True, k='-ILOGONINFO-')],
							[sg.Checkbox('Parse potential anti-forensics information', default=True, k='-IANTIFORENSICS-')],
							[sg.Checkbox('Export results in CSV format', default=False, k='-ICSVRESULTS-')],
							[sg.Checkbox('Export results in HTML format', default=True, k='-IHTMLRECORDS-')],
							[sg.Text('Split .html files every'),sg.Input(default_text=2000,key='-SPLITRECORDS-',s=10),sg.Text('records')]]

	image_options_frame_outer = [[sg.Frame('Image file:',image_options_frame_inner,font='Any 10 bold')]]

	logs_options_frame_inner = [
							[sg.Checkbox('Parse Hardware information', default=True, k='-LHWINFO-')],
							[sg.Checkbox('Parse Login/Logout information', default=True, k='-LLOGONINFO-')],
							[sg.Checkbox('Parse potential anti-forensics information', default=True, k='-LANTIFORENSICS-')],
							[sg.Checkbox('Export results in CSV format', default=False, k='-LCSVRESULTS-')],
							[sg.Checkbox('Export results in HTML format', default=True, k='-LHTMLRECORDS-')],
							]

	logs_options_frame_outer = [[sg.Frame('Log file(s):',logs_options_frame_inner,font='Any 10 bold')]]

	capabilities_frame = [sg.Frame('Capabilities:',image_options_frame_outer+logs_options_frame_outer,font='Any 12 bold'), sg.Multiline("Hikvision Log Analyzer Logging System:",autoscroll=True,reroute_stdout=True,key='-MULTILINE-KEY-',size=(72,26))]

	input_layout = [ 
			   [sg.Frame('Select image file [.dd/.001], log file [.txt] or folder containing log files:',input_files_frame,font='Any 12')],
			   [sg.Frame('Select output folder:',output_files_frame,font='Any 12')],	   
			   [capabilities_frame],
			   [sg.ProgressBar(max_value=100, orientation='h',size=(75,15), key='-PROGRESS-BAR-',bar_color=("Green","Light Grey"))],
			   [sg.Button("Process"), sg.Button('Cancel')]]

	window = sg.Window('Hikvision Log Analyzer v. '+version, input_layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=False, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True, icon=myfavicon)
	#window.set_min_size(window.size)
	return window

def validate_input(values, window):
	input_f = values['-INPUT-F-']
	output_f = values['-OUTPUT-FOLDER-']
	split_records = values['-SPLITRECORDS-']
	input_choice = ""
	iflag = ""
	oflag = ""
	rflag = ""
	if len(input_f) == 0:
		sg.popup_error("Neither 'INPUT FILE' nor 'INPUT FOLDER' were provided.",title="Input Error",keep_on_top = True, icon=myfavicon)
		iflag =  False
	elif not os.path.exists(input_f):
		sg.popup_error("'INPUT FILE' or 'INPUT FOLDER' does not exist.",title = "Input Error",keep_on_top = True, icon=myfavicon)
		iflag =  False
	elif os.path.isdir(input_f):
		iflag = True
		input_choice = "Folder"
	else:
		if not input_f.lower().endswith(".txt") and not input_f.lower().endswith(".001") and not input_f.lower().endswith(".dd"):
			sg.popup_error(f"File type not supported: You provided {input_f[-3:]} whereas .txt | .dd | .001 types are supported.",title = "Filetype Error",keep_on_top = True, icon='scripts/Images/myfavicon.ico')
			iflag = False
		else:
			iflag = True
			input_choice = Path(input_f).suffix[1:].lower()
	if len(output_f) == 0:
		sg.popup_error("No 'OUTPUT FOLDER' was provided.",title = "Output Error",keep_on_top = True, icon=myfavicon)
		oflag = False
	elif not os.path.exists(output_f):
		sg.popup_error("'OUTPUT FOLDER' does not exist.",title = "Output Error",keep_on_top = True, icon=myfavicon)
		oflag = False
	elif os.path.isdir(output_f):
		oflag = True
	try:
		if int(split_records) < 0:
			sg.popup_error("'Split Records' cannot be negative number. Choose an integer.",title = "Split Records Error", icon=myfavicon,keep_on_top = True)
			rflag = False
	except Exception as e:
		sg.popup_error_with_traceback(f"A 'Split Records' error happened. Here is the info:", e)
		rflag = False
	if 	iflag == False or oflag == False or rflag == False:
		flag = False
	else:
		flag = True
	return [flag,input_choice]

#######################################################################################################
#									"""GUI Code section FINISH"""
#######################################################################################################
#######################################################################################################
#									"""Main Part BEGIN"""
#######################################################################################################

window = make_window(version)

while True:
	event,values = window.read()
	#hrf.mylogger(isEmpty(values['-INPUT-F-']))
	if event in (sg.WIN_CLOSED,'Cancel'):
		break
	elif event == 'About':
		hrf.mylogger(f"\n{cur_time}: User clicked About Info\n")
		about_info = f"""Current Version: {version}\n\nDeveloped by Evangelos Dragonas (@theAtropos4n6)\n\nResearch by:\n-Evangelos Dragonas\n-Costas Lambrinoudakis\n-Michael Kotsis\n\nMore information available at: https://github.com/HikvisionLogAnalyzer"""
		sg.popup(about_info, title='About',button_type=0,keep_on_top=True,icon=myfavicon)
	elif event == 'Process':
		window['-PROGRESS-BAR-'].UpdateBar(5,100)
		hrf.mylogger(values['-INPUT-F-'])
		hrf.mylogger(f"{cur_time}=> User hit Process button.\n")
		hrf.mylogger(f"------------------------------------------------------------------------------------\n")
		hrf.mylogger(f"{cur_time}=>User chose the following options:\n")
		hrf.mylogger(f"{cur_time}=>Input File/Folder: {values['-INPUT-F-']}\n")
		hrf.mylogger(f"{cur_time}=>Output File/Folder: {values['-OUTPUT-FOLDER-']}\n")
		hrf.mylogger(f"{cur_time}=>Image Carving Options:\n")
		hrf.mylogger(f"{cur_time}=>Records Carving Choice: {values['-RECORDSCARVING-']}\n") 
		hrf.mylogger(f"{cur_time}=>Parse File System information: {values['-IFSINFO-']}\n")
		hrf.mylogger(f"{cur_time}=>Parse Hardware information: {values['-IHWINFO-']}\n")
		hrf.mylogger(f"{cur_time}=>Parse Login/Logout information: {values['-ILOGONINFO-']}\n")
		hrf.mylogger(f"{cur_time}=>Parse potential anti-forensics information: {values['-IANTIFORENSICS-']}\n")
		hrf.mylogger(f"{cur_time}=>Export results in CSV format: {values['-ICSVRESULTS-']}\n")
		hrf.mylogger(f"{cur_time}=>Export results in HTML format: {values['-IHTMLRECORDS-']}\n")
		hrf.mylogger(f"{cur_time}=>Split .html files every: {values['-SPLITRECORDS-']}records\n")
		hrf.mylogger(f"{cur_time}=>Log File Analysis Options:\n")
		hrf.mylogger(f"{cur_time}=>Parse Hardware information: {values['-LHWINFO-']}\n")
		hrf.mylogger(f"{cur_time}=>Parse Login/Logout information: {values['-LLOGONINFO-']}\n")
		hrf.mylogger(f"{cur_time}=>Parse potential anti-forensics information: {values['-LANTIFORENSICS-']}\n")
		hrf.mylogger(f"{cur_time}=>Export results in CSV format: {values['-LCSVRESULTS-']}\n")
		hrf.mylogger(f"{cur_time}=>Export results in HTML format: {values['-LHTMLRECORDS-']}\n")
		hrf.mylogger(f"------------------------------------------------------------------------------------\n")
		hrf.mylogger(f"{cur_time}=>Validating User Choices\n")
		window['-PROGRESS-BAR-'].UpdateBar(10,100)
		validation_results = validate_input(values, window)
		window['-PROGRESS-BAR-'].UpdateBar(20,100)
		valid_results = "Validation Failed." if validation_results[0] == False else "Validation Successful."
		hrf.mylogger(f"{cur_time}=>{valid_results}\n")
		window['-PROGRESS-BAR-'].UpdateBar(25,100)
		if valid_results == "Validation Successful.":
			window['-PROGRESS-BAR-'].UpdateBar(30,100)
			parse_user_input(values,validation_results[1])
			hrf.log_exporter(values['-OUTPUT-FOLDER-'],hrf.hk_log)
			window['-PROGRESS-BAR-'].UpdateBar(100,100)
			prinfo = f"""Process Complete"""
			sg.popup(prinfo, title='Hikvision Log Analyzer',button_type=0,keep_on_top=True,icon=myfavicon)
			break

window.close()
