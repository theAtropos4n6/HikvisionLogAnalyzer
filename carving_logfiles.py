import binascii
import datetime
from datetime import timezone
import codecs
import re
import csv
import os
import carving_utils as carutil
import scripts.html_report_files as hrf

def carved_logfiles(input_file):
	try:
		offset = 0
		blocksize = 512
		fs_signature ='48494b564953494f4e4048414e475a484f55' #HIKVISION@HANGZHOU

		with open(input_file,'rb') as img_file:
			global offsets
			global log_start_offset
			global log_size
			log_start_offset = 0
			log_size = 0
			offsets = ['']
			while True:
				data = img_file.read(blocksize) # read image per blocksize
				blk_to_str = binascii.hexlify(data).decode('utf-8')
				if not data:
					hrf.mylogger("Searched the whole image and no HikVision File System was found!")
					break #continues till the end of image
				if fs_signature in blk_to_str: # if == HIKVISION@HANGZHOU
					offsets = carutil.parse_fs_info(blk_to_str) #retrieves fs info, offset etc.
					log_start_offset = offsets[0]
					log_size = offsets[1]
				offset += blocksize
				if log_size > 0 and offset == log_start_offset: #when reading iteration reach the offset where the logs begin
					log_data = img_file.read(log_size) # read the whole block where the logs reside
					log_data_to_str = binascii.hexlify(log_data).decode('utf-8') #convert to big string
					carved_info = carutil.parse_log_data(log_data_to_str,log_start_offset) # pass it on for parsing -> returned value is a dictionary where key is the no. of log entry and value is the extracted data
					break#searching finishes as soon as the dict returns
		return carved_info
	except Exception as e:
		hrf.mylogger(f"Error occured while reading image file. The error message was {e}")

