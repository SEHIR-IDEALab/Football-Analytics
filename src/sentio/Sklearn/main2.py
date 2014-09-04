__author__ = 'aliuzun'

import time as tm
from WhoHasBall import *
from src.sentio.Sentio import Sentio



def main():
    start = tm.time()


    sentio = Sentio()
    sentio.parseSentioData(coordinate_data="../data/GS_FB_Sentio.txt", event_data="../data/GS_FB_Event.txt")

    hasball = WhoHasBall(sentio)

    #print hasball.Run_Test()
    print hasball.getCorrelatedPlayer_byTime(1,1,1,0)

    end = tm.time()

    print end - start

if __name__ == "__main__":
    main()

#[36, 85, 18.182324675324658, 53.072061208664685]