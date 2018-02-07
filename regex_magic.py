#!/usr/bin/python3
'''
I will use '|' as OR operator, instead of '+' in order to use '+' for Kleene plus operator
'''
import re
from collections import OrderedDict
from copy import copy

class InvalidNewTerminalIndex(Exception):
    pass

REGEX_OPERATORS = '+*|()'

def sigma_without(sigma, *letters):
    result = copy(sigma)
    for letter in letters:
        result.remove(letter)
    expr = '(' + ' | '.join(x for x in result) + ')'
    return expr

def get_expr(sigma, expr):
    return expr

replaces = {
    'a': [sigma_without, ['a']],
    'a|b': [sigma_without, ['a', 'b']],
    '(': [get_expr, ['(']],
    ')': [get_expr, [')']],
}

def translate_to_current_terminals(expr, new_terminals):
    '''
    This function assumes that new_terminals is ordered by the display order in the regex expr
    '''
    new_expr = ''
    for i in range(len(expr)):
        #get current letter which is not operator
        cur = expr[i]
        if cur in REGEX_OPERATORS:
            new_expr += cur
            continue
        assert(len(cur) == 1)

        #replace with the new terminal which matches the letter (a=0, b=1..)
        new_terminal_index = ord(cur) - ord('a')
        if new_terminal_index >= len(new_terminals):
            raise InvalidNewTerminalIndex('Invalid new_terminal_index: ', new_terminal_index)
        new_expr += new_terminals[new_terminal_index]
    return new_expr

def negate_regex(sigma, expr):
    '''
    param expr: a regex expression
    param sigma: list of all available terminals/signs/letters in the language
    '''
    whole_new_expr = ''
    expr = expr.replace(' ', '')
    # import ipdb; ipdb.set_trace()
    index = 0
    ordered_keyes = sorted(replaces.keys(), key=len, reverse=True)

    while index < len(expr):
        did_replace = False
        #start parse from the longest item in replaces to the shortest
        for key in ordered_keyes:
            sub_expr = expr[index:index + len(key)]
            if len(sub_expr) != len(key):
                #they don't match in the length
                continue

            sub_expr_terminals = [x for x in sub_expr if x not in REGEX_OPERATORS]
            value = replaces[key]
            func, params = value
            #translate key
            try:
                new_key = ''.join(translate_to_current_terminals(x, sub_expr_terminals) for x in key)
            except InvalidNewTerminalIndex as err:
                continue
            if sub_expr != new_key:
                #they don't match
                continue

            #replace with the inverse
            new_params = [translate_to_current_terminals(x, sub_expr_terminals) for x in params]
            new_expr = func(sigma, *new_params)

            index += len(key)
            whole_new_expr += new_expr
            did_replace = True
            break

        if not did_replace:
            raise Exception('Failed to find element to replace with')
    return whole_new_expr

def intersect_regex(sigma, *exprs):
    result = None
    negated_exprs = '|'.join('(%s)' % (negate_regex(sigma, x)) for x in exprs)
    print(negated_exprs)
    # result = negate_regex(sigma, negated_exprs)
    return result
