import re
import pandas as pd
import DocumentParsing.form_patterns as patterns
from DocumentParsing.cell_class import DEBUG


class Expenditures:

	# Debt service
	#   Principal retirement
	#   Interest
	# I believe that you can also have 'interest' outside and it's assumed to be
	# debt
	
	# Here we want
	# 	total expenditures

	def __init__(self, labels: pd.Series, column: pd.Series, revenues_after_expenditures_index: int, expenditures_index: int) -> None:

		if DEBUG:
			print('Finding expenditures')
			print(expenditures_index, revenues_after_expenditures_index)

			print(labels)
			print(column)

		self._expenditures_index = expenditures_index
		self._revenues_after_expend_index = revenues_after_expenditures_index

		self.has_one_entry = False

		self.has_one_entry = revenues_after_expenditures_index - expenditures_index == 2
			
		# Limit our area to just the ones that contain expenditures
		use_labels = labels.iloc[expenditures_index: revenues_after_expenditures_index]
		use_column = column.iloc[expenditures_index: revenues_after_expenditures_index]

		self._labels = use_labels.copy().reset_index()
		self._column = use_column.copy().reset_index()
		
		self.bond_issuance_costs: int = 0
		self.capital_projects: int = 0
		self.principle_retirement: int = 0
		self.interest: int = 0
		# self.debt: int = 0
		self.economic_dev: int = 0

		self.total_expenditures: int = 0

		self.hazards: list[str] = []

		if expenditures_index == -1 or revenues_after_expenditures_index == -1:
			self.hazards.append('Cannot complete expenditures object')
			return

		pattern_pairs = [
			(patterns.bond_pattern, 'bond_issuance_costs'),
			(patterns.capital_projects_pattern, 'capital_projects'),
			(patterns.principle_retirement_pattern, 'principle_retirement'),
			(patterns.interest_pattern, 'interest'),
			(patterns.economic_dev_pattern, 'economic_dev'),
			(patterns.total_expenditures_pattern, 'total_expenditures')
		]

		if DEBUG:
			print(use_labels)

		for index, value in use_labels.items():

			if DEBUG:
				print(index, value, use_column[index])

			number = 0
			is_negative = False
			number_na = False
			number_absent = False
			test_me = use_column[index]
			if pd.isna(test_me):
				number_na = True
				number = 0
				if DEBUG:
					print('Field blank, setting 0')
			elif re.sub(r'\D', '', test_me) == '':
				number_absent = True
				number = 0
				if DEBUG:
					print('Number is absent, set 0')
			else:
				if re.match(patterns.full_negative_pattern, test_me):
					is_negative = True
					# We'll remove parents next
					test_me = re.sub(r'\(|\)', '', test_me)
				if not test_me.isnumeric():
					test_me = re.sub(r'\D', '', test_me)
					if DEBUG:
						print('Number value is non-numeric, removing symbols')
				number = int(test_me)
				if is_negative:
					number = -number

			# Find label
			field = labels[index]
			if pd.isna(field) or field.strip() == '':
				if number != 0:
					self.hazards.append(f'Number {number} was not attached to a field')
				# It's not going to match anything so why continue
				continue

			# Match field
			for pair in pattern_pairs:
				if re.match(pair[0], value):

					if DEBUG:
						print('match for', pair[1])

					if number_na or number_absent:
						self.hazards.append(f'field "{pair[1]}" had no value attached')
						if DEBUG and self.has_one_entry:
							print("The 'total_expenditures' had no value because of that")
					else:
						setattr(self, pair[1], number)
						
						if self.has_one_entry:
							self.total_expenditures = number
					break
			else:
				if number != 0:
					self.hazards.append(f'Number {number} was not attached to a field')

		if self.total_expenditures == 0:
			if DEBUG:
				print(use_labels)
				print(use_column)
				print("Couldn't find total expenditures. Attempting replacement by adding")
			self.hazards.append('Total expenditures did not match. Guessing total by adding individual')
			self.total_expenditures = (
				self.bond_issuance_costs +
				self.capital_projects +
				self.principle_retirement +
				self.interest +
				# self.debt +
				self.economic_dev
			)
		else:
			check_me = (
				self.bond_issuance_costs +
				self.capital_projects +
				self.principle_retirement +
				self.interest +
				# self.debt +
				self.economic_dev
			)
			if self.total_expenditures != check_me:
				self.hazards.append('Checksum failed')
		
	def vertical_check_sum(self) -> bool:
		if self._expenditures_index == -1 or self._revenues_after_expend_index == -1:
			return False

		check_me = (self.bond_issuance_costs +
		self.capital_projects +
		self.principle_retirement +
		self.interest +
		self.economic_dev)

		return check_me == self.total_expenditures
	
	def display(self):
		print('bond_issuance_costs:', self.bond_issuance_costs)
		print('capital_projects:', self.capital_projects)
		print('principle_retirement:', self.principle_retirement)
		print('interest:', self.interest)
		print('economic_dev:', self.economic_dev)
		print('total_expenditures:', self.total_expenditures)
