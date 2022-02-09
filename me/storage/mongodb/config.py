import os
from datetime import datetime

BULK_LIMIT = 100
BULK_MIN = 1


s00 = f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PWD']}@127.0.0.1:27017"
# s00 = "mongodb://127.0.0.1:5000/?directConnection=true"

db_name = 'test'

mongo_to_python__ = {
    'string': str,
    'int': int,
    'double': float,
    'bool': bool,
    'array': list,
    'null': None,
    'date': datetime
}

mongo_type_check__ = {
    'string': lambda x: type(x) == mongo_to_python__['string'],
    'int': lambda x: type(x) == mongo_to_python__['int'],
    'double': lambda x: type(x) == mongo_to_python__['double'],
    'bool': lambda x: type(x) == mongo_to_python__['bool'],
    'array': lambda x: type(x) == mongo_to_python__['array'],
    'null': lambda x: x is None,
    'date': lambda x: type(x) == mongo_to_python__['date']
}

mongo_as_type__ = {
    'string': lambda x: mongo_to_python__['string'](x),
    'int': lambda x: mongo_to_python__['int'](x),
    'double': lambda x: mongo_to_python__['double'](x),
    'bool': lambda x: mongo_to_python__['bool'](x),
    'array': lambda x: mongo_to_python__['array'](x),
    'null': lambda x: x is None,
    'date': lambda x: datetime.strptime(x, '%Y-%m-%d')
}

mongo_to_pandas__ = {
    'string': 'object',
    'int': 'int64',
    'double': 'float64',
    'bool': 'bool',
    'array': 'object',
    'null': None,
    'date': 'datetime64[ns]'
}


def mongo_to_python(type_, mode=None):
    if type(type_) == list:
        return [mongo_to_python(i, mode) for i in type_]
    if mode == 'check':
        return mongo_type_check__[type_]
    if mode == 'convert':
        return mongo_as_type__[type_]
    return mongo_to_python__[type_]


