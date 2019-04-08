#house hunting
annual_salary = float(input('Enter your annual salary:\n'))
portion_saved = float(input('Enter the percent of your salary to save, as a demical:\n'))
total_cost = float(input('Enter the cost of your dream home\n'))
portion_down_payment = 0.25
current_savings = 0.0
r = 0.04
month_time = 0
month_saved = annual_salary/12*portion_saved
while current_savings < total_cost*portion_down_payment:
	 current_savings = current_savings + month_saved
	 current_savings = current_savings * (1 + r/12)
	 month_time = month_time + 1
print('Number of months;',month_time,'\n')
