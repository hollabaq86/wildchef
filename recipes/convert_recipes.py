import pandas

# def separate_ingredients(list):
# 	for ingredient_list in ingredients:
# 		if type(ingredient_list) == str:
# 			separated_ingredients.extend(_prep_columns(ingredient_list))
# 	return separated_ingredients		

# def _prep_columns(list):
# 	columns = list.split(',')
# 	return columns

TEST = pandas.read_csv('output.csv', delimiter=',')

# print(TEST.columns)
TO_SCALE = TEST[['Duration', 'Sell Price', 'Health Effect Details']]
# print(TO_SCALE)

TO_SCALE -= TO_SCALE.min()
TO_SCALE /= TO_SCALE.max()
print(TO_SCALE)

TEST = TEST.drop(['Duration', 'Sell Price', 'Health Effect Details'], axis=1)

FINAL = pandas.concat([TEST, TO_SCALE], axis=1)

print(FINAL.columns)