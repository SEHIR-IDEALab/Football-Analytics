__author__ = 'emrullah'


def get_coefficient():

    speed_data={}
    sum_ball,numberLine=[],0
    data = open ("pass_evaluate/player_speed.txt","r").readlines()

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
                if tmp <= 10.38:

                    if tmp not in speed_data:
                        speed_data[tmp]=1
                    else:
                        speed_data[tmp] = speed_data.get(tmp)+1

    # print sum(sum_ball),len(sum_ball)

    # print speed_data
    # di=sum(speed_data.values())
    # print di
    for key in speed_data.keys():
        speed_data[key]=100.0*speed_data.get(key)/316800.0

    return speed_data