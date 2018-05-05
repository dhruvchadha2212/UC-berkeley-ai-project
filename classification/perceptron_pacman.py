# perceptron_pacman.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation for apprenticeship learning
import util
from perceptron import PerceptronClassifier
from pacman import GameState

PRINT = True


class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, maxIterations)
        self.weights = util.Counter()
    
    def classify(self, data ):
        """
            Data contains a list of (datum, legal moves)
            
            Datum is a Counter representing the features of each GameState.
            legalMoves is a list of legal moves for that GameState.
            """
        guesses = []
        # print(len(data))
        # print(data)
        print("\n\n\n")
        # print(data)
        for datum, legalMoves in data:
            #print(datum)
            vectors = util.Counter()
            for l in legalMoves:
                print(datum[l])
                # print(self.weights)
                vectors[l] = self.weights * datum[l] #changed from datum to datum[l]
            # print(vectors.argMax())
            guesses.append(vectors.argMax())
            print(guesses)
            print(self.weights)
            print(vectors.argMax())
            print("b")
        return guesses
    
    
    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        self.features = trainingData[0][0]['Stop'].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.
        # print(self.weights)
        # print(self.max_iterations)
        for iteration in range(self.max_iterations):
            # print("a")
            # print (len (trainingData))
            print "Starting iteration ", iteration, "..."
            for i in range (len (trainingData)):
                "*** YOUR CODE HERE ***"
                # util.raiseNotDefined()
                datum = trainingData[i]
                guess = self.classify ([datum])[0]
                print(guess)
                correctLabel = trainingLabels[i]
                print(correctLabel)
                # print (datum[0][correctLabel])
                # print("next")
                # print(self.weights)
                if guess != correctLabel:
                    # print("Corr")
                    self.weights += datum[0][correctLabel]
                    self.weights -= datum[0][guess]
