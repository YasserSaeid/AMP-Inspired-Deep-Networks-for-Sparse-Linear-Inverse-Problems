#MIT LIC

import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # BE QUIET!!!!
import tensorflow as tf

np.random.seed(1) # numpy is good about making repeatable output
tf.set_random_seed(1) # on the other hand, this is basically useless (see issue 9171)

# import our problems, networks and training modules
from tools import problems,networks,train

# Create the basic problem structure.
prob = problems.bernoulli_gaussian_trial(kappa=None,M=250,N=500,L=1000,pnz=.1,SNR=40) #a Bernoulli-Gaussian x, noisily observed through a random matrix
#prob = problems.random_access_problem(2) # 1 or 2 for compressive random access or massive MIMO

# build a LAMP network to solve the problem and get the intermediate results so we can greedily extend and then refine(fine-tune)
layers = networks.build_LAMP(prob,T=6,shrink='bg',untied=False)

# plan the learning
training_stages = train.setup_training(layers,prob,trinit=1e-3,refinements=(.5,.1,.01) )

# do the learning (takes a while)
sess = train.do_training(training_stages,prob,'LAMP_bg_giid.npz')
