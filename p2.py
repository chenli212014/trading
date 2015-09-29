#!/usr/bin/python 

import p1; 

from p1 import sys as S; 
from p1 import re as RE; 

globals()['regex_ip'] = RE.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'); 
globals()['regex_port'] = RE.compile(r'^[0-9]{5}$'); 

def locate_netelem(netlines, pattern): 
	located = []; 
	for line in netlines: 
		located.append(pattern(line)); 
	return located; 

def pattern_gen(tgt_regex): 
	def patternizer(sym_list): 
		for sym in sym_list: 
			if (tgt_regex.match(sym)): return sym; 
		return -1; 
	return patternizer; 

def check_netstat(ip, port): 
	calc_port = 50000 + (200 * ip[2]) + ip[3]; 
	if (calc_port != int(port)): 
		print '.'.join(map(str, ip)), "expected", calc_port, "found", port;  

def parse_p2(file_name): 
	port_pattern = pattern_gen(regex_port); 
	netlines = list(p1.read_file(S.argv[1], ';|\ |\='));  
	ips = locate_netelem(netlines, pattern_gen(regex_ip)); 
	ports = locate_netelem(netlines, pattern_gen(regex_port));
	for i in range(0, len(ips), 1): 
		check_netstat(map(int, RE.split('\.', ips[i])), ports[i]); 

if __name__ == "__main__": 
	if (len(S.argv) == 2): 
		parse_p2(S.argv[1]); 
	else: 
		print """\n\t\tIncorrect number of parameters: \n
		Necessary Argument: netstats_file """ 
