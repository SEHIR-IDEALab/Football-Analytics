import os
import time
from src.sentio.Parameters import DATA_BASE_DIR
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.file_io.reader.XMLreader import XMLreader
from src.sentio.pass_evaluate.Pass import Pass
import statistics

__author__ = 'emrullah'




reader = XMLreader(os.path.join(DATA_BASE_DIR, 'output/sentio_data_new.xml'))
game_instances, slider_mapping = reader.parse()

computation_times = []
evaluate = Pass()
for game_instance in game_instances.getAllInstances():
    if game_instance.event and game_instance.event.isPassEvent():
        pass_event = game_instance.event.pass_event
        # if pass_event.isSuccessful():
        # try:
        pass_source = pass_event.pass_source
        pass_target = pass_event.pass_target
        evaluate.teams = ReaderBase.divideIntoTeams(game_instance.players)
        start = time.time()
        evaluate.effectiveness_withComponents(pass_source, pass_target)
        temp_computation_time = time.time() - start  # in sec
        computation_times.append(temp_computation_time)
        # except:
        #     print "the algorithm is buggy"

print max(computation_times),min(computation_times),"---"
# bin1,bin2,bin3,bin4=[],[],[],[]
# for pt in computation_times:
#     if pt < 0.004: bin1.append(pt)
#     elif 0.004 <pt<  0.005: bin2.append(pt)
#     elif 0.005 <pt<  0.006: bin3.append(pt)
#     else: bin4.append(pt)
#
# print len(bin1),len(bin2),len(bin3),len(bin4)

cp = sorted(computation_times)
x,y=[],[]
index=0
while index < len(cp):
    x.append(float("{0:.5f}".format(cp[index])))
    y.append(index+1)
    index+=1


print x
# for i in x:
#     print i
#
# print "-------"
#
# for i in y:
#     print i



# print "total number of passes given", len(computation_times)
# print statistics.mean(computation_times)  # average computation time, in sec
# print statistics.median(computation_times)



