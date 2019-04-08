#finding the right amount to save away
global bisection
bisection = 0

def best_saving_rate(start_rate,end_rate,start_salary):
	global bisection
	bisection = bisection + 1
	if end_rate - start_rate < 0.001:
		return start_rate
	mid_rate = (start_rate + end_rate)/2
	time_start = time_calculate(start_salary,start_rate)
	time_end = time_calculate(start_salary,end_rate)
	time_mid = time_calculate(start_salary,mid_rate)
	if time_end > 36:
		return -1
	if time_mid > 36:
		return best_saving_rate(mid_rate,end_rate,start_salary)
	else:
		return best_saving_rate(start_rate,mid_rate,start_salary)

def time_calculate(start_salary,portion_saved):
	total_cost = 1000000
	semi_annual_rate = 0.07
	annual_return = 0.04
	down_payment = 0.25
	month = 0
	saving = 0
	month_salary = start_salary/12
	month_saved = month_salary * portion_saved
	month_return = annual_return/12
	while saving < total_cost*down_payment:
		saving = saving + month_saved
		saving = saving * (1 + month_return)
		month = month + 1
		if month % 6 == 0:
			month_salary = month_salary *(1 + semi_annual_rate)
			month_saved = month_salary*portion_saved
	return month

start_salary = int(input('Enter the starting salary:'))
rate = best_saving_rate(0,0.5,start_salary)
if rate < 0:
	print('It is not possible to pay the down payment in three years.\n')
else:
	print('Best saving rate:',round(rate,4),'\n')
	print('Steps in bisection search:',bisection,'\n')
