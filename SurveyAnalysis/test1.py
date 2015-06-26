__author__ = 'aliuzun'




# def get_coefficient():
speed_data={}
sum_ball,numberLine=[],0
data = open ("player_speed.txt","r").readlines()

# float("{0:.2f}".format(13.949999999999999))
for line in data:
    line=line.split()

    for i in range(2,45,2):
        if i==2:
            tmp=float("{0:.2f}".format(float(line[2])))
            if tmp <= 60.0:
                sum_ball.append(tmp)


        else:
            tmp=float("{0:.1f}".format(float(line[i])))
            if tmp <= 10:

                if tmp not in speed_data:
                    speed_data[tmp]=1
                else:
                    speed_data[tmp] = speed_data.get(tmp)+1

# print sum(sum_ball),len(sum_ball)

# print speed_data
di=sum(speed_data.values())
# print di
for key in speed_data.keys():
    speed_data[key]=100.0*speed_data.get(key)/316800.0

x_val=speed_data.keys()
y_val=speed_data.values()

import matplotlib.pyplot as plt
plt.plot(x_val, y_val, 'ro')
plt.axis([0, 10, 0, 10])
plt.show()

#total sample 14400*22 ==316800

print speed_data