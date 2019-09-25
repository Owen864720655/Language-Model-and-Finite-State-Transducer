from fst import *


A2Z = set('abcdefghijklmnopqrstuvwxyz')
VOWS = set('aeiou')
CONS = A2Z-VOWS
E = set('e')
U = set('u')
NR = set('nr')
PT = set('pt')


def buildFST():
    # The states:
    # ---------------------------------------
    f = FST('q0') # q0 is the initial (non-accepting) state
    f.addState('q1')
    f.addState('q_ing')
    f.addState('q_drop_E')
    f.addState('q_EE')
    f.addState('q_IE')
    f.addState('q_VOWS')
    f.addState('q_VOWS2')
    f.addState('q_CONS')
    f.addState('q_CONS+E')
    f.addState('q_CONS_VOWS-E')
    f.addState('q_EOW', True) # an accepting state

    # The transitions:
    # ---------------------------------------
    f.addSetTransition('q0', A2Z, 'q1')
    f.addSetTransition('q0', CONS, 'q_CONS')
    f.addSetTransition('q0', VOWS, 'q_VOWS')

    f.addSetTransition('q1', A2Z, 'q1')
    f.addSetTransition('q1', CONS.union(U), 'q_drop_E')
    f.addSetTransition('q1', E, 'q_EE')
    f.addTransition('q1', 'i', '', 'q_IE')
    f.addSetTransition('q1', VOWS, 'q_VOWS')
    f.addSetTransition('q1', CONS, 'q_CONS')

    f.addTransition('q_ing', '', 'ing', 'q_EOW')

    f.addTransition('q_drop_E', 'e', '', 'q_ing')

    f.addSetTransition('q_EE', E, 'q_ing')

    f.addTransition('q_IE', 'e', 'y', 'q_ing')
    
    f.addSetTransition('q_VOWS', VOWS, 'q_VOWS2')

    f.addSetTransition('q_VOWS2', CONS, 'q_ing')

    f.addSetTransition('q_CONS', E, 'q_CONS+E')
    f.addSetTransition('q_CONS', VOWS-E, 'q_CONS_VOWS-E')
    f.addSetTransition('q_CONS', CONS, 'q_ing')

    f.addSetTransition('q_CONS+E', A2Z-PT-VOWS, 'q_ing')
    for i in PT:
        f.addTransition('q_CONS+E', i, i*2, 'q_ing')
    
    f.addSetTransition('q_CONS_VOWS-E', A2Z-NR-PT-VOWS, 'q_ing')
    for i in NR.union(PT):
        f.addTransition('q_CONS_VOWS-E', i, i*2, 'q_ing')
    
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
