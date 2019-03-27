import math


def cumsum(ls):
    
	acc = 0
	r = [0 for v in ls]
	for i,v in enumerate(ls):
		acc += v
		r[i] = acc
	return r


def extend(d, k, v):
    
	n = d.copy()
	n[k] = v
	return n

def cut(d, k):
    
	if isinstance(d, dict):
		n = d.copy()
		if k in n:
			del n[k]
		return n
	return [v for v in d if v != k]


def bayes_thm(likelihood, priorOutcome, priorCondition):
	return likelihood * priorOutcome / priorCondition

class DiscreteCPT(object):
   def __init__(self, vals, probTable):
		   self.myVals = vals
   if isinstance(probTable, list) or isinstance(probTable, tuple):
        		self.probTable = {(): probTable}
   else:
        		self.probTable = probTable
            
            
class DiscreteBayesNode(object):
	
	def __init__(self, name, parents, cpt):
		
		self.parents = parents
		self.name = name
		self.cpt = cpt
		
class DiscreteBayesNet(object):
	def __init__(self, nodes):
        
       self.variables = dict([(n.name, n) for n in nodes])
		 self.roots = [n for n in nodes if not n.parents]
		 self.nodes = nodes
   def enumerate_ask(self, var, e):
		vals = self.variables[var].cpt.values()
		dist = {}
		if var in e:
			for v in vals:
				dist[v] = 1.0 if e[var]==v else 0.0
			return dist
			
		for v in vals:
			dist[v] = self.enumerate_all(self.variables, 
											extend(e, var, v))
		normalize(dist)
		return dist
	
	def enumerate_all(self, vars, e, v=None):
		
		
		if len(vars) == 0:
			return 1.0
			
		if v:
			Y = v
		else:
			Y = vars.keys()[0]
		Ynode = self.variables[Y]
		parents = Ynode.parents
		cpt = Ynode.cpt
		
		# Work up the graph if necessary
		for p in parents:
			if p not in e:
				return self.enumerate_all(vars, e, p)
		
		if Y in e:
			y = e[Y]
			# P(y | parents(Y))
			cp = cpt.prob_dist([e[p] for p in parents])[y]
			result = cp * self.enumerate_all(cut(vars,Y), e)
		else:
			result = 0
			for y in Ynode.cpt.values():
				# P(y | parents(Y))
				cp = cpt.prob_dist([e[p] for p in parents])[y]
				result += cp * self.enumerate_all(cut(vars,Y),
													extend(e, Y, y))

		return result
		
	def prob(self, e):
		
		return self.enumerate_all(self.variables, e)
def values(self):
		return self.myVals
		
def prob_dist(self, parentVals):
		if isinstance(parentVals, list):
			parentVals = tuple(parentVals)
		return dict([(self.myVals[i],p) for i,p in \
					enumerate(self.probTable[parentVals])])
    
if __name__ == "__main__":
	# The burglary node has no parents
	burglary = DiscreteBayesNode('Burglary', [],
						# Mapping probabilities to T,F values for the variable
						DiscreteCPT(['T','F'], [0.001, 0.999]))
	
	# The earthquake node has no parents
	earthquake = DiscreteBayesNode('Earthquake', [],
						DiscreteCPT(['T','F'], [0.002, 0.998]))
						
	# The alarm node depends on burglary and earthquake
	alarm = DiscreteBayesNode('Alarm', ['Burglary', 'Earthquake'],
						DiscreteCPT(['T','F'],
							# Mapping values of B,E to T,F values for the
							# alarm
							{('T','T'):[0.95, 0.05],
							('T','F'):[0.94, 0.06],
							('F','T'):[0.29, 0.71],
							('F','F'):[0.001, 0.999]}))
	
	# The JohnCalls node depends on the alarm
	john = DiscreteBayesNode('JohnCalls', ['Alarm'],
						DiscreteCPT(['T','F'],
							# Mapping values of Alarm to T,F values for
							#  John calling
							{('T',):[0.9, 0.1],
							('F',):[0.05, 0.95]}))
									
	# The MaryCalls node depends on the alarm
	mary = DiscreteBayesNode('MaryCalls', ['Alarm'],
						DiscreteCPT(['T','F'],
							{('T',):[0.7, 0.3],
							('F',):[0.01, 0.99]}))
							
	burglarynet = DiscreteBayesNet([burglary, earthquake, alarm, john, mary])
	
	# Evidence can be empty (gives us the overall probability of something
	#  occurring, without prior knowledge)
	evidence = {}
	print("Prob. of earthquake:", \
			burglarynet.enumerate_ask('Earthquake', evidence))
			
	# Evidence can contain mappings of variables to legal values
	evidence = {'JohnCalls':'T', 'MaryCalls':'T'}
	print("Prob. of burglary, given John and Mary call:", \
		burglarynet.enumerate_ask('Burglary', evidence))    
            
            
