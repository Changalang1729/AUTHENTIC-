import sys
import csv
import os

left_articles = os.listdir('./left')
# right_articles = os.listdir('./right')
csv.field_size_limit(sys.maxsize)
for left in left_articles:
    if left == '.DS_Store' or '.txt' in left:
        continue
    txt_file = os.path.join('./left', left[:-4] + '.txt')
    print(left)
    with open(txt_file, "w") as my_output_file:
        with open(os.path.join('./left', left), encoding="latin-1") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()
    os.remove(os.path.join('./left', left))