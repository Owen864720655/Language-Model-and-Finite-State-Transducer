from fst import *


AZ = set('abcdefghijklmnopqrstuvwxyz')
VOWS = set('aeiou')
CONS = set('bcdfghjklmnprstvwxz')
E = set('E')


def buildFST():
    # The states:
    # ---------------------------------------
    f = FST('q0') # q0 is the initial (non-accepting) state
    f.addState('q1') # a non-accepting state
    f.addState('q_ing') # a non-accepting state
    f.addState('q_EOW', True) # an accepting state

    # The transitions:
    # ---------------------------------------

    # transduce every element in this set to itself
    f.addSetTransition('q0', AZ, 'q1')
    
    # AZ-E =  the set AZ without the elements in the set E
    f.addSetTransition('q1', AZ-E, 'q1')

    # get rid of this transition! (it overgenerates)
    f.addSetTransition('q1', AZ, 'q_ing')

    # map the empty string to ing
    f.addTransition('q_ing', '', 'ing', 'q_EOW')

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
