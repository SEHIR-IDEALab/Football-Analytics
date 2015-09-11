__author__ = 'emrullah'


def get_coefficient():
    speed_data={}
    data = open ("/Users/aliuzun/PycharmProjects/futbol-data-analysis/src/sentio/pass_evaluate/player_speed.txt","r").readlines()

    for line in data:
        line=line.split()
        for i in range(2,45,2):
            tmp=float("{0:.1f}".format(float(line[i])))
            if (tmp >= 3.0) and (tmp <= 10):
                if tmp not in speed_data:
                    speed_data[tmp]=1
                else:
                    speed_data[tmp] = speed_data.get(tmp)+1
    # div = sum(speed_data.values())*1.0

    dd = speed_data.items()
    dd.sort()

    key,val=[],[]

    for i,j in dd:
        key.append(i)
        val.append(j)
    div = sum(val)*1.0

    new_dict={}
    end=len(val)
    for index,num in enumerate(key):
        new_dict[num]=sum(val[index:end])

    coef={}
    # x_val,y_val=[],[]
    for i,j in new_dict.items():
        coef[i]=(j/div)
    return coef