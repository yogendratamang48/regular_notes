import re
import sys
import json

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
            ]
    for pass_regex in pass_regexes:
        id_numbers = re.findall(pass_regex, raw_string)
        id_numbers = [_.strip() for _ in id_numbers if _.strip()]
        if id_numbers:
            return id_numbers
    return [raw_string]

def extract_list(raw_string):
    '''
    extract plain list of string from string like-
    (1) Abdul (2) Haji ==> ["Abdul", "Haji"]
    '''
    _list = []
    #raw_list = re.findall(r'\(\d{1,}\)[A-Za-z,\-.0-9\s]+', raw_string)
    raw_list = re.split(r'(?:^|\s|-)\(?[\da-e]\)\s', raw_string)
    if not raw_list:
        raw_list.append(raw_string)
    for _item in raw_list:
        _raw = re.sub(r'\(\d{1}\)','',_item)
        if _raw.strip() != '':
            _list.append(_raw.strip())
    return list(_list)

def extract_date(raw_string, mode=None):
    '''
    '''
    date_regexes = [
            # issued on 16 Nov 1989
            r'issued\s?(?:on)?\s+(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
            r'[I|i]ssued\s?(?:on)?\s?(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
            r'[I|i]ssued\s?(?:on)?\s?(\d{1,2}[./-]+\d{1,2}[./-]+\d{4})'
            r'[I|i]ssued\s?(?:on)?\s?(\d{1,2}[./-]+\d{1,2}[./-]+\d{4})'
            # issued on 16 9.12.2003
                ]
    if mode == "exp":
        date_regexes = [
                # issued on 16 Nov 1989
                r'[V|v]alid\s?(?:[U|u]ntil)?\s+(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
                r'[E|i]xpir[eds]+\s?(?:on)?\s?(\d{1,2}\s+(?:\w+)\s+\d{1,4})',
                r'[E|i]xpir[eds]+\s?(?:on)?\s?(\d{1,2}[/-]+\d{1,2}[/-]+\d{4})',
                    ]
    _date = None
    for pattern in date_regexes:
        pattern_out = re.findall(pattern, raw_string)
        if pattern_out:
            try:
                _date = nlp.resolve_date_range(pattern_out[0])
                return _date
                break
            except:
                pass
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
    counter = 1
    for _id in check_format(sys.argv[1]):
        print("====== ", counter)
        jdata = json.dumps(_id, ensure_ascii=False, indent=2)
        print(jdata)
        counter += 1



