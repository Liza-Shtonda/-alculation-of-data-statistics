"""
Module of Shtonda Yelizaveta, contains class Information for storing data from .csv file
"""
import re
from datetime import date


class Information:
    """
    stores information from .csv file, contains nested class _Problem,
    stores list of _Problem objects and list of problems names
    """

    def __init__(self):
        """
        creates empty lists of _Problem objects, problems names, creates fields according to .json file
        """
        self.problems = []
        self.problems_names = []
        self.records_sum = 0
        self.surnames_length = 0

    def clear(self):
        """
        clears Information object -- lists of _Problem objects and problems names
        """
        self.problems = []
        self.problems_names = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :param exc_type: error class
        :param exc_val: error instance
        :param exc_tb: trace object
        in case of some error during processing .csv file clears Information object
        """
        if exc_type is not None:
            self.clear()

    def load_add_inf(self, record_sum, surnames_sum):
        """
        :param record_sum: quantity of records in .csv file
        :param surnames_sum: sum of lengths of surnames in .csv file
        update data in Information object
        """
        self.records_sum = record_sum
        self.surnames_length = surnames_sum

    def output(self, output_file, output_encoding):
        """
        :param output_file: relative path to file where information is outputed
        :param output_encoding: type of encoding of file where information is outputed
        opens file for outputing, calls _output() method, and prints 'OK' if there are no errors
        """
        print(f'output {output_file}: ', end='')
        with open(output_file, 'w', encoding=output_encoding) as f:
            self._output(f)
        print('OK')

    def _output(self, f):
        """
        :param f: opened file object
        iterates on _Problem objects and prints sorted information about all attempts of every needed problem
        """
        for i in self.problems:
            if i.good_problem():
                f.write(f'{i.cond}\t{i.attemptes_num}\t{i.good_attemptes_num}\t{i.good_attempt_percentage}\n')
                unsorted = []
                for j in i.students:
                    unsorted.append([j, j.surname, j.name, j.middle_name])
                unsorted.sort(key=lambda sur: (sur[1], sur[2], sur[3]))
                students = []
                for n in unsorted:
                    students.append(n[0])
                for j in students:
                    unsorted1 = []
                    for k in j.attempts:
                        unsorted1.append([k, k.percent, k.year])
                    unsorted1.sort(key=lambda sur: (-sur[1], sur[2]))
                    attempts = []
                    for b in unsorted1:
                        attempts.append(b[0])
                    for k in attempts:
                        f.write(f'\t{k.year}\t{j.surname}\t{j.name}\t{j.middle_name}\t{k.percent}\n')

    def load(self, name: str, surname: str, percent: int, middle_name: str, cond: str, year: int, month: int, day: int):
        """
        :param name: name of student
        :param surname: surname of student
        :param percent: point for attempt
        :param middle_name: middle_name of student
        :param cond: condition of problem
        :param year: year of attempt
        :param month: month of attempt
        :param day: day of attempt
        loads information about problem attempt of student, if there is not such a problem,
        creates _Problem object, otherwise in existing problem loads attempt data
        """
        found = self._find(cond)
        if found is None:
            return self._add(name, surname, percent, middle_name, cond, year, month, day)
        else:
            self.problems[found].load(name, surname, percent, middle_name, year, month, day)

    def _find(self, cond: str):
        """
        :param cond: condition of problem
        checks whether this problem exists
        :return: None if there is no problem, otherwise index of problem in problems list
        """
        if cond not in self.problems_names:
            return None
        else:
            index_ = self.problems_names.index(cond)
            return index_

    def _add(self, name, surname, percent, middle_name, cond, year, month, day):
        """
        :param name: name of student
        :param surname: surname of student
        :param percent: point for attempt
        :param middle_name: middle_name of student
        :param cond: condition of problem
        :param year: year of attempt
        :param month: month of attempt
        :param day: day of attempt
        creates _Problem object and add its to list of problems objects and to list of problems names
        :return: index of problem in list
        """
        obj = self._Problem(name, surname, percent, middle_name, cond, year, month, day)
        self.problems.append(obj)
        self.problems_names.append(cond)
        index_ = self.problems.index(obj)
        return self.problems[index_]

    class _Problem:
        """
        stores information about problem, contains nested class _Student,
        stores list of _Student objects and list of problems names
        """
        def __init__(self, name: str, surname: str, percent: int, middle_name: str, cond: str, year: int,
                     month: int, day: int):
            """
            :param name: name of student
            :param surname: surname of student
            :param percent: point for attempt
            :param middle_name: middle_name of student
            :param cond: condition of problem
            :param year: year of attempt
            :param month: month of attempt
            :param day: day of attempt
            creates empty lists of _Student objects and problems names, stores student data, calls load() method
            """
            self.students = []
            self.students_names = []
            self.name = name
            self.surname = surname
            self.percent = percent
            self.middle_name = middle_name
            self._check_cond(cond)
            self.cond = cond
            self.year = year
            self.month = month
            self.day = day
            self.load(name, surname, percent, middle_name, year, month, day)

        @staticmethod
        def _check_cond(cond):
            """
            :param cond: condition of problem
            checks accordance of condition format, in case of improper format raises error
            :return: True
            """
            pattern = re.compile(r'[-\w".,{}$+*\\)(%\]\[ ]{4,54}')
            if not re.fullmatch(pattern, cond):
                raise ValueError('something wrong with problem`s condition')
            return True

        def load(self, name: str, surname: str, percent: int, middle_name: str, year: int, month: int, day: int):
            """
            :param name: name of student
            :param surname: surname of student
            :param percent: point for attempt
            :param middle_name: middle_name of student
            :param year: year of attempt
            :param month: month of attempt
            :param day: day of attempt
            loads information about attempt of student of problem, if there is not such a student,
            calls add() method, otherwise in existing student loads attempt data by calling method _Student.load()
            :return:
            """
            found = self._find(name, surname, middle_name)
            if found is None:
                self._add(name, surname, percent, middle_name, year, month, day)
            else:
                self.students[found].load(percent, year, month, day)

        def _find(self, name: str, surname: str, middle_name: str):
            """
            :param name: name of student
            :param surname: surname of student
            :param middle_name: middle_name  of student
            finds student in list of students
            :return: None if there is not such a student, index of student in list otherwise
            """
            if [name, surname, middle_name] not in self.students_names:
                return None
            else:
                index_ = self.students_names.index([name, surname, middle_name])
                return index_

        def _add(self, name, surname, percent, middle_name, year, month, day):
            """
            :param name: name of student
            :param surname: surname of student
            :param percent: point for attempt
            :param middle_name: middle_name of student
            :param year: year of attempt
            :param month: month of attempt
            :param day: day of attempt
            creates _Student object, appends its to lists, finds index of this student in list
            :return: object of student
            """
            obj = self._Student(name, surname, percent, middle_name, year, month, day)
            self.students.append(obj)
            self.students_names.append([name, surname, middle_name])
            index_ = self.students.index(obj)
            return self.students[index_]

        def _attempt_num(self):
            """
            counts quantity of attempts, done by this student in one this problem
            :return: quantity of these attempts
            """
            an = 0
            for i in self.students:
                an += i.attempts_num
            self.attemptes_num = an
            return an

        def _good_attempt_num(self):
            """
            counts quantity of good attempts, done by this student in one this problem (attempt is successful, if
            gained points are 60 or more)
            :return: quantity of these good attempts
            """
            gan = 0
            for i in self.students:
                gan += i.good_attempts_num
            self.good_attemptes_num = gan
            return gan

        def _good_attempt_percentage(self):
            """
            :return: percent of good attempts to all attempts
            """
            return round((self._good_attempt_num() / self._attempt_num()) * 100)

        def good_problem(self):
            """
            creates object field of good attempts percentage
            :return: True if all attempts are good, False otherwise
            """
            self.good_attempt_percentage = self._good_attempt_percentage()
            return self.attemptes_num == self.good_attemptes_num

        class _Student:
            """
            stores information about student, contains nested class _Attempt,
            stores list of _Attempt objects and list of attempts date
            """
            def __init__(self, name: str, surname: str, percent: int, middle_name: str,
                         year: int, month: int, day: int):
                """
                :param name: name of student
                :param surname: surname of student
                :param percent: point for attempt
                :param middle_name: middle_name of student
                :param year: year of attempt
                :param month: month of attempt
                :param day: day of attempt
                creates empty lists of _Attempt objects and attempts dates,
                stores student and attempt data, calls load() method
                """
                self.attempts = []
                self.attempts_names = []
                self._check_name(name)
                self.name = name
                self._check_surname(surname)
                self.surname = surname
                self.percent = percent
                self._check_middle_name(middle_name)
                self.middle_name = middle_name
                self.year = year
                self.month = month
                self.day = day
                self.attempts_num = 0
                self.good_attempts_num = 0
                self.good_attempts_percentage = 0
                self.load(percent, year, month, day)

            @staticmethod
            def _check_name(name):
                """
                :param name: name of student
                checks accordance of name format, in case of improper format raises error
                :return: True
                """
                pattern_digit = re.compile(r'\d')
                pattern = re.compile(r'\b[-\w` ]{0,26}\b')
                digit = re.search(pattern_digit, name)
                if digit is None:
                    if not re.fullmatch(pattern, name):
                        raise ValueError('something wrong with student`s name')
                    return True
                else:
                    raise ValueError('something wrong with student`s name')

            @staticmethod
            def _check_surname(surname):
                """
                :param surname: surname of student
                checks accordance of surname format, in case of improper format raises error
                :return: True
                """
                pattern_digit = re.compile(r'\d')
                pattern = re.compile(r'\b[-\w` ]{0,25}\b')
                digit = re.search(pattern_digit, surname)
                if digit is None:
                    if not re.fullmatch(pattern, surname):
                        raise ValueError('something wrong with student`s name')
                    return True
                else:
                    raise ValueError('something wrong with student`s name')

            @staticmethod
            def _check_middle_name(middle_name):
                """
                :param middle_name: middle_name of student
                checks accordance of middle_name format, in case of improper format raises error
                :return: True
                """
                pattern_digit = re.compile(r'\d')
                pattern = re.compile(r'\b[-\w` ]{0,30}\b')
                digit = re.search(pattern_digit, middle_name)
                if digit is None:
                    if not re.fullmatch(pattern, middle_name):
                        raise ValueError('something wrong with student`s name')
                    return True
                else:
                    raise ValueError('something wrong with student`s name')

            def load(self, percent: int, year: int, month: int, day: int):
                """
                :param percent: points of attempt
                :param year: year of attempt
                :param month: month of attempt
                :param day: day of attempt
                calls find() method
                :return: calls add() method
                """
                self._find(year, month, day)
                return self._add(percent, year, month, day)

            def _find(self, year, month, day):
                """
                :param year: year of attempt
                :param month: month of attempt
                :param day: day of attempt
                finds attempt in list of attempt dates
                :return: None if there is not such an attempt, raises error otherwise
                """
                if [year, month, day] in self.attempts_names:
                    raise ValueError('Attempt has already been added')
                return None

            def _add(self, percent, year, month, day):
                """
                :param percent: points of attempt
                :param year: year of attempt
                :param month: month of attempt
                :param day: day of attempt
                creates _Attempt object, appends its to lists, finds index of attempt in list,
                update quantity of attempts and good attempts
                :return: object of attempt
                """
                obj = self._Attempt(percent, year, month, day)
                self.attempts.append(obj)
                self.attempts_names.append([year, month, day])
                index_ = self.attempts.index(obj)
                self.attempts_num += 1
                if self.good_attempt(percent):
                    self.good_attempts_num += 1
                return self.attempts[index_]

            @staticmethod
            def good_attempt(percent):
                """
                :param percent: points of attempt
                :return: True if attempt is good (60 points or more), False otherwise
                """
                return percent >= 60

            class _Attempt:
                """
                stores information about attempt
                """
                def __init__(self, percent: int, year: int, month: int, day: int):
                    self._check_percent(percent)
                    self.percent = percent
                    self._check_year(year)
                    self.year = year
                    self._check_month(month)
                    self.month = month
                    self._check_day(day)
                    self.day = day

                @staticmethod
                def _check_percent(percent):
                    """
                    :param percent: points of attempt
                    checks accordance of percent format, in case of improper format raises error
                    :return: True
                    """
                    if not 0 <= percent <= 100:
                        raise ValueError('something wrong with points')
                    return True

                @staticmethod
                def _check_year(year):
                    """
                    :param year: year of attempt
                    checks accordance of year format, in case of improper format raises error
                    :return: True
                    """
                    if not 2001 <= year or not len(str(year)) == 4:
                        raise ValueError('something wrong with year')
                    return True

                @staticmethod
                def _check_month(month):
                    """
                    :param month: month of attempt
                    checks accordance of month format, in case of improper format raises error
                    :return: True
                    """
                    if not 0 < month < 13:
                        raise ValueError('something wrong with month')
                    return True

                def _check_day(self, day):
                    """
                    :param day: day of attempt
                    checks accordance of day format, in case of improper format raises error
                    :return: date if it is proper, raises error otherwise
                    """
                    return date(self.year, self.month, day)
