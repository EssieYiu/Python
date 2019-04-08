#saving, with a rise
annual_salary = float(input('Enter your starting annual salary:\n'))
portion_saved = float(input('Enter the percent of your salary to save, as a demical:\n'))
total_cost = float(input('Enter the cost of your dream home:\n'))
semi_annual_raise = float(input('Enter the semi-annual raise, as a demical;\n'))
portion_down_payment = 0.25
current_savings = 0.0
r = 0.04
month_time = 0
month_salary = annual_salary/12
month_saved = month_salary*portion_saved
while current_savings < total_cost*portion_down_payment:
	current_savings = current_savings + month_saved
	current_savings = current_savings * (1 + r/12)
	month_time = month_time + 1
	if month_time % 6 == 0:
		month_salary = month_salary * (1 + semi_annual_raise)
		month_saved = month_salary * portion_saved
print('Number of months:',month_time,'\n')
