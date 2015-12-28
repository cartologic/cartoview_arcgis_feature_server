__author__ = 'kamal'
from .constants import *
from .utils import DynamicObject
from pyparsing import *


def get_boolean(val, default):
    if val is None or val == "":
        return default
    try:
        val = int(val)
        return val != 0
    except:
        pass

    if val.lower() == 'true':
        return True
    elif val.lower() == 'false':
        return False

    return default


def parse(request):
    """
    extracts the valid query params from the request
    @param request: the request object
    @return: dict with all valid arcgis rest rquest parameters
    """
    params = {}

    def get_params(obj):
        if obj:
            for key, val in obj.items():
                if key.lower() in LAYER_QUERY_PARAMS_MAP.keys():
                    value = str(val)
                    if value != "":
                        params[key.lower()] = str(val)

    get_params(request.GET)
    get_params(request.POST)
    params = DynamicObject(params)
    params.returngeometry = get_boolean(params.returngeometry, True)
    params.returnidsonly = get_boolean(params.returnidsonly, False)
    params.returncountonly = get_boolean(params.returncountonly, False)
    # parse where clause and wrap column names in double quotes to work with postgres
    if params.where is not None and params.where != '':
        params.where = as_string(parse_where(params.where))
    return params


# arcgis server supported functions
functions = ["CURRENT_TIMESTAMP", "CURRENT_DATE", "CHAR_LENGTH", "SUBSTRING",
             "TRUNCATE", "CEILING", "EXTRACT", "CONCAT", "ROUND", "LOWER",
             "UPPER", "FLOOR", "LOG10", "POWER", "ABS", "LOG"]
# Binary operators.
binary_operators = ['=', '<>', '<', '<=', '>', '>=', 'LIKE']


def add_double_quotes(s, l, t):
    if t[0].upper() not in functions:
        return '"%s"' % t[0]
    return t[0]


def parse_where(expression_str):
    arithSign = Word("+-", exact=1)
    realNum = Combine(Optional(arithSign) + (Word(nums) + "." + Optional(Word(nums)) | ("." + Word(nums))))
    intNum = Combine(Optional(arithSign) + Word(nums))
    ident = Word(alphas + "_", alphanums + "_").setParseAction(add_double_quotes)
    binary_operators_def = oneOf(' '.join(binary_operators), caseless=True)
    logical_def = oneOf('and or', caseless=True)

    function_parameter = realNum | intNum | quotedString | ident
    expression = (ident + Optional("(" + Group(delimitedList(function_parameter, ',')) + ")")) | realNum | intNum

    # where clause
    where_clause = Forward()
    standard_condition = (
        expression.setResultsName('lfs') +
        binary_operators_def.setResultsName("operator") +
        (quotedString | Word(nums) | expression)
        .setResultsName("value")
    ).setResultsName("condition")

    # nested clause
    nested_condition = (
        Suppress("(") + where_clause + Suppress(")")
    ).setResultsName("nested")

    condition = Group(standard_condition | nested_condition)
    where_clause << (condition + ZeroOrMore(logical_def + condition))
    query = where_clause
    return query.parseString(expression_str)


def as_string(tokens):
    out = ""
    for token in tokens:
        if not isinstance(token, basestring):
            out += as_string(token)
        else:
            out += token + " "
    return out
