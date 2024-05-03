import re

full_negative_pattern = re.compile(r'^\(.*\)$')


# Revenue form patterns

interest_pattern = re.compile(r'.*[li]nterest.*$', re.IGNORECASE)
interest_other_pattern = re.compile(r'.*investment\sincome.*$', re.IGNORECASE)

property_tax_pattern = re.compile(r'[,\-_\'=~\s.—§©:]*property\s*tax(es)?[$,Ss\-_\'=~\s.—§©:]*$', re.IGNORECASE)
sales_tax_pattern = re.compile(r'[,\-_\'=~\s.—©:]*[5s$§]ales\s*tax(es)?$', re.IGNORECASE)
rent_pattern = re.compile(r'[,\-_\'=~\s.—§©:]*rent(al)?\s*(income|revenue)?[$,Ss\-_\'=~\s.—§©:]*$', re.IGNORECASE)
miscellaneous_pattern = re.compile(r'[,\-_\'=~\s.—§©:]*Mise?cell[ae]neous\s*(income|revenue)?\s*(\(Note \d\))?[$,Ss\-_\'=~\s.—§©:]*$', re.IGNORECASE)
other_pattern = re.compile(r'^.*other.*$', re.IGNORECASE)

land_pattern = re.compile(r'.*sale\sof\sland.*$', re.IGNORECASE)
liquor_pattern = re.compile('.*liquor.*$', re.IGNORECASE)
reimbursed_pattern = re.compile(r'.*reimbursed\srevenue.*$', re.IGNORECASE)  # Occurs in ONE place

total_rev_pattern = re.compile(""
	r"[\.:|;‘_\s-]*to[ti]a[l!] reven[u\s]es\s*[:-]*$|"
	r"tota[l!] revenues \.$|"  # 2004_44. Speck
	r"Tota[l!] reven e[sn]$"  # 2008_14 and 2006_15? Idk if these are accurate
"", re.IGNORECASE)


# Statement form patterns

revenue_after_expenditure_pattern = re.compile(""
	r"^excess of revenues? (over|of) expen?ditures[., ]*$|"
	r"^[’ ]*excess of expenditures over revenues?[:. ]*|^expenditures over revenues?$|"
	r"^revenues? (over|under) expenditures$|"
	r"^revenues? over \(under\) expenditures$|"
	r"^deficiency of revenues over expenditures$|"
	r"^excess \(deficiency\) of revenues over expenditures$"
"", re.IGNORECASE)

revenue_header_pattern = re.compile(r'^[^a-z]*revenues?(: en)?[^a-z]*$', re.IGNORECASE)

expenditure_header_pattern = re.compile(""
	r"[\.:|;‘_]*\s*expenditures:?$|"
	r"[\.:|;‘_]*\s*expenditures\/expenses?:?$|"	 # Introduced 2002_1
	r"expenditu\. 2s$|"  # Edge case 1997_27
	r"expenditures\/expenses: \."  # Edge case 2007_46
"", re.IGNORECASE)

other_finance_sources_header_pattern = re.compile(r'other financ.{3} (sources\s?)?(\/?\(?uses\)?)?[:. ”]*|financing uses:', re.IGNORECASE)

transfers_in_pattern = re.compile(r'.*transfers in.*$', re.IGNORECASE)
transfers_out_pattern = re.compile(r'.*transfers? out.*$', re.IGNORECASE)
surplus_pattern = re.compile(r'.*surp[li]us distr[iu]bution.*$', re.IGNORECASE)
tax_liability_pattern = re.compile(r'tax liability distribution.*', re.IGNORECASE)
debt_plus_bond_refund_pattern = re.compile(r'^.*proceeds of debt.*|and refunding expenses \(note 2\)', re.IGNORECASE)  # Specifically for 1999 and 2000_31
escrow_agent_pattern = re.compile(r'payment to refunded bond escrow agent', re.IGNORECASE)

total_other_finance_sources_pattern = re.compile(r'tota[li!] other financ.{3} (sources ?)?(\/?\(?uses\)?)?( ?- net)?', re.IGNORECASE)

change_in_net_position_pattern = re.compile(r'.*change in ?ne[it] ?(assets|position).*', re.IGNORECASE)

net_assets_funds_header_pattern = re.compile(r'^(’ )?fund ba[tl]ance( \(deficit\))?\/ne[it] (position|asse[ti]s).*$', re.IGNORECASE)

begin_of_year_pattern = re.compile('.*beginn(ing|gin) of year.*$', re.IGNORECASE)
end_of_year_pattern = re.compile('.*end of year.*$', re.IGNORECASE)


# Expenditures form patterns
bond_pattern = re.compile(r'.*bond\s*issuance.*$', re.IGNORECASE)
capital_projects_pattern = re.compile(r'.*capita[li]\s*projects.*$', re.IGNORECASE)
principle_retirement_pattern = re.compile(r'.*principa[lt]\s*retirement.*$', re.IGNORECASE)
interest_pattern = re.compile(r'.*[li]nterest.*$', re.IGNORECASE)
economic_dev_pattern = re.compile(r'.*eco[nm][oa][mn]ic\s*(deve[li]opment|projects?)?\s*(deve[li]opment|projects?)?.*$', re.IGNORECASE)

total_expenditures_pattern = re.compile(r'.*tota[l!]\sexpenditures.*$', re.IGNORECASE)
