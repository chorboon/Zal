#!/usr/bin/env python3

# A programme that:
#  - Opens file "data.csv"
#  - Sorts data by price
#  - Prints results to standard out
#  - After you are done submit source and output

import operator

def parse_data():
    csv_list = []
    list_of_values = []
    csv_dict = {}
    header = True
    
    with open('data.csv','rb') as csv_file:
        for binary_line in csv_file:
            raw_line = binary_line.decode('ascii')
#           Need this line to remove newline at end of each line
            line = raw_line.rstrip()
#           Capture first line as the keys
            if header:
                list_of_keys = line.split(',')
                header = False
                continue

            list_of_values = line.split(',')

#           Convert DISCOUNTED_PRICE field to float for correct sorting
            list_of_values[3]=float(list_of_values[3])

#           Make each book entry a dictionary
            csv_dict = { list_of_keys[i] : list_of_values[i] for i in range(0, len(list_of_keys)) }

#           Creating a list of dictionary per entry. Chose this structure to maximise flexibility 
#           in choosing which field to sort, and future schema changes
            csv_list.append(csv_dict)


#   Sorting the list based on Price
    sorted_list = sorted(csv_list,key=operator.itemgetter('Price'))


#   Make output prettier to see sorting more clearly    
    for j in list_of_keys:
            print("{0:35s}".format(str(j)),end='')
    print()
    for i in sorted_list:
        for k,v in i.items():
            print("{0:35s}".format(str(v)),end='')
        print()


def main():
    parse_data()


if __name__ == "__main__":
    main()
