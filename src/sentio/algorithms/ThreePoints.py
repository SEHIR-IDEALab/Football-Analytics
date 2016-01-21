import math

__author__ = 'aliuzun'

class ThreePoints:

    def __init__(self):
        self.aSlow=2.86*2
        self.aFast=2.86
        self.tp=.5 # in s, that is excepted penalty time for 180 deg return

    def getAlphaAndSlope(self,p1,p2):
        (x1,y1),(x2,y2)=p1,p2
        dx,dy=(x2-x1),(y2-y1)
        dx =(dx if dx !=0 else 0.01)
        slope = math.atan(dy/dx)
        alpha = math.degrees(slope)
        alpha = (alpha if alpha > 0 else alpha + 180.0)
        return (alpha,slope)

    def getDirectionInfo(self,p1,p2,w1,w2):
        turn_angle1,turn_angle2,Q1,Q2=None,None,None,None
        (x1,y1),(x2,y2)=p1,p2

        alpha,slope = self.getAlphaAndSlope(p1,p2)
        if slope >0:
            Ra1,Rb1,Rd1,Rc1=(alpha <= w1 < 90.0 + alpha),((w1 >= 270.0 + alpha) or (w1<alpha)),(180+ alpha >= w1 > 90.0 + alpha),(180+alpha < w1 < 270.0 + alpha)
            Ra2,Rb2,Rd2,Rc2=(alpha <= w2 < 90.0 + alpha),((w2 >= 270.0 + alpha) or (w2<alpha)),(180+ alpha >= w2 > 90.0 + alpha),(180+alpha < w2 < 270.0 + alpha)
            if y1 > y2:
                Q1,Q2=alpha+180,alpha
                if Ra1 or Rd1:
                    turn_angle1 = math.fabs(180-math.fabs(w1-alpha))
                elif Rb1:
                    turn_angle1 = min(math.fabs(180-math.fabs(alpha-w1)),math.fabs(w1-(180+alpha)))
                else: #Rc1
                    turn_angle1 = math.fabs(w1-(180+alpha))

                if Ra2 or Rd2:
                    turn_angle2 = math.fabs(w2-alpha)
                elif Rb2:
                    turn_angle2 = min(math.fabs(w2-alpha),(360-w2)+alpha)
                else: # Rc2
                    turn_angle2 = (360-w2)+alpha
            else:
                Q1,Q2=alpha,alpha+180
                if Ra1 or Rd1:
                    turn_angle1 = math.fabs(w1-alpha)
                elif Rb1:
                    turn_angle1 = min(math.fabs(alpha-w1),(360-w1)+alpha)
                else: #Rc1
                    turn_angle1 = (360-w1)+alpha

                if Ra2 or Rd2:
                    turn_angle2 = math.fabs(180-math.fabs(w2-alpha))
                elif Rb2:
                    turn_angle2 = min(math.fabs(180-math.fabs(alpha-w2)),math.fabs(w2-(180+alpha)))
                else: # Rc2
                    turn_angle2 = math.fabs(w1-(180+alpha))

        elif slope < 0:
            Ra1,Rb1,Rc1,Rd1=(alpha-90 < w1 <= alpha),(180+alpha <= w1 or w1 <= alpha-90 ),(alpha+90 <= w1 < 180+alpha),(alpha < w1 < alpha+90)
            Ra2,Rb2,Rc2,Rd2=(alpha-90 < w2 <= alpha),(180+alpha <= w2 or w2 <= alpha-90 ),(alpha+90 <= w2 < 180+alpha),(alpha < w2 < alpha+90)
            if y1 > y2 :
                Q1,Q2=alpha+180,alpha
                if Ra1:
                    turn_angle1 = 180-(alpha-w1)
                elif Rb1:
                    turn_angle1 = min(math.fabs(w1+(180-alpha)),math.fabs(w1-(alpha+180)))
                elif Rc1 or Rd1:
                    turn_angle1 = (180+alpha)-w1

                # if Ra2:
                #     turn_angle2 = alpha-w2
                if Rb2:
                    turn_angle2 = min(math.fabs(alpha-w2),math.fabs(180-(w2-(alpha+180))))
                else:
                    turn_angle2 = math.fabs(w2-alpha)

            else:
                Q1,Q2=alpha,alpha+180
                # if Ra1:
                #     turn_angle1 = alpha-w1
                if Rb1:
                    turn_angle1 = min(math.fabs(alpha-w1),math.fabs(180-(w1-(alpha+180))))
                else:
                    turn_angle1 = math.fabs(w1-alpha)
                if Ra2:
                    turn_angle2 = 180-(alpha-w2)
                elif Rb2:
                    turn_angle2 = min(math.fabs(w2+(180-alpha)),math.fabs(w2-(alpha+180)))
                elif Rc2 or Rd2:
                    turn_angle2 = (180+alpha)-w2
        else:
            Ra1,Rb1,Rd1,Rc1=(0 < w1 <= 90.0 ),((w1 > 270.0 )),(180 >= w1 > 90.0 ),(180 < w1 <= 270.0 )
            Ra2,Rb2,Rd2,Rc2=(0 < w2 <= 90.0 ),(w2 > 270.0 ),(180 >= w2 > 90.0 ),(180 < w2 <= 270)
            print Ra2,Rb2,Rc2,Rd2,w2
            if x1 > x2:
                Q1,Q2=180,0
                turn_angle1 = math.fabs(180-w1)
                if Ra2 or Rd2:
                    turn_angle2 = w2
                else:
                    turn_angle2 = 360-w2
            else:
                Q1,Q2=0,180
                turn_angle2 = math.fabs(180-w2)
                if Ra1 or Rd1:
                    turn_angle1 = w1
                else: turn_angle1 = 360-w1
        print Q1,Q2,turn_angle1,turn_angle2,"--------"
        return Q1,Q2,turn_angle1,turn_angle2

    def gelDM(self,p1,V1,p2,V2,w1,w2):   # return the movement distance
        if V1 == 0.0 and V2 == 0.0: V1 = 0.5; V2 = 0.5

        (x1,y1),(x2,y2)=p1,p2
        Q1,Q2,turn_angle1,turn_angle2=self.getDirectionInfo(p1,p2,w1,w2)
        t_penalty1,t_penalty2 = (turn_angle1/180.0)*self.tp,(turn_angle2/180.0)*self.tp
        print t_penalty1,t_penalty2
        distance=math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
        t=distance/(V1+V2)

        dp1,dp2=V1*t,V2*t

        d_f1,d_f2=V1*t_penalty1 , V2*t_penalty2
        d_left=d_f1+d_f2
        dp1,dp2=dp1-d_f1,dp2-d_f2
        da1,da2=V1*(d_left/(V1+V2)),V2*(d_left/(V1+V2))
        d_total1,d_total2 =dp1+da1,dp2+da2

        return {p1:(d_total1,Q1),p2:(d_total2,Q2)}

    def NewPoint(self,p,d,alpha):
        x0,y0=p
        Q1= math.radians(alpha)
        # sings=[1.0,-1.0]
        # if 0 < alpha <=90:      x_sing,y_sing=sings[0],sings[0]
        # elif 90 < alpha <=180:  x_sing,y_sing=sings[1],sings[0]
        # elif 180 < alpha <=270: x_sing,y_sing=sings[1],sings[1]
        # else:                x_sing,y_sing=sings[0],sings[1]
        x1,y1  = x0 + (d)*round(math.cos(Q1),2) ,\
                       y0 + (d)*round(math.sin(Q1),2)
        # x1,y1  = x0 + x_sing*(d)*round(math.cos(Q1),2) ,\
        #                y0 + y_sing*(d)*round(math.sin(Q1),2)
        return x1,y1

    def Do(self,p1,p2,p3,V1,V2,V3,w1,w2,w3):
        pairs=[(p1,p2),(p1,p3),(p2,p3)]
        Vs=[(V1,V2),(V1,V3),(V2,V3)]
        ws=[(w1,w2),(w1,w3),(w2,w3)]
        tmp_p_list={}
        check_dict={p1:0,p2:0,p3:0}
        for index in range(len(pairs)):
            (pa,pb),(Va,Vb),(wa,wb) = pairs[index],Vs[index],ws[index]
            if Va > Vb: b_point=pa
            else: b_point=pb
            length,Q = self.gelDM(pa,Va,pb,Vb,wa,wb)[b_point]

            new_x,new_y=self.NewPoint(b_point,length,Q)
            check_dict[b_point]+=1
            if b_point not in tmp_p_list:
                tmp_l=(new_x,new_y)
                tmp_p_list[b_point]=tmp_l
            else: tmp_p_list[b_point]=((tmp_l[0]+new_x)*0.5,(tmp_l[1]+new_y)*0.5)

        if len(tmp_p_list)>2:
                tmp_p_list[p3]=p3
        else:
            for p in check_dict:
                if check_dict[p] == 0:
                    # print p
                    tmp_p_list[p]=p
        return [tmp_p_list[p1],tmp_p_list[p2],tmp_p_list[p3]]




