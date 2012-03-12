#!/usr/bin/env python

import json

class State:
    ''' This class represents a single state
    and its transitions '''
    def __init__(self, text, transitions=None, x=None, y=None, end=False):
        self.text = text
        self.transitions = transitions if transitions else dict()
        self.x = x
        self.y = y
        self.end = end

    def getPosition(self):
        return (self.x, self.y)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def addTransition(self, command, state):
        ''' Adds a transition to State object in
        state with the command text from command '''
        self.transitions[command] = state

    def getTransition(self, command):
        ''' Returns the transition taken from
        that command '''
        return self.transitions[command]

    def listTransitions(self):
        ''' Returns a list of all transition commands and states '''
        return [(k,v) for (k,v) in self.transitions.iteritems()]

    def removeTransition(self, command):
        ''' Removes a transition with the given command '''
        del self.transitions[command]

    def removeConnections(self, state):
        ''' Removes all transition to a given state '''
        toRemove = []
        for cmd, s in self.transitions.iteritems():
            if s == state: toRemove.append(cmd)
        for cmd in toRemove:
            del self.transitions[cmd]
                
    def __str__(self):
        s = self.text + "@" + str(x) + ',' + str(y) + " : {"
        for k,v in self.transitions.iteritems():
            s += repr(k) + ": " + repr(v.text) + ", "
        return s + "}"

class Graph:
    ''' This class stores an entire transition graph made
    out of State objects.'''
    def __init__(self, serialized=None):
        if serialized:
            self._readSerialized(serialized)
        else:
            self.states = []

    def _readSerialized(self, serialized):
        ''' Reads in the graph from a serialized format '''
        self.states = []

        # Read in states with text and attirbutes
        for st in serialized:
            state = State(st['state'], None, st['x'], st['y'], st['end'])
            self.states.append(state)

        # Add transitions between states
        for i,st in enumerate(serialized):
            start = self.states[i]
            for (cmd,j) in st['transitions'].iteritems():
                self.addTransition(start, self.states[j], cmd)

    def numStates(self):
        ''' Returns the number of states '''
        return len(self.states)

    def getState(self, index):
        ''' Gets the state at the given index '''
        return self.states[index]

    def getIndex(self, state):
        ''' Returns the index of the state '''
        return self.states.index(state)

    def addState(self, text='', x=0, y=0):
        ''' Adds a State object with the given text to the 
        graph, and returns the new state object '''
        state = State(text, x, y)
        self.states.append(state)
        return state

    def removeState(self, index):
        ''' Removes a state by index from the graph '''
        state = self.states.pop(index)
        for s in self.states:
            s.removeConnections(state)

    def addTransition(self, start, end, command):
        ''' Adds a transition from the start state to the
        end state on the given command '''
        start.addTransition(command, end)
        
    def removeTransition(self, start, command):
        ''' Removes a transition starting at start with
        the given command '''
        start.removeTransition(command)

    def toSerializable(self):
        ''' Converts graph into a format that can be
        serialized into JSON '''
        numbers = dict((v,i) for (i,v) in enumerate(self.states))
        out = []
        for i,v in enumerate(self.states):
            trns = dict((cmd,numbers[st]) for (cmd,st) \
                            in v.transitions.iteritems())
            out.append({'state': v.text, 
                        'x': v.x, 'y': v.y,
                        'end': v.end,
                        'transitions': trns})
        return out


def saveGraph(graph, filename):
    ''' Saves the graph to the given file name '''
    with open(filename, 'w') as outf:
        json.dump(graph.toSerializable(), outf)

def loadGraph(filename):
    ''' Loads a graph from a file '''
    with open(filename) as inf:
        j = json.load(inf)
    return Graph(serialized=j)

def playGame(graph):
    # TODO: add a method for getting the start state
    state = graph.getState(0)
    while not state.end:
        print state.text, "\n"
        options = state.listTransitions()
        for i,option in enumerate(options):
            print "\t%2d> %s" % (i+1, option)
        choice = int(raw_input('Select an option: ')) - 1
        state = state.getTransition(options[choice])
        print ""
    print "end of game"

if __name__ == '__main__':
    g = Graph()
    sn1 = g.addState('first state')
    sn2 = g.addState('another state')
    sn3 = g.addState('third state')
    sn3.end = True
    g.addTransition(sn1, sn2, 'go up')
    g.addTransition(sn1, sn3, 'pass')
    g.addTransition(sn2, sn1, 'go down')
    g.addTransition(sn2, sn3, 'continue')
    g.addTransition(sn3, sn1, 'back')
    #s = g.toSerializable()
    #print json.dumps(s, indent=2)
    playGame(g)
    
