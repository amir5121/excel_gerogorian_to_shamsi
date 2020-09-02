import pandas as pd
from dateutil import parser
from jdatetime import datetime
import sys
import json

df = pd.read_excel('input.xlsx')
grouped = dict()

also_group_bye = len(sys.argv[1:]) > 0

result_groups = dict()

for name, values in df.iteritems():
	row_value = str(values[0])
	print(name, row_value, end=' ==========> ')
	try:
		if len(row_value) > 9:
			parser.parse(row_value)
		else:
			raise ValueError
	except (ValueError, OverflowError):
		print()
		pass
	else:
		items = list()
		i = 0
		print("There are", len(values), "items for column", name)
		print("Done with 0%", end='')
		for row in values:
			i += 1
			if i % 1000 == 0:
				print(int(i / len(values) * 100), end='%, ', flush=True)
			try:
				jalali_date = datetime.fromgregorian(
					datetime=parser.parse(str(row)))
				if also_group_bye:
					for argument in sys.argv[1:]:
						selected_column = int(argument) - 1
						selected_column_name = df.columns[selected_column]
						# print("ASDASDASD", grouped, flush=True)
						grouped_date = jalali_date.strftime("%Y-%m")
						# print("B", selected_column_name, df.values[i][selected_column], flush=True)
						# print("I", i, flush=True)
						grouped.update(
							{
								grouped_date: [
									grouped.get(grouped_date, [0, 0])[0] + int(df.values[i - 1][selected_column]),
									grouped.get(grouped_date, [0, 0])[1] + 1,
								]
							}
						)
				# grouped.update(
				# 	{
				# 		f'{selected_column_name}_date': grouped_date,
				# 		f'{selected_column_name}_sum': grouped.get(f'{selected_column_name}_sum', {}).get(
				# 			grouped_date, 0) + int(df.values[selected_column][i]),
				# 		f'{selected_column_name}_count': grouped.get(f'{selected_column_name}_sum', {}).get(
				# 			grouped_date, 0) + int(df.values[selected_column][i])
				# 	}
				# )
				items.append(jalali_date.strftime("%Y-%m-%d %H:%M"))

			except ValueError:
				items.append("N/A")
		print("All done")
		result_groups.update(
			{
				name: grouped
			}
		)
		grouped = dict()
		df[f'{name}_jalali'] = items

df.to_excel("out.xlsx")  # Write DateFrame

res = dict()

with open('results.json', 'w') as result_json:
	result_json.write(json.dumps(result_groups))

for name, values in result_groups.items():
	res[f'{name.lower().replace(" ", "_")}_dates'] = list(values.keys())
	res[f'{name.lower().replace(" ", "_")}_sum'] = [i[0] for i in values.values()]
	res[f'{name.lower().replace(" ", "_")}_count'] = [i[1] for i in values.values()]

print(res)
df = pd.DataFrame(res)
df.to_excel("out_grouped2.xlsx")  # Write DateFrame
