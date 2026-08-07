import numpy as np
from mdpPlayer import MdpPlayer
 
agent = MdpPlayer(gamma=0.95)
weights = agent.runValueIteration(numIterations=20, numStates=300)
 
np.save("trained_weights.npy", weights)
print("Trained weights:", weights)
