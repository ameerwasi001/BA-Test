import sys
import os
import helpers
import re
import importlib

def get_the_getters(given_list, getter='GET'):
    getters = [i for i, x in enumerate(given_list) if x == getter]
    for g in getters:
        print('getters: ', given_list[g], g, end=', ')
    if getters != []:
        for getter in getters:
            getter_var = getter+1
            getter_val = given_list[getter_var]
            value = getattr(helpers, given_list[getter])(given_list[getter_var])
            print('value: ', value)
            given_list[getter_var] = value
            del given_list[getter]
#            given_list = [value if given == getter_val else given for given in given_list]
#            print('pt', given_list)
            return given_list
    else:
        return given_list

def remove_space_or_not(part):
    while part.startswith(' '):
        part = part[1:]
    while part.endswith(' '):
        part = part[:-1]
    if (part.startswith('"') and part.endswith('"')) or (part.startswith("'") and part.endswith("'")):
        print(part)
        part = part[1:-1]
        print(part)
    else:
        part = part.replace(" ", '')
    return part

def get_args(dsl_args, shouldEqualBeSeprated=True, seprationOperator='->'):
    """return args, kwargs"""
    args = []
    kwargs = {}
    for index, dsl_arg in enumerate(dsl_args):
        if str(dsl_arg).__contains__('GET'):
            getter = 'GET'
        elif str(dsl_arg).__contains__('EVALUATE'):
            getter = 'EVALUATE'
    
        if str(dsl_arg).__contains__("GET") or str(dsl_arg).__contains__('EVALUATE'):
            k, v = dsl_arg.split(seprationOperator, 1)
            k = remove_space_or_not(k)
            v = remove_space_or_not(v)
            kwargs[k] = getattr(helpers, getter)(dsl_args[index+1])
            del dsl_args[index+1]
        else:
            if seprationOperator in str(dsl_arg) and shouldEqualBeSeprated:
                k, v = dsl_arg.split(seprationOperator, 1)
                kwargs[remove_space_or_not(k)] = remove_space_or_not(v)
            else:
                args.append(dsl_arg)
    return args, kwargs

def get_help():
    print(
        """
Hello there! this is an opensource DSL for browser automation made for testers who want a simple interface for testing web applications. It calls functions from from helpers file and to know what those functions exactly are, you may visit the documentation of this language at Github,to assign parameters to a function you use '=>' and to assign parameters with names you use something like 'enter->false' and all paramenetersmust be seprated by ','. Thanks for reading along and to to know the exact syntax with examples, you should visit our GitHub because we do have some documentation there.\n...Were you a developer, thinking this might help in providing your testers with an easier to use interface, then it's for you too because you can write your own python functions in 'extensions.py' and they will be directly accessible in this language"""
        )

if len(sys.argv) != 2:
    print('usage 1: %s <src.dsl>' % sys.argv[0])
    print('usage 2: %s help=<module name>' % sys.argv[0])
    sys.exit(1)

def getModules(path):
    path=os.path.dirname(os.path.abspath(path))
    path=path.replace('\\', '/')
    print(path)
    return path

sys.path.insert(0, getModules(sys.argv[1]))

if sys.argv[1].startswith('help'):
    get_help()
else:
    with open(sys.argv[1], 'r') as file:
        line_no = 0
        file = file.read()
        lines = file.split("\n")
        while line_no<len(lines):
            line = lines[line_no].strip()
            if not line or line[0] == '#':
                line_no += 1
                continue
            parts = line.split()
            parts = re.split('=>|,', line)
            for index, part in enumerate(parts):
                if not part.__contains__('=' if parts[0] == 'SET' else '->'):
                    parts[index] = remove_space_or_not(part)
            parts = get_the_getters(parts, getter='GET')
            parts = get_the_getters(parts, getter='EVALUATE')
            parts = [x for x in parts if not x == 'GET']
            parts = [x for x in parts if not x == 'EVALUATE']
            seprationOperator = '=' if parts[0] == 'SET' else '->'
            args, kwargs = get_args(parts[1:], shouldEqualBeSeprated=True, seprationOperator=seprationOperator)

            print(kwargs, '/', args)
            getattr(helpers, parts[0])(*args, **kwargs)
            line_no += 1
