from me.storage import datalist

type_to_table = {
    datalist.Data.TXs.value: 'transactions'
}

type_to_schema = {
    datalist.Data.TXs.value: 'me_banking'
}


psql_to_python__ = {
    'integer': int,
    'text': str,
    'real': float,
    'boolean': bool,
    'ARRAY': str,
    'timestamp without time zone': str
}

psql_type_check__ = {  # TODO
    'integer': lambda x: type(x) == psql_to_python__['integer'],
    'text': lambda x: type(x) == psql_to_python__['text'],
    'real': lambda x: type(x) == psql_to_python__['real'],
    'boolean': lambda x: type(x) == psql_to_python__['boolean'],
    'ARRAY': lambda x: type(x) == psql_to_python__['ARRAY'],
    'timestamp without time zone': lambda x: type(x) == psql_to_python__['timestamp without time zone'],
}

psql_as_type__ = {  # TODO
    'integer': lambda x: psql_to_python__['integer'](x),
    'text': lambda x: psql_to_python__['text'](x),
    'real': lambda x: psql_to_python__['real'](x),
    'boolean': lambda x: psql_to_python__['boolean'](x),
    'ARRAY': lambda x: psql_to_python__['ARRAY'](x),
    'timestamp without time zone': lambda x: psql_to_python__['timestamp without time zone'](x),
}


def psql_to_python(type_, mode=None):
    if type(type_) == list:
        return [psql_to_python(i, mode) for i in type_]
    if mode == 'check':
        return psql_type_check__[type_]
    if mode == 'convert':
        return psql_as_type__[type_]
    return psql_to_python__[type_]
