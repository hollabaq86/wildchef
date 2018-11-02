import csv


def ingredients_prep(ingredients_list):
    row_ingredients = {}
    split_up = ingredients_list.split(',')
    for item in split_up:
        if " x" in item:
            working = item.split(' x')
            ingredient_key = working[0]
            multiplier = int(working[-1].strip()[-1])
            row_ingredients['ing_' + ingredient_key] = multiplier
        else:
            row_ingredients['ing_' + item] = 1
    return row_ingredients


def get_recipe_effect(recipe_name):
    return recipe_name.split(' ')[0]


def build_writing_row(recipe, ingredients, recipe_effects, health_effects):
    written_row = {}
    written_row['Name'] = recipe['Name']
    written_row['Category'] = recipe['Category']

    # adding the first word in recipe names as columns in case this is a valuable feature
    for adjective in recipe_effects:
        if recipe['Recipe Name Effect'] in adjective:
            written_row[adjective] = 1
        else:
            written_row[adjective] = 0
    written_row['Strength'] = recipe['Strength']

    working_duration = recipe['Duration']
    if working_duration == '':
        written_row['Duration'] = 0
    else:
         time_measurement = working_duration.split(':')
         minutes = float(time_measurement[0])
         seconds = float(time_measurement[-1]) / 60
         written_row['Duration'] = minutes + seconds


    written_row['Sell Price'] = recipe['Sell Price']

    # adding row entries for all possible ingredient columns
    for key in ingredients:
        if key in recipe['Ingredients']:
            written_row[key] = recipe['Ingredients'][key]
        else:
            written_row[key] = 0

    #adding row entries for all possible health effect columns
    row_effects = recipe['Health Effects'].split(',')
    for key in health_effects:
        written_row[key] = 0
        for row_effect in row_effects:
            if row_effect in key:
                written_row[key] = 1

    # adding columns for max hearts or reg hearts
    written_row['Health Effect Details'] = float(recipe['Health Effect Details'])

    return written_row


OUTPUT = {}
INGREDIENTS = {}
RECIPE_EFFECTS = {}
HEALTH_EFFECTS = {}


with open('raw_data.csv',) as csvfile:
    for row in csv.DictReader(csvfile):

        name = row['Food']
        category = 0 
        #recipes can have multiple combinations
        for recipe in OUTPUT:
            if name in recipe:
                category += 1  


        prepped_ingredients = ingredients_prep(row['Ingredients'])
        for key in prepped_ingredients:
            if key not in INGREDIENTS:
                INGREDIENTS[key] = 1
            else:
                INGREDIENTS[key] += 1

        name_effect = get_recipe_effect(name)
        if 'first_' + name_effect in RECIPE_EFFECTS:
            RECIPE_EFFECTS['first_' + name_effect] += 1
        else:
            RECIPE_EFFECTS['first_' + name_effect] = 1   
        
        health_effect = row['Effect Type'].split(',')
        if row['Effect Type'] == '':
            health_effect = ['Unknown']
        elif row['Effect Type'] == '' and float(row['Effect Details']) > 0:
            health_effect = ['Hearts']  
        for effect in health_effect:
            if 'effect_' + effect in HEALTH_EFFECTS:
                HEALTH_EFFECTS['effect_' + effect] += 1
            else:
                HEALTH_EFFECTS['effect_' + effect] = 1

        if row['Effect Details'] == '':
            health_effect_details == 'NaN'
        elif 'x+' in row['Effect Details']: 
            health_effect_details = float(row['Effect Details'].split('x+')[-1]) + 10
        else: 
            health_effect_details = row['Effect Details']
                
        recipe = {
        'Name': name,
        'Category': category,
        'Recipe Name Effect': name_effect,
        'Strength': row['Strength'],
        'Duration': row['Duration'],
        'Sell Price': row['Sell Price'], 
        'Ingredients': prepped_ingredients,
        'Health Effects': row['Effect Type'],
        'Health Effect Details': health_effect_details
        }

        OUTPUT[name+'_'+str(category)] = recipe


HEADERS = ['Name','Category']+list(RECIPE_EFFECTS.keys())+['Strength','Duration','Sell Price']+list(INGREDIENTS.keys())+list(HEALTH_EFFECTS.keys())+['Health Effect Details']


with open('output.csv', 'w') as csvfile:
    WRITER = csv.DictWriter(csvfile, fieldnames=HEADERS)
    WRITER.writeheader()
    for recipe in OUTPUT: #recipe is the key, which are the names of the recipes in Output
        add_to_csv = build_writing_row(OUTPUT[recipe], INGREDIENTS, RECIPE_EFFECTS, HEALTH_EFFECTS)
        WRITER.writerow(add_to_csv) 
