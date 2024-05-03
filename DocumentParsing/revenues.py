from __future__ import annotations
import re
import pandas as pd
import DocumentParsing.form_patterns as patterns
from DocumentParsing.cell_class import DEBUG

# Here we want
# 	property tax


class Revenues:

	# It's structured in two because we have year/statement/adjustments/governmental
	def __init__(self, labels: pd.Series, column: pd.Series, revenue_index: int, expenditures_index: int) -> None:

		self._revenue_index = revenue_index
		self._expenditures_index = expenditures_index

		self.has_one_entry = expenditures_index == revenue_index + 2

		use_labels = labels.iloc[revenue_index:expenditures_index]
		use_column = column.iloc[revenue_index:expenditures_index]

		self._labels = use_labels.copy().reset_index()
		self._column = use_column.copy().reset_index()

		self.interest: int = 0
		self.interest_other: int = 0
		self.property_tax: int = 0
		self.sales_tax: int = 0
		self.rent: int = 0
		self.miscellaneous: int = 0
		self.other: int = 0
		self.land: int = 0
		self.liquor: int = 0
		self.reimbursed: int = 0

		self.total_revenue: int = 0

		self.hazards: list[str] = []

		if revenue_index == -1 or expenditures_index == -1:
			self.hazards.append('Cannot complete revenues object')
			return

		pattern_pairs = [
			(patterns.total_rev_pattern, 'total_revenue'),
			(patterns.interest_pattern, 'interest'),
			(patterns.interest_other_pattern, 'interest_other'),
			(patterns.property_tax_pattern, 'property_tax'),
			(patterns.sales_tax_pattern, 'sales_tax'),
			(patterns.rent_pattern, 'rent'),
			(patterns.miscellaneous_pattern, 'miscellaneous'),
			(patterns.other_pattern, 'other'),
			(patterns.land_pattern, 'land'),
			(patterns.liquor_pattern, 'liquor'),
			(patterns.reimbursed_pattern, 'reimbursed'),
		]

		for index, value in use_labels.items():

			if DEBUG:
				print(index, value, use_column[index])

			# Find number
			number = 0
			is_negative = False
			number_na = False
			number_absent = False
			test_me = use_column[index]
			if pd.isna(test_me):
				number_na = True
				if DEBUG:
					print('Field blank, setting 0')
				number = 0
			elif re.sub(r'\D', '', test_me) == '':
				number_absent = True
				if DEBUG:
					print('Number is absent, set 0')
				number = 0
			else:
				if re.match(patterns.full_negative_pattern, test_me):
					is_negative = True
					# We'll remove parens next
					test_me = re.sub(r'\(|\)', '', test_me)
				if not test_me.isnumeric():
					if DEBUG:
						print('Number value is non-numeric, removing symbols')
					test_me = re.sub(r'\D', '', test_me, flags=re.IGNORECASE)
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
						if self.has_one_entry and DEBUG:
							print("The 'total_revenue' had no value because of that")
					else:
						if DEBUG:
							print('setting', pair[1], number)
						setattr(self, pair[1], number)
						
						if self.has_one_entry:
							if DEBUG:
								print("Found 'the one' field")
							self.total_revenue = number
					break
			else:
				if number != 0:
					self.hazards.append(f'Number {number} was not attached to a field')

		if self.property_tax == 0 and DEBUG:
			print('Did this one have no property tax?')

		if self.total_revenue == 0:
			if DEBUG:
				print(use_labels)
				print(use_column)
				print("Couldn't find total revenue. Attempting replacement by adding")
			self.hazards.append('Total revenue did not match. Guessing total by adding individual')
			self.total_revenue = (
				self.interest +
				self.interest_other +
				self.property_tax +
				self.sales_tax +
				self.rent +
				self.miscellaneous +
				self.other +
				self.land +
				self.liquor +
				self.reimbursed
			)
		else:
			check_me = (
				self.interest +
				self.interest_other +
				self.property_tax +
				self.sales_tax +
				self.rent +
				self.miscellaneous +
				self.other +
				self.land +
				self.liquor +
				self.reimbursed
			)

			if self.total_revenue != check_me:
				self.hazards.append('Checksum failed')

	def vertical_check_sum(self):
		if self._revenue_index == -1 or self._expenditures_index == -1:
			return False
		
		check_me = (self.interest +
		self.interest_other +
		self.property_tax +
		self.sales_tax +
		self.rent +
		self.miscellaneous +
		self.other +
		self.land +
		self.liquor +
		self.reimbursed)

		return check_me == self.total_revenue
	
	def horizontal_check_sum(governmental_funds: Revenues, adjustments: Revenues, statement: Revenues):
		governmental_funds.passes_horizontal_checksum = statement.total_revenue - adjustments.total_revenue == governmental_funds.total_revenue

		governmental_funds.passes_whole_checksum = (
			statement.interest - adjustments.interest == governmental_funds.interest and
			statement.interest_other - adjustments.interest_other == governmental_funds.interest_other and
			statement.property_tax - adjustments.property_tax == governmental_funds.property_tax and
			statement.sales_tax - adjustments.sales_tax == governmental_funds.sales_tax and
			statement.rent - adjustments.rent == governmental_funds.rent and
			statement.miscellaneous - adjustments.miscellaneous == governmental_funds.miscellaneous and
			statement.other - adjustments.other == governmental_funds.other and
			statement.land - adjustments.land == governmental_funds.land and
			statement.liquor - adjustments.liquor == governmental_funds.liquor and
			statement.reimbursed - adjustments.reimbursed == governmental_funds.reimbursed and
			governmental_funds.passes_horizontal_checksum
		)

	def display(self):
		print('interest:', self.interest)
		print('interest_other:', self.interest_other)
		print('property_tax:', self.property_tax)
		print('sales_tax:', self.sales_tax)
		print('rent:', self.rent)
		print('miscellaneous:', self.miscellaneous)
		print('other:', self.other)
		print('land:', self.land)
		print('liquor:', self.liquor)
		print('reimbursed:', self.reimbursed)
		print('total_revenue:', self.total_revenue)
