__author__ = 'aliuzun'
import random,math
from SurveyScoreCalculation import ScoreCal

q=ScoreCal()

class Optimization():

    def __init__(self):
        self.domain=[(2,10),(1,5),(1,20),(0,1000),(0,1000),(0,1000),(0,1000)] # [r1,r2,rgw1,w2,w3]
        # self.domain=[(1,20),(2,30)]
        # self.domain=[(1,50)] # possible goal distance

    def hillclimb(self):

        # Create a random solution
        sol=[random.randint(self.domain[i][0],self.domain[i][1])
            for i in range(len(self.domain))]

        # Main loop
        while 1:
            # Create list of neighboring solutions
            neighbors=[]

            for j in range(len(self.domain)):
              # One away in each direction
              if sol[j] > self.domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
              if sol[j] < self.domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])

            # See what the best solution amongst the neighbors is
            current = q.CostScore2(sol) # cost function
            best = current
            for j in range(len(neighbors)):
              cost = q.CostScore2(neighbors[j]) # cost function
              if cost > best:
                best = cost
                sol = neighbors[j]

            # If there's no improvement, then we've reached the top
            if best==current:
              break
        return (sol,best)


    def annealingoptimize(self,T=10000.0,cool=0.95,step=1):
        # Initialize the values randomly
        domain=self.domain
        vec=[float(random.randint(domain[i][0],domain[i][1]))
           for i in range(len(domain))]

        while T>0.1:
            # Choose one of the indices
            i=random.randint(0,len(domain)-1)

            # Choose a direction to change it
            dir=random.randint(-step,step)

            # Create a new list with one of the values changed
            vecb=vec[:]
            vecb[i]+=dir
            if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
            elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]

            # Calculate the current cost and the new cost
            ea = q.CostScore2(vec)
            eb = q.CostScore2(vecb)

            # Is it better, or does it make the probability
            # cutoff?
            if (eb > ea): vec = vecb

            else:
                p=pow(math.e,(-eb-ea)/T)

                if (random.random() < p):
                    vec = vecb

            # Decrease the temperature
            T=T*cool
        return (vec,eb)


    def geneticoptimize(self,pair,popsize=50,mutprob=0.2,step=1,elite=0.2,maxiter=100):

        domain = self.domain
        # Mutation Operation

        def mutate(vec):
            i=random.randint(0,len(domain)-2) # -2
            if random.random()<0.5 and vec[i]>domain[i][0]:
              return vec[0:i]+[vec[i]-step]+vec[i+1:]
            elif vec[i]<domain[i][1]:
              return vec[0:i]+[vec[i]+step]+vec[i+1:]

        # Crossover Operation
        def crossover(r1,r2):
            i=random.randint(1,len(domain)-2)# -2
            return r1[0:i]+r2[i:]

        # Build the initial population
        pop=[]
        for i in range(popsize):
            vec=[random.randint(domain[i][0],domain[i][1])
                 for i in range(len(domain))]
            pop.append(vec)

            # How many winners from each generation?
            topelite=int(elite*popsize)

        # Main loop

        for i in range(maxiter):
            try:
                print pop[i]
                scores=[(q.CostScore2(v,pair),v) for v in pop]
                scores.sort(reverse=True)
                ranked=[v for (s,v) in scores]

                # Start with the pure winners
                pop=ranked[0:topelite]

                # Add mutated and bred forms of the winners
                while len(pop)<popsize:
                    if random.random() < mutprob:

                        # Mutation
                        c=random.randint(0,topelite)
                        pop.append(mutate(ranked[c]))
                    else:

                        # Crossover
                        c1=random.randint(0,topelite)
                        c2=random.randint(0,topelite)
                        pop.append(crossover(ranked[c1],ranked[c2]))

                # Print current best score
                print scores[0][0]
            except IndexError:
                print "www"


        return scores[0][1]


if __name__ == "__main__":

    w=Optimization()
    # for i in range(50):
    #     print w.hillclimb()
    # print "----"
    # for i in range(30):
    #     print w.annealingoptimize()

    # print w.geneticoptimize()





    Qs=[0,1,2,3,4,5,6,7,8,9,10,11]
    for i in Qs:

        print "Q:",i+1,"-------"
        print w.geneticoptimize(i)

    # print "----"
    # Qs=[0,1,2,3,4,5,6,7,8,9,10,11]
    # for i in range(6):
    #     a,b=random.sample(Qs,2)
    #     Qs.remove(a)
    #     Qs.remove(b)
    #     print "Pair:",(a,b)
    #     print "Q:",i+1,"-------"
    #     print w.geneticoptimize((a,b))





#         ([33.0, 915.0, 547.0], 30)
# ([244.0, 135.0, 583.0], 30)
# ([169.0, 939.0, 37.0], 30)
# ([117.0, 137.0, 244.0], 30)
# ([563.0, 356.0, 119.0], 30)
# ([402.0, 283.0, 272.0], 30)
# ([619.0, 21.0, 223.0], 30)
# ([811.0, 499.0, 662.0], 30)
# ([165.0, 214.0, 233.0], 30)
# ([670.0, 433.0, 967.0], 30)