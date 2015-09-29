#!/usr/bin/python 

import sys, re, itertools; 

globals()['regex_ticker'] = re.compile(r'^[A-Z]{1,4}$'); 

def read_file(file_name, delimiters, selection_mech=lambda x : x): 
	handle = open(file_name, 'r'); 
	slines = ((' '.join(selection_mech(re.split(delimiters, line.strip())))).split() for line in  handle.readlines()); 
	handle.close(); 
	return slines; 

def ticker_gen(): 
	def selector(sym_list): 
		processed = []; 
		for sym in sym_list: 
			processed.append(sym if regex_ticker.match(sym) else ' '); 	
		return processed; 
	return selector;  

def parse_p1(sym_file, dat_file): 
	symlines = read_file(sym_file, '\ '); 
	datlines = read_file(dat_file, '\=|\ ', ticker_gen()); 
	symset = set(list(itertools.chain.from_iterable(symlines))); 
	datset = set(list(itertools.chain.from_iterable(datlines))); 
	diff_set = datset - symset; 
	print '\t'.join(list(diff_set)); 

if __name__ == "__main__": 
	if (len(sys.argv) == 3): 
		parse_p1(sys.argv[1], sys.argv[2]); 
	else: 
		print """\n\t\tIncorrect number of parameters: \n
		Necessary Arguments: symbol_file_name, data_file_name; """ 
