# The basic target here is to read databases from the .csv files and manipulate them.

# Import statements
import csv
import numpy
import pandas

# Invoke File
countryData_filename = 'CountryData.csv'

# We could import using any of the following strategies:
# 1. Using direct CSV readers
#       reader = csv.reader(countryData)
#       country_Data_read = list(reader)
# 2. Using numpy (preferable for just numbers)
#       country_Data_read = numpy.loadtxt(countryData, delimiter=',')
# 3. Using pandas (really useful)
tags = ['id','name']
country_Data = pandas.read_csv(countryData_filename, names=tags)

print(country_Data.shape)
