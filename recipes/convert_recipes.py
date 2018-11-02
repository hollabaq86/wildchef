import pandas
from sklearn import linear_model

CSV_FILES = ['train.csv', 'test.csv']

def format_dataframe(filename):
	test_df = pandas.read_csv(filename, delimiter=',')

	# one hot encode recipe categories
	category_df = pandas.get_dummies(test_df['Category'], prefix='recipe_cat')
	recipe_name_df = pandas.get_dummies(test_df['Name'], prefix='name')

	# columns that will be scaled
	to_scale_df = test_df[['Duration', 'Sell Price', 'Health Effect Details']]
	to_scale_df -= to_scale_df.min()
	to_scale_df /= to_scale_df.max()

	# drop the columns that were manipulated so that the pandas-transformed DataFrames can be added in
	test_df = test_df.drop(['Name', 'Category', 'Strength', 'Duration', 'Sell Price', 'Health Effect Details'], axis=1)
	final = pandas.concat([recipe_name_df, test_df, to_scale_df, category_df, ], axis=1)
	return final

training_df = format_dataframe(CSV_FILES[0])
training_y_df = training_df[['Sell Price']]
testing_df = format_dataframe(CSV_FILES[-1])
testing_df.reset_index()
import pdb
pdb.set_trace()

training_df = training_df.drop(['Sell Price'])
clf = linear_model.Lasso(alpha=0.1)
clf.fit(training_df, training_y_df)
training_df.to_csv('input.csv')
print(training_y_df)
print(clf.coef_)
print(clf.predict(training_df))