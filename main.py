"""
Module of Shtonda Yelizaveta, contains main function
"""
import sys
import Loading


def developer_information():
    """
    prints information about student and variant
    """
    print('This program is coded by Shtonda Yelizaveta,  К-13/2. Variant 140.\n')


def problem_condition():
    """
    prints information about condition of lab variant
    """
    print("""Program takes, processes data and returns information about exercises in tests, done by students. 
Processing: program finds all the problems that were solved in each attempt by at least 60%. Prints the following
information for each of them: condition, number of attempts, number of attempts not worse than 60%, percentage 
of attempts not worse than 60% for all attempts. Then prints information about every prompt of problem:
year, last name, first name, middle name, percentage of points scored, sorted by last name, first name, middle name, 
the percentage of points scored in descending order, year.""")


def process(path):
    """
    :param path: received as second parameter in cmd

    calls method load_ini(), which opens and process .ini file
    calls method load(), which loading all data in object
    calls method output(), which write down asked information in .txt file
    in case of error catches it and prints proper information
    """
    try:
        print(f'ini {path}: ', end='')
        main_file, additional_file, input_encoding, output_file, output_encoding = Loading.load_ini(path)
        Loading.load(main_file, additional_file, input_encoding).output(output_file, output_encoding)
    except BaseException as b:
        print('\n***** program aborted *****')
        print(b)

if not len(sys.argv) == 2:
    print('***** program aborted *****')
else:
    developer_information()
    problem_condition()
    print('*****')
    process(sys.argv[1])
