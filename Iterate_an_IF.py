myio = input('enter the name of a city:').title()

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = []
for key in CITY_DATA:
    print(key)
    cities.append(key.title())



if myio in cities:
    myresult = ""
else:
    myresult = " NOT"

print('\n{} is{} in the list.'.format(myio, myresult))
