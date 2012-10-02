# -*- coding: utf-8 -*-

from decimal import Decimal

# Types and syntax are already checked
# syntax is expected allright cf input validators

def _coerce(typename, value):
    if typename == 'S' or typename == 'B':
        return value
    if typename == 'SS' or typename == 'BS':
        return set(value)
    if typename == 'N':
        return Decimal(value)
    if typename == 'NS':
        return set(map(Decimal, value))

def _parse_elem(elem):
    typename, value = elem.items()[0]
    value = _coerce(typename, value)
    return typename, value

#Types restrictions are performed by the input validators


# Common comparison operators

TYPEMSG1 = "Types '{}' is not compatible in test {}"
TYPEMSG2 = "Types '{}' and '{}' are not compatible in test {}"
TYPEMSG3 = "Types '{}', '{} and '{}' are not compatible in test {}"

def eq(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue == rvalue

def le(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue <= rvalue

def lt(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue < rvalue

def ge(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue >= rvalue

def gt(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue > rvalue

def begins_with(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue.startswith(rvalue)

def between(target, rule1, rule2):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype1, rvalue1 = _parse_elem(rule1)
    rtype2, rvalue2 = _parse_elem(rule2)
    if not (itype == rtype1 == rtype2):
        raise TypeError(TYPEMSG3.format(itype, rtype1, rtype2, __name__))
    return ivalue >= rvalue1 and ivalue <= rvalue2

# Comparisons specific to Scan

def null(target):
    return target is None

def not_null(target):
    return not null(target)

def contains(target, rule):
    if target is None: return False
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)

    if itype[0] != rtype or itype == u"N":
        raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return rvalue in ivalue

def not_contains(target, rule):
    return not contains(target, rule)

def in_test(target, *rules):
    if target is None: return False
    itype, ivalue = _parse_elem(target)

    if len(itype) != 1:
        raise TypeError(TYPEMSG1.format(itype, __name__))

    return target in rules

# workaround to use a function with a built-in name
import sys
setattr(sys.modules[__name__], 'in', in_test)