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
        return set(map(value, Decimal))

def _parse_elem(elem):
    typename, value = elem.items()[0]
    value = _coerce(typename, value)
    return typename, value

#Types restrictions are performed by the input validators

TYPEMSG2 = "Types {} and {} are not copatible in test {}"
TYPEMSG3 = "Types {}, {} and {} are not copatible in test {}"

def eq(target, rule):
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue == rvalue

def le(target, rule):
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue <= rvalue

def lt(target, rule):
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue < rvalue

def ge(target, rule):
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue >= rvalue

def gt(target, rule):
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue > rvalue

def begins_with(target, rule):
    itype, ivalue = _parse_elem(target)
    rtype, rvalue = _parse_elem(rule)
    if itype != rtype: raise TypeError(TYPEMSG2.format(itype, rtype, __name__))
    return ivalue.startswith(rvalue)

def between(target, rule1, rule2):
    itype, ivalue = _parse_elem(target)
    rtype1, rvalue1 = _parse_elem(rule1)
    rtype2, rvalue2 = _parse_elem(rule2)
    if not (itype == rtype2 == rtype2):
        raise TypeError(TYPEMSG3.format(itype, rtype1, rtype2, __name__))
    return ivalue >= rvalue1 and ivalue <= rvalue2
