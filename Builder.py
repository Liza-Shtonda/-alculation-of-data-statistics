"""
Module of Shtonda Yelizaveta, contains class Builder
"""
import Information
import Loading
import json
import csv


class Builder:
    """
    contains functions, which open and process main_file, and pass data to object of class Information
    """

    def load(self, data, main_file, input_encoding):
        """
        :param data: instance of the class Information
        :param main_file: relative path to .csv file
        :param input_encoding: type of encoding of main_file
        opens main_file, process it, counts number of records and sum of lengths of surnames in main_file,
        after processing pass data to class Information
        """
        with open(main_file, 'r', encoding=input_encoding) as f, data:
            r = csv.reader(f, delimiter=';', skipinitialspace=True)
            records = 0
            surnames = 0
            for i in r:
                line = list(i)
                if not line:
                    continue
                if len(line) != 8:
                    raise BaseException('Some troubles with csv_file')
                surnames += self._process_cur_line(line)
                records += 1
                data.load(self._name, self._surname, self._points, self._mid_name,
                          self._cond, self._year, self._month, self._day)
        data.load_add_inf(records, surnames)

    def _process_cur_line(self, line):
        """
        :param line: current line, which was read from main_file
        :return: result of processing method _convert_fields() -- length of surname
        """
        return self._convert_fields(line)

    def _convert_fields(self, line):
        """
        :param line: current line, which was read from main_file
        divides current line into object fields and converts some values to integer
        :return: surname length of surname from current line
        """
        self._name = line[0]
        self._surname = line[1]
        self._points = int(line[2])
        self._mid_name = line[3]
        self._cond = line[4]
        self._year = int(line[5])
        self._month = int(line[6])
        self._day = int(line[7])
        return len(self._surname)
