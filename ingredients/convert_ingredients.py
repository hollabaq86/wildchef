import pandas

test = pandas.read_csv('food_ingredients.csv', delimiter=',')

#print(test.columns)
#print(test)

#test_dummies = pandas.get_dummies(test, prefix=['Effect'])

#print(test_dummies)

effects = test['Effect'].unique()
types = test['Type'].unique()
#print(effects)

hot_effects = pandas.get_dummies(test['Effect'], prefix='effect')
hot_types = pandas.get_dummies(test['Type'], prefix='type')

new_test = pandas.concat([test, hot_effects, hot_types], axis=1).drop(['Effect', 'Potency', 'Type'], axis=1)

print(new_test)
print(new_test.columns)

#print(hot_effects)