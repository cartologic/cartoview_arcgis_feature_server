__author__ = 'Ahmed Nour Eldeen'

from pyparsing import Word, alphas, alphanums, Forward, Keyword, oneOf, quotedString, ZeroOrMore, Group, Optional, \
    OneOrMore

def parse_query(query_str):
    """
    parse search query which  esri uses in ArcGIS Portal.
    """
    # TODO: handle search by text (parser does not work if the query has text keywords).
    # TODO: must be tested and enhanced to meet all queries requirements.
    identifier = Word(alphas, alphanums+"_$").setName("identifier")
    where_expression = Forward()
    and_ = Keyword("AND", caseless=True)
    or_ = Keyword("OR", caseless=True)
    bin_op = oneOf(":", caseless=True)
    right_side_val = quotedString | Word(alphanums)
    where_condition = Group(
        (Optional('-')+Optional('+')+identifier + bin_op + right_side_val) |
        ("(" + where_expression + ")")
    )
    where_expression << where_condition + ZeroOrMore((and_ | or_) + where_expression)
    query = where_expression
    return query.parseString(query_str)