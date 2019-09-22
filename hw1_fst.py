from fst import *


AZ = set('abcdefghijklmnopqrstuvwxyz')
VOWS = set('aeiou')
CONS = set('bcdfghjklmnprstvwxz')
E = set('e')
U = set('u')


def buildFST():
    # The states:
    # ---------------------------------------
    f = FST('q0') # q0 is the initial (non-accepting) state
    f.addState('q1')
    f.addState('q_ing')
    f.addState('q_drop_E')
    f.addState('q_EE')
    f.addState('q_IE')
    f.addState('q_EOW', True) # an accepting state

    # The transitions:
    # ---------------------------------------
    f.addSetTransition('q0', AZ, 'q1')

    f.addSetTransition('q1', AZ, 'q1')
    f.addSetTransition('q1', CONS.union(U), 'q_drop_E')
    f.addSetTransition('q1', E, 'q_EE')
    f.addSetTransition('q1', AZ-E, 'q_ing')
    f.addTransition('q1', 'i', '', 'q_IE')

    f.addTransition('q_ing', '', 'ing', 'q_EOW')

    f.addTransition('q_drop_E', 'e', '', 'q_ing')

    f.addSetTransition('q_EE', E, 'q_ing')

    f.addTransition('q_IE', 'e', 'y', 'q_ing')
    
    # Return your completed FST
    return f
    

if __name__ == '__main__':
    # Pass in the input file as an argument
    if len(sys.argv) < 2:
        print('This script must be given the name of a file containing verbs as an argument')
        quit()
    else:
        file = sys.argv[1]

    # Construct an FST for translating verb forms
    f = buildFST()

    # Print out the FST translations of the input file
    f.parseInputFile(file)
