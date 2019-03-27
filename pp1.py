# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 05:47:23 2018

@author: Soutrik
"""
obs = input("Compute_a_posteriori ")

def likelihood(obs, h):
    if h == 0:
        return (1.0 if obs == 'C' else 0)
    elif h == 1:
        return (0.75 if obs == 'C' else 0.25)
    elif h == 2:
        return (0.50 if obs == 'C' else 0.50)
    elif h == 3:
        return (0.25 if obs == 'C' else 0.75)
    elif h == 4:
        return (0 if obs == 'C' else 1.0)
    
h_apriori = [0.1,0.2,0.4,0.2,0.1]

def calculateProbab(q, h):
	value = 1;
	for i in range(len(q)):
		value = value * likelihood(q[i], h)
	value = value * h_apriori[h];
	return value

def computeObservation(string):
	ph1 = calculateProbab(string, 0);
	ph2 = calculateProbab(string, 1);
	ph3 = calculateProbab(string, 2);
	ph4 = calculateProbab(string, 3);
	ph5 = calculateProbab(string, 4);

	alpha = 1/(ph1 + ph2 + ph3 + ph4 + ph5)


	print('P(h1 | Q) = ',alpha * ph1)
	print('P(h2 | Q) = ',alpha * ph2)
	print('P(h3 | Q) = ',alpha * ph3)
	print('P(h4 | Q) = ',alpha * ph4)
	print('P(h5 | Q) = ',alpha * ph5)

	prediction_c = likelihood('C', 0) * alpha * ph1 + likelihood('C', 1) * alpha * ph2 + likelihood('C', 2) * alpha * ph3 + likelihood('C', 3) * alpha * ph4 + likelihood('C', 4) * alpha * ph5
	prediction_l = likelihood('L', 0) * alpha * ph1 + likelihood('L', 1) * alpha * ph2 + likelihood('L', 2) * alpha * ph3 + likelihood('L', 3) * alpha * ph4 + likelihood('L', 4) * alpha * ph5
	print('Probability that the next candy we pick will be C, given Q: ',prediction_c)
	print('Probability that the next candy we pick will be L, given Q: ',prediction_l)
	print('')

def generateResult(obs):
    sizeOfObservation = len(obs);
    print('Observation sequence Q: '+obs)
    print('Length of Q: '+str(sizeOfObservation))
    for i in range(1, sizeOfObservation + 1):
        substring = obs[:i]
        print('After Observation ',str(i),' = ',substring,':')
        computeObservation(substring)

generateResult(obs)