def getDxy(p1,p2):
    (x1,y1),(x2,y2)=p1,p2
    dx,dy=(x2-x1),(y2-y1)
    return dx,dy

p1,p1e=(13.0,22.9),(15.0,15.0)
p2,p2e=(42.0,40.0),(15.0,25.0)
p3,p3e=(93.0,51.0),(15.0,20.0)
V1=math.sqrt(math.pow((p1[0]-p1e[0]),2) + math.pow((p1[1]-p1e[1]),2))
V2=math.sqrt(math.pow((p2[0]-p2e[0]),2) + math.pow((p2[1]-p2e[1]),2))
V3=math.sqrt(math.pow((p3[0]-p3e[0]),2) + math.pow((p3[1]-p3e[1]),2))

# import matplotlib.pyplot as plt
#
#
# if __name__=="__main__":
#     q=MovePoints()
#     # w1,w2,w3=q.getAlphaAndSlope(p1,p1e)[0],q.getAlphaAndSlope(p2,p2e)[0],q.getAlphaAndSlope(p3,p3e)[0]
#     w1,w2,w3=330,250,170
#     V1,V2,V3=2,2.5,4.2
#     pa,pb,pc= q.Do(p1,p2,p3,V1,V2,V3,w1,w2,w3)
#     # plt.scatter([pa[0],pb[0],pc[0]],[pa[1],pb[1],pc[1]],c="r")
#     # print(pa,pb,pc)
#     plt.scatter(p1[0],p1[1],c="b")
#     plt.scatter(p2[0],p2[1],c="y")
#     plt.scatter(p3[0],p3[1],c="g")
#
#     plt.scatter(pa[0],pa[1],c="r",s=50)
#     plt.scatter(pb[0],pb[1],c="r",s=50)
#     plt.scatter(pc[0],pc[1],c="r",s=50)
#
#     # plt.plot([p1[0],p2[0]],[p1[1],p2[1]],c='r')
#     # plt.plot([p1[0],p3[0]],[p1[1],p3[1]],c='r')
#     # plt.plot([p2[0],p3[0]],[p2[1],p3[1]],c='r')
#
#     # dx,dy=getDxy(p1,p1e)
#     # plt.arrow(p1[0],p1[1],dx,dy,head_length=0.1, fc='k', ec='k')
#     # dx,dy=getDxy(p2,p2e)
#     # plt.arrow(p2[0],p2[1],dx,dy,head_length=0.1, fc='k', ec='k')
#     # dx,dy=getDxy(p3,p3e)
#     # plt.arrow(p3[0],p3[1],dx,dy,head_length=0.1, fc='k', ec='k')
#
#
#     # print q.getAlphaAndSlope(p1,p3)
#     # print q.getDirectionInfo(p1,p3,w1,w3),"Bu"
#     # k,l=q.NewPoint(p3,2,123.05)
#
#
#     #
#     # im2=plt.imread('/Users/aliuzun/PycharmProjects/futbol-data-analysis/src/sentio/Sklearn/srcc/background.png',0)
#     # hm = plt.imshow(im2, extent=[-2.0, 107.0, 0.0, 72.0], aspect="auto")
#     plt.show()