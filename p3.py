#!/usr/bin/python 

import p1; 

from p1 import sys as S; 
from p1 import re as RE; 
from p1 import itertools as I; 

import locale; 

class portfolio(object): 

	def __init__(self, name): 
		self.name = name; 
		self.globalize_portfolio(); 
		self.globalize_action(); 

	def globalize_portfolio(self): 	
		globals()['sym'] = "Symbol"; 
		globals()['dsc'] = "Description"; 
		globals()['nat'] = "Country"; 
		globals()['cnt'] = "Shares"; 
		globals()['prc'] = "Price"; 
		globals()['crr'] = "Currency";
		globals()['cap'] = "Total Value"; 

		locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ); 
		globals()['sregex_dq'] = RE.compile(r'\"'); 

	def globalize_action(self): 
		globals()['day'] = "Day"
		globals()['act'] = "Corporate Action"; 
		globals()['date_keys'] = ["month", "date", "year"]; 

		globals()['div'] = "dividend"; 
		globals()['spl'] = "split"; 
		globals()['chg'] = "change"; 

	class portfolio_corp: 
		
		def __init__(self, kvars): 
			#print kvars; 
			self.symbol = kvars[sym]; 
			self.description = kvars[dsc]; 
			self.country = kvars[nat]; 
			self.shares = int(kvars[cnt]); 
			self.price = self.share_price(kvars[prc]); 
			self.currency = kvars[crr]; 
			self.value = self.capitalization(kvars[cap]); 

		def show(self): 
			return ','.join([self.symbol, self.description, self.country, \
				str(self.shares), self.price.show(), self.currency, self.value.show()]); 

		class share_price(object): 

			def __init__(self, value_string): 
				self.value_string = value_string; 
				self.value = locale.atof(value_string.replace('"', ''));  

			def show(self): 
				return self.value_string; 

			def get(self): 
				return self.value; 

			def update(self, fval): 
				self.value = fval; 
				a = {'size': self.value, 'unit': 'bytes'}
				self.value_string = locale.format("%(size).2f", a); 

		class capitalization(share_price): 

			def __init__(self, value_string): 
				super(portfolio.portfolio_corp.capitalization, self).__init__(value_string); 
				self.value = locale.atof(sregex_dq.sub("", value_string));  

			def update(self, fval): 
				self.value = fval; 
				a = {'size': self.value, 'unit': 'bytes'}
				self.value_string = '"'+locale.format("%(size).2f", a, grouping=True)+'"'; 

		def change(self, key, new_val): 
			if (key == sym): 
				self.symbol = new_val; 
			elif (key == dsc): 
				self.description = new_val; 
			else: print "Unknown Change Type:", key; sys.exit(0); 

		def share_split(self, denom, numer): 
			self.price.update((self.price.get() / denom) * numer); 
			self.shares = int((float(self.shares) / numer) * denom);  

		def dividend(self, per_share): 
			self.value.update(self.value.get() - (float(self.shares) * per_share));  

	class portfolio_action: 
	
		def __init__(self, **kvars): 
			self.day = self.date(kvars['day']); 
			self.symbol = kvars['sym']; 
			self.description = kvars['act']; 
			self.analyze_action();  

		def analyze_action(self): 
			[atype, adesc] = self.description.split('-'); 
			ttokens = atype.replace('"', '').strip().split(); 
			if (div in ttokens): 
				self.type = div; 
				self.amount = float(RE.split('\ |\/', adesc.strip().replace('"', ''))[0]); 
				#print div, self.amount, atype, adesc; 
			elif (spl in ttokens): 
				self.type = spl; 
				self.denom = float(adesc.strip().split()[0]);
				self.numer = float(adesc.strip().split()[2]); 
				#print spl, self.denom, self.numer, adesc; 
			elif (chg in ttokens): 
				self.type = chg; 
				if (sym in ttokens): 
					self.key = sym; 
				elif ("Name" in ttokens): 
					self.key = dsc; 
				else: print "unknown change elem:", atype; S.exit(1); 
				self.val = (adesc.strip().split()[-1]).replace('"', ''); 
				#print chg, self.key, self.val; 
			else: print "unknown action type", self.description; S.exit(1); 

		class date: 
			
			def __init__(self, date_string): 
				self.date_info = dict(zip(date_keys, date_string.strip().split('/'))); 

			def show(self): 
				return '/'.join(self.date_info.values()); 

class portfolio_information(portfolio): 

	def __init__(self, name, portfolio_file, action_file): 
		super(portfolio_information, self).__init__(name); 
		self.portfolio_file = portfolio_file; 
		self.action_file = action_file; 

	def read_csv(self, file_name, delimiters, segmenter=RE.split): 
		handle = open(file_name, 'r'); 
		self.csv_lines = (segmenter(delimiters, line.strip()) for line in  handle.readlines()); 
		handle.close(); 

	def parse_portfolio(self, csv_lines): 
		self.portfolio = {}; 
		self.portfolio_order = []; 
		self.portfolio_keys = csv_lines[0]; 
		for l in range(1, len(csv_lines), 1): 
			corp = self.portfolio_corp(dict(zip(self.portfolio_keys, csv_lines[l]))); 
			self.portfolio[corp.symbol] = corp; #print corp.symbol; 
			self.portfolio_order.append(corp.symbol); 

	def parse_actions(self, csv_lines): 
		self.actions = {}; 
		self.date_strings = {}; 
		self.action_keys = csv_lines[0]; 
		self.action_order = []; 
		for l in range(1, len(csv_lines), 1): 
			date_tokens = csv_lines[l][0].strip().split('/'); 
			numeric_date = int(date_tokens[2]+date_tokens[0]+date_tokens[1]); 
			if (numeric_date not in self.actions): 
				self.actions[numeric_date] = []; #print "date:", numeric_date; 
				self.date_strings[numeric_date] = csv_lines[l][0]; 
			action = self.portfolio_action(day = csv_lines[l][0], \
				sym = csv_lines[l][1], act = csv_lines[l][2]);  
			self.actions[numeric_date].append(action); 
			if numeric_date not in self.action_order: 
				self.action_order.append(numeric_date);  
		self.action_order.sort(); 

	def portfolio_segment_gen(self): 
		def portfolio_segmenter(delimiters, string): 
			segmented = []; 
			p_state = 0; 
			new_str = ""; 
			for lit in list(string): 
				if ((p_state == 0) and (lit == '"')): 
					p_state = 1; 
					new_str += lit; 
				elif ((p_state == 1) and (lit == '"')):  
					p_state = 0; 
					new_str += lit; 
				elif ((p_state == 0) and (lit in delimiters)): 
					segmented.append(new_str); 
					new_str = ""; 
				else: 
					new_str += lit; 
			segmented.append(new_str); 
			return segmented; 
		return portfolio_segmenter; 

	def p3_info(self): 
		self.read_csv(self.portfolio_file, ',', self.portfolio_segment_gen());
		self.parse_portfolio(list(self.csv_lines));  
		self.read_csv(self.action_file, ','); 
		self.parse_actions(list(self.csv_lines)); 

class portfolio_manager(portfolio_information): 

	def __init__(self, name, portfolio_file, action_file): 
		super(portfolio_manager, self).__init__(name, portfolio_file, action_file); 

	def display_portfolio(self, date_string): 
		print ('^' * 79)+'\n';  
		print date_string; 
		print ','.join(self.portfolio_keys); 
		for symbol in self.portfolio_order: 
			print self.portfolio[symbol].show(); 
		print ('$'*79)+'\n'; 

	def update_portfolio(self, date): 
		for action in self.actions[date]: 
			if (action.type == div): 
				self.portfolio[action.symbol].dividend(action.amount); 
			elif (action.type == spl): 
				self.portfolio[action.symbol].share_split(action.denom, action.numer); 
			elif (action.type == chg): 
				self.portfolio[action.symbol].change(action.key, action.val); 

	def perform_actions(self): 
		self.display_portfolio("Original Portfolio"); 
		for date in self.action_order: 
			self.update_portfolio(date); 
			self.display_portfolio("On date:"+self.date_strings[date]); 

if __name__ == "__main__": 
	if (len(S.argv) == 3): 
		pfm = portfolio_manager("p3", S.argv[1], S.argv[2]); 
		pfm.p3_info(); 
		pfm.perform_actions(); 
	else: 
		print """\n\t\tIncorrect number of parameters: \n
		Necessary Arguments: portfolio_file_name, actions_file_name; """ 
