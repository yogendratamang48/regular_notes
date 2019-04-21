import re
import sys
import json

LIST_NOISES = [
'',
'passport no', 
'passport no',
'bosnia and herzegovina passport number',
'qatari passport number',
'jordanian passport numbers',
]
def extract_passport(raw_string):
    '''
    '''
    if len(raw_string.strip().split(' ')) == 1:
        return [raw_string]
    pass_regexes = [
        r'[Nn]o|[Nn]o[:.]|[Nn]umber\s+(\w+)',
        r'Code\s+(\w+)$',
        r'(?:^|\s+)([A-Z]+\d{2,}[A-Z]+?)',
        r'\w?\d{5,}\w?',
        r'[N|n]umber:?\s([A-Z0-9\-]+)',
            ]
    for pass_regex in pass_regexes:
        id_numbers = re.findall(pass_regex, raw_string)
        id_numbers = [_.strip() for _ in id_numbers if _.strip()]
        if id_numbers:
            return [id_numbers[0]]
    return [raw_string]

def extract_list(raw_string):
    '''
    extract plain list of string from string like-
    (1) Abdul (2) Haji ==> ["Abdul", "Haji"]
    '''
    _list = []
    #raw_list = re.findall(r'\(\d{1,}\)[A-Za-z,\-.0-9\s]+', raw_string)
    list_regexes = [
            r'\(\d{1,2}\)\s',
            # . And 
            r'\.\sAnd\s',
            r'\([a-e]\)',
            r'\([A-E]\)',
            r'(?:^|\s|-)\(?[\da-e]\)\s',
            r'Yemeni passport number',
            ]
    for _p in list_regexes:
        raw_list = re.split(_p, raw_string)
        if len(raw_list) > 1:
            break
    if not raw_list:
        # CAses of "4546454 and 56794730"
        raw_list.append(raw_string)
    for _item in raw_list:
        _raw = re.sub(r'\(\d{1}\)','',_item)
        if _raw.lower().strip() not in LIST_NOISES:
            _list.append(_raw.strip())
    return list(_list)

def extract_date(raw_string, mode=None):
    '''
    '''
    date_regexes = [
            # issued on 16 Nov 1989
            r'issued\s?(?:on)?\s+(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
            r'[I|i]ssued\s?(?:on)?\s?(\d{1,2}\s+[A-Za-z\.]+\s+\d{1,4})',
            r'[I|i]ssued:?\s?(?:on)?\s?(\d{1,2}[./-]+\d{1,2}[./-]+\d{4})',
            # issued on 16 9.12.2003
            # date of issue: 24.5.2015
            r'issue:\s?(\d{1,2}\.\d{1,2}\.\d{4})',
            # date of issue 24 November 2015
            r'issue:?\s?(\d{1,2}\s[A-Za-z\.]+\s+\d{4})',
            # valid 21/03/2016
            # valid 13.11.2013
            r'valid\s?(\d{1,2}[./-]+\d{1,2}[./-]+\d{4})',
            # valid from 15.4.2011 until 14.4.2016
            r'valid\sfrom\s?(\d{1,2}[./-]+\d{1,2}[./-]+\d{4})',
            # (approximately issued in 2009)
            r'approximately issued in\s(\d{4})',
                ]
    if mode == "exp":
        date_regexes = [
                # issued on 16 Nov 1989
                r'[V|v]alid\s?(?:[U|u]ntil)?\s+(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
                # expires on 6 june 2013
                r'[E|e]xpir[edsing]+\s?(?:on)?\s?(\d{1,2}[-/\s]+[A-Za-z\.]+[-/\s]+\d{4})',
                # expiration date: 3.6.2016
                r'[E|e]xpiration:?\s(?:date)?:?\s?(?:on)?\s?(\d{1,2}[-/\s\.]\d{1,2}[-/\s\.]+\d{4})',
                # expiration date 25 Feb. 2026
                r'[E|e]xpiration (?:date)?:?\s?(?:on)?\s?(\d{1,2}[-/\s]+[A-Za-z\.]+[-/\s]+\d{4})',
                # expired 23.09.2023
                # expires 23.09.2023
                r'[E|e]xpir[eds]+:?\s?(?:on)?\s?(\d{1,2}[-/\.]+\d{1,2}[-/\.]+\d{4})',
                r'[E|e]xpir[eds]+\s?(?:on)?\s?(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
                # date of expiry: 23.5.2021
                # expiring 03/05/2022
                r'expir[ingy]+:?\s?(\d{1,2}[\./]+\d{1,2}[\./]+\d{4})',
                # date of expiry 24 November 2015
                r'expiry:?\s?(\d{1,2}\s[A-Za-z\.]+\s+\d{4})',
                # expiry date of 24 November 2015
                r'expiry date (?:of)?\s?(\d{1,2}\s[A-Za-z\.]+\s+\d{4})',
                # valid from 15.4.2011 to 14.4.2016
                r'valid\sfrom\s?\d{1,2}[./-]+\d{1,2}[./-]+\d{4}\s+to\s+(\d{1,2}[./-]+\d{1,2}[./-]+\d{4})',
                # valid until 4.2.2019.
                r'until\s?(\d{1,2}\.\d{1,2}\.\d{4})',
                # expires 23.09.2023
                # expiry date
                # Date of Expiration: 6.4.2016
                    ]
    _date = None
    for pattern in date_regexes:
        pattern_out = re.findall(pattern, raw_string)
        if pattern_out:
            return pattern_out
    return _date


def check_format(mode):
    '''
    '''
    filename = 'pass.txt'
    if mode.lower().strip() == 'ni':
        filename = 'nis.txt'
    raw_passes = open(filename).read().split('\n')
    for i, raw_pass in enumerate(raw_passes):
        raw_pass_list = extract_list(raw_pass)
        for raw_pass in raw_pass_list:
            numbers = extract_passport(raw_pass)
            if numbers:
                issue_date = extract_date(raw_pass)
                expire_date = extract_date(raw_pass, mode="exp")
                for number in numbers:
                    _id = {}
                    _id['type'] = 'pass'
                    _id['number'] = number
                    _id['issue_date'] = issue_date
                    _id['expire_date'] = expire_date
                    _id['index'] = i
                    yield _id


if __name__ == '__main__':
    '''
    '''
    for _id in check_format(sys.argv[1]):
        print("====== ", (_id['index']+1))
        jdata = json.dumps(_id, ensure_ascii=False, indent=2)
        print(jdata)



