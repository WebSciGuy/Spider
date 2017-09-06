import csv
from projectData import *
from domain import *

# PL.csv
print('Preparing ' + PROJECT_NAME + '/' + PROJECT_NAME + 'PL' + '.csv')
txt_source = (PROJECT_NAME + '/' + PROJECT_NAME + 'PL' '.txt')
csv_file = (PROJECT_NAME + '/' + PROJECT_NAME + 'PL' + '.csv')

in_txt = csv.reader(open(txt_source, "r"), delimiter = ',')
out_csv = csv.writer(open(csv_file, 'w', newline=''))

out_csv.writerows(in_txt)

#WL.csv
print('Preparing ' + PROJECT_NAME + '/' + PROJECT_NAME + 'WL' + '.csv')
txt_source = (PROJECT_NAME + '/' + PROJECT_NAME + 'WL' + '.txt')
csv_file = (PROJECT_NAME + '/' + PROJECT_NAME + 'WL' + '.csv')

in_txt = csv.reader(open(txt_source, "r"), delimiter = ',')
out_csv = csv.writer(open(csv_file, 'w', newline=''))

out_csv.writerows(in_txt)

# WLC.csv
print('Preparing ' + PROJECT_NAME + '/' + PROJECT_NAME + 'WLC' + '.csv')
txt_source = (PROJECT_NAME + '/' + PROJECT_NAME + 'WLC' + '.txt')
csv_file = (PROJECT_NAME + '/' + PROJECT_NAME + 'WLC' + '.csv')

in_txt = csv.reader(open(txt_source, "r"), delimiter = ',')
out_csv = csv.writer(open(csv_file, 'w', newline=''))

out_csv.writerows(in_txt)


