def call_a(msg):
    '''
    '''
    print("Function a: ", msg)
    

def call_b(msg):
    '''
    '''
    print("Function b: ", msg)


def call_c(msg):
    '''
    '''
    print("Function c: ", msg)

action = 'm'

# Using elif
if action == 'a':
    call_a("argument")
elif action == 'b':
    call_b("argument")
elif action == 'c':
    call_c("argument")

# Using function references
functions = dict(a=call_a, b=call_b, c=call_c)
try:
    functions[action]("argument")
except KeyError:
    print("Define method for action: ", action)
