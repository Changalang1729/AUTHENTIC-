import sys
import csv
import os

Right_articles = os.listdir('./Right')
# right_articles = os.listdir('./right')
csv.field_size_limit(sys.maxsize)
for Right in Right_articles:
    if Right == '.DS_Store' or '.txt' in Right:
        continue
    txt_file = os.path.join('./Right', Right[:-4] + '.txt')
    print(Right)
    with open(txt_file, "w") as my_output_file:
        with open(os.path.join('./Right', Right), encoding="latin-1") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()
    os.remove(os.path.join('./Right', Right))