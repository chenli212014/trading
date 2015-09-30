#!/usr/bin/python 

import re as RE; 

## p1 globals: 
globals()['regex_ticker'] = RE.compile(r'^[A-Z]{1,4}$'); 

## p2 globals; 
globals()['regex_ip'] = RE.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'); 
globals()['regex_port'] = RE.compile(r'^[0-9]{5}$'); 

## p3 globals: 
globals()['sym'] = "Symbol"; 
globals()['dsc'] = "Description"; 
globals()['nat'] = "Country"; 
globals()['cnt'] = "Shares"; 
globals()['prc'] = "Price"; 
globals()['crr'] = "Currency";
globals()['cap'] = "Total Value"; 

globals()['sregex_dq'] = RE.compile(r'\"'); 


globals()['day'] = "Day"
globals()['act'] = "Corporate Action"; 
globals()['date_keys'] = ["month", "date", "year"]; 

globals()['div'] = "dividend"; 
globals()['spl'] = "split"; 
globals()['chg'] = "change"; 
