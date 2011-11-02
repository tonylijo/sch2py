import lispio
import sys
identifiers = []
premitives = ['+','-','*','/','=','<','>','==','or','and','obj','car','cdr']
algibraic = ['+','-','*','/','=','<','>','==','or','and']
tab = '  '
tab_count = 0

def print_tab(count):
    if count == 0:
        pass
    else :
        for i in range(count):
            print tab,
        

def isstring(s): return (type(s) == type(''))
def isnum(s): return (type(s) == type(0.0))
def issymbol(s): return isstring(s)

def analyse(exp):
    if isnum(exp):
        sys.stdout.write(str(exp))
    elif isvariable(exp):
        sys.stdout.write(exp)
    elif isstring(exp):
        sys.stdout.write(exp)
    elif isquoted(exp):
        analyse_quote(text_of_expr(exp))
    elif isempty(exp):
        sys.stdout.write("not ")
        analyse(exp[1:][0])
    elif isstr(exp):
        print "'",exp[1:]
    elif isimport(exp):
        sys.stdout.write("import ")
        analyse(exp[1:][0])
        print ""
    elif isreturn(exp):
        sys.stdout.write("return ")
        analyse(exp[1:][0])
    elif isdisplay(exp):
        sys.stdout.write("print ")
        analyse(exp[1:][0])
    elif isassignment(exp):
        assign_analyser(exp)
    elif isif(exp):
        to_py_if(exp)
    elif isdefine(exp):
        define_analyser(exp)
        print ""
    elif is_proc_call(exp):
        to_py_proc(proc_name(exp),proc_par(exp))
    elif isbegin(exp):
        analyse_sequence(begin_body(exp))
    elif isprimitive(exp):
        x = operator(exp)
        y = operands(exp)
        apply(x,y)
    else :
        print "error expression:",exp


def selfeval(exp):
    if isnum(exp):
        return True
    elif isstring(exp):
        return True
    else: return False

def isvariable(exp):
    return issymbol(exp)


def isassignment(exp):
    return istaggedlist(exp,'set!')

def isif(exp):
    return istaggedlist(exp,'if')

def isreturn(exp):
    return istaggedlist(exp,'return')

def isempty(exp):
    return istaggedlist(exp,'empty?')

def iscond(exp):
    return istaggedlist(exp,"cond")

def isimport(exp):
    return istaggedlist(exp,"import")

def isdisplay(exp):
    return istaggedlist(exp,"display")

def isstr(exp):
    return istaggedlist(exp,"str")

def isquoted(exp):
    return istaggedlist(exp,"quote")

def is_proc_call(exp):
    return exp[0] in identifiers

def isbegin(exp):
    return istaggedlist(exp,'begin')

def isdefine(exp):
    return istaggedlist(exp,'define')

def algibraic_exp(exp):
    return (exp in algibraic)

def isprimitive(exp):
    if (exp[0] in premitives):
        return True
    else : return False

####text of
def text_of_expr(exp):
    return exp[1:][0]

####definition
def def_var(exp):
    if type(exp[1:][0]) == type([]):
        if issymbol(exp[1:][0]):
            return exp[1:][0]
        else:
            return exp[1:][0][0]
    if type(exp[1:][0]) == type(''):
        return exp[1:][0]

def def_par(exp):
    if issymbol(exp[1:][0]):
        return []
    else : 
        return exp[1:][0][1:]
def def_body(exp):
    return exp[1:][1:]

##application
def operator(exp):
    return exp[0]

def operands(exp):
    return exp[1:]

def no_operands(exp):
    return exp == []

def first_operands(exp):
    return exp[0]

def rest_of_operands(exp):
    return exp[1:]

##body_begin
def begin_body(exp):
    return exp[1:]

##if
def if_cond(exp):
    return exp[1:][0]

def if_consequent(exp):
    return exp[1:][1:][0]

def if_alternate(exp):
    if not exp[1:][1:][1:] == []:
        return exp[1:][1:][1:][0]
    else:
        return False
####assignment
def assignment_var(exp):
    return exp[1:][0]

def assigment_body(exp):
    return exp[1:][1:][0]

####proc_call 
def proc_name(exp):
   return exp[0]

def proc_par(exp):
    return exp[1:]

####taggedlist
def istaggedlist(exp,tag):
    if type(exp) == type([]):
        if exp[0] == tag:
            return True
        else:
            return False
        
####analyse-quote
def analyse_quote(exp):
    if type(exp) == type([]):
        to_py_array(exp)
    else :
        analyse(exp)

####apply
def apply(proc,args):
    if algibraic_exp(proc):
        to_py_algibraic(proc,args)
    elif proc == 'car':
        return args[0]
    elif proc == 'cdr':
        return args[1:]
    elif proc == 'obj':
        to_py_obj(args)
    else:
        print "Error"

####analyse_sequence
def analyse_sequence(exp):
    print_tab(tab_count)
    if exp[1:] == []:
        analyse(exp[0])
        print ""
    else :
        analyse(exp[0])
        analyse_sequence(exp[1:])

### analyse_quote
def analyse_quote(exp):
    if type(exp) == type([]):
        to_py_array(exp)
    else:
        analyse(exp)

####algibra
def alg(l,proc,fo,lr):
    if l:
        sys.stdout.write('(')
        alg(l[1:],proc,fo,lr[1:])
        sys.stdout.write(' '+proc+' ')
        analyse(lr[0])
        sys.stdout.write(')')
    else:
        analyse(fo)

def to_py_algibraic(proc,args):
    lr=[x for x in args]
    lr.reverse()
    alg(args[1:],proc,args[0],lr)

#assign_analyser
def assign_analyser(exp):
    print_tab(tab_count)
    print assignment_var(exp),"=",
    analyse(assigment_body(exp))

def arg_list(l):
    if l[1:] == []:
       return analyse(l[0])
    else :
        analyse(l[0])
        sys.stdout.write(',')
        return arg_list(l[1:])

def to_py_obj(arguments):
    analyse(arguments[0])
    temp(arguments[1:])

def temp(arg):
    if arg == []:
        print "",
    elif '$' == arg[0]:
        print "("+")",
        temp(arg[1:])
    elif '$l' == arg[0]:
        sys.stdout.write('(')
        arg_list(arg[1:][0])
        sys.stdout.write(')')
    else:
        sys.stdout.write('.')
        analyse(arg[0])
        temp(arg[1:])

#proc-call-analyser
def to_py_proc(name,par):
    sys.stdout.write(name)
    sys.stdout.write('(')
    arg_list(par)
    sys.stdout.write(')')

#to-py-if
def to_py_if(exp):
    global tab_count
    sys.stdout.write('if ')
    analyse(if_cond(exp))
    sys.stdout.write(':\n')
    tab_count = tab_count + 1
    print_tab(tab_count)
    analyse(if_consequent(exp))
    print ""
    tab_count = tab_count - 1
    print_tab(tab_count)
    sys.stdout.write("else:\n")
    tab_count = tab_count + 1
    print_tab(tab_count)
    analyse(if_alternate(exp))
    tab_count = tab_count - 1

# to py decl
def to_py_decl(name,expr):
    print_tab(tab_count)
    print name," =",
    analyse(expr)

# to py def
def to_py_def(name,par,body):
    global tab_count
    sys.stdout.write("def "+name+"(")
    arg_list(par)
    sys.stdout.write(") :\n")
    tab_count = tab_count + 1
    analyse_sequence(body)
    tab_count = tab_count - 1

#define analyse
def define_analyser(exp):
    name = def_var(exp)
    par = def_par(exp)
    body = def_body(exp)
    if name in identifiers:
        print "identifier defined earlier:",name
    else:
        identifiers.append(name)
    if issymbol(exp[1:][0]):
        to_py_decl(exp[1:][0],exp[1:][1:][0])
    else:
        to_py_def(name,par,body)

#to_py_array
def to_py_array(l):
    print "[",
    arg_list(l)
    print "]"

while 1:
    try:
        s_exp_list = lispio.getSexp()
    except:
        break
    try:
        analyse(s_exp_list)
    except:
        print '???'
