# coding=utf-8
from Tkconstants import VERTICAL, Y, LEFT, END, E, NE

import Tkinter as Tk
import csv
import time as tm
import math
import tkFileDialog
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.patches import BoxStyle
import matplotlib.pyplot as plt
import numpy
from src.sentio.CircleStyle import CircleStyle
from src.sentio.DraggablePass import DraggablePass
from src.sentio.DraggableText import DraggableText
from src.sentio.Player_base import Player_base
from src.sentio.Time import Time

__author__ = 'emrullah'


class Visualization(object):
    def __init__(self, coordinateData_byTme, eventData_byTime, teamNames, minMaxOfHalf, id_explanation):

        self.coordinatesData_byTime = coordinateData_byTme
        self.eventData_byTime = eventData_byTime
        self.teamNames = teamNames
        self.minMaxOfHalf = minMaxOfHalf
        self.event_id_explanation = id_explanation


        self.master = Tk.Tk()
        self.master.wm_title("Game Data Visualization")
        self.master.geometry("1200x750")

        menubar = Tk.Menu(self.master)

        filemenu = Tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.saveSnapShot)
        filemenu.add_command(label="Load", command=self.loadSnapShot)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Create a container
        self.frame = Tk.Frame(self.master)

        self.scaleVariable = Tk.DoubleVar()
        scale = Tk.Scale(self.frame,orient=Tk.HORIZONTAL,length=700, width=20, sliderlength=10, showvalue=0,
                 from_=0, to=90, resolution=(1.0/300.0), variable=self.scaleVariable, tickinterval=15).pack(side="bottom")

        rb_var = Tk.IntVar()
        rb_pass = Tk.Radiobutton(self.master, text="Define Pass", variable=rb_var, value=1,
                                 command=self.rb_define_pass).pack(side='top')
        rb_drag = Tk.Radiobutton(self.master, text= "Draggable Objects", variable=rb_var,value=2,
                                 command=self.rb_drag_objects).pack(side='top')

        self.heatmapTypeVariable = Tk.StringVar()
        self.heatmapTypeVariable.set("-----")
        heatmapType_options = Tk.OptionMenu(self.frame, self.heatmapTypeVariable, "-----", "defence position taking",
                                            "position of target of pass", "position of source of pass").pack(side="top",anchor=NE)
        self.resolutionLevelVariable = Tk.StringVar()
        self.resolutionLevelVariable.set("2")
        resolutionLevel_options = Tk.OptionMenu(self.frame, self.resolutionLevelVariable,
                                                "0.5", "1", "2", "3", "4", "5", "10").pack(side="top", anchor=NE)


        self.componentsOfEffectivenessVariable = Tk.StringVar()
        self.componentsOfEffectivenessVariable.set("effectiveness")
        componentsOfEffectiveness_options = Tk.OptionMenu(self.frame, self.componentsOfEffectivenessVariable,
                            "effectiveness", "gain", "pass advantage", "goal chance", "overall risk").pack(side="top",anchor=NE)


        self.text_toDisplayPasses = Tk.Text(self.master, width=35, height=35)
        self.text_toDisplayPasses.pack(side="left", anchor="nw")
        yscrollbar = Tk.Scrollbar(self.master, orient=VERTICAL, command=self.text_toDisplayPasses.yview)
        yscrollbar.pack(side=LEFT, fill=Y)
        self.text_toDisplayPasses["yscrollcommand"]=yscrollbar.set

        self.effec_withCompVariable_forChosenPoint = Tk.StringVar()
        self.effec_withCompVariable_forChosenPoint.set("dasdasdasdasdasdasdasdas")
        displayChosenPoint = Tk.Label(master=self.frame, textvariable=self.effec_withCompVariable_forChosenPoint, justify=LEFT)\
            .pack()

        button_scaleDraw = Tk.Button(master=self.frame, text='Draw', command=self.scaleDraw).pack(side="left")
        button_play = Tk.Button(master=self.frame, text='Play', command=self.play).pack(side="left")

        self.pauseButtonClicked = False
        self.directionSpeed_ofObjects = list()
        self.currentTime_whenPause = [min(self.minMaxOfHalf.keys())] + self.minMaxOfHalf[min(self.minMaxOfHalf.keys())][0] # 1,0,0,0

        button_pause = Tk.Button(master=self.frame, text='Pause', command=self.pause).pack(side="left")

        self.playVariable = Tk.StringVar()
        self.playVariable.set("normal")
        self.play_options = Tk.OptionMenu(self.frame, self.playVariable, "slow", "normal", "fast").pack(side="left")

        self.skipPlayVariable = Tk.StringVar()
        self.skipPlayVariable.set("0")
        self.skipPlay_options = Tk.OptionMenu(self.frame, self.skipPlayVariable, "0", "1", "2", "3", "4").pack(side="left")

        self.button_quit = Tk.Button(self.frame, text="Quit", command=self.quit).pack(side="right")

        self.currentTimeVariable = Tk.StringVar()
        self.currentTimeVariable.set("Time = 0.0.0")
        self.label = Tk.Label(master=self.frame, textvariable = self.currentTimeVariable).pack(side="right")

        #*********************************************************

        fig = plt.figure(figsize=(5,4))

        self.canvas = FigureCanvasTkAgg(fig,master=self.master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)

        self.ax = fig.add_subplot(111)
        im = plt.imread('source/background.png')
        self.ax.imshow(im, zorder=0, extent=[-5.0, 110.0, 0, 65.0], aspect="auto")
        self.ax.grid()
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 120, 5))
        self.ax.set_yticks(numpy.arange(-5, 75, 5))

        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = \
            self.getObjectsCoords_forGivenTime(1, 0, 0, 0)

        self.trailAnnotation, self.eventAnnotation, self.passAnnotation, self.passEffectivenessAnnotation, self.ballAnnotation = None, None, None, None, None
        self.count_forEventAndPassEffect = 0

        self.texts = list()
        self.definePasses = None
        self.definedPasses_forSnapShot = list()
        self.setJerseyNumbers_forGivenObjects(homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)

        a,b,c,d, = plt.plot([],[],"bo",[],[],"ro",[],[],"yo",[],[],"ko", markersize=15)
        self.ax.legend([a,b,c,d], [self.teamNames[0].decode("utf-8"), self.teamNames[1].decode("utf-8"), 'Referees', 'Unknown Objects'],
                       numpoints=1, fontsize=12, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.5)

        self.frame.pack()
        self.master.config(menu=menubar)
        self.master.mainloop()


    def saveSnapShot(self):
        fileName = tkFileDialog.asksaveasfilename(initialfile=("%s_%s"%self.teamNames), initialdir="../../SampleScenarios")
        if fileName:
            a = list()
            a.extend(["team_id", "team_name", "jersey_no", "x1", "y1", "x2", "y2", "speed", "passTo"])
            homeTeam, awayTeam = self.teamNames
            current_half, current_minute, current_second, current_milisecond = self.currentTime_whenPause
            name_of_file = "%s.csv" %(fileName)
            out = csv.writer(open(name_of_file,"a"), delimiter='\t', quoting=csv.QUOTE_NONE)
            out.writerow(a)
            del a[:]
            homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forSnapShot()
            hm, wy, rfr, nkw = self.getDirectionOfObjects_forGivenTime(
            current_half, current_minute, current_second, current_milisecond)
            teams_next = [hm, wy, rfr, nkw]
            teams = self.getSpeedOfObjects_forGivenTime(current_half, current_minute, current_second, current_milisecond)
            for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for player in team:
                    teamID = (index if index != 3 else -1)
                    teamName = (homeTeam if index == 0 else (awayTeam if index == 1 else ("referee" if index == 2 else "unknownObject")))
                    jersey_number = player
                    currentX, currentY = team[player]
                    nextX, nextY = teams_next[index][player][0][1], teams_next[index][player][1][1]
                    speed = teams[index][player]
                    js2 = ""
                    for i in self.definePasses.definedPasses:
                        p1 = i.textcoords
                        x1, y1 = p1.get_position()
                        js1 = p1.get_text()
                        if currentX==x1 and currentY==y1 and jersey_number==int(js1):
                            p2 = i.xycoords
                            js2 += p2.get_text() + "@"
                    passTo = ("None" if js2=="" else js2[:-1])
                    a.extend([teamID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo])
                    out.writerow(a)
                    del a[:]


    def loadSnapShot(self):
        filename = tkFileDialog.askopenfilename(initialdir="../../SampleScenarios")
        if filename:
            self.remove_directionSpeedOfObjects() # remove previous annotations
            self.remove_allDefinedPassesForSnapShot()
            homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = dict(),dict(),dict(),dict()
            with open(filename) as fname:
                fname.readline()
                snapshot_data= csv.reader(fname, delimiter="\t")
                for line in snapshot_data:
                    teamID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = line
                    teamID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = \
                        int(teamID), teamName, int(jersey_number), float(currentX), float(currentY), \
                        float(nextX), float(nextY), float(speed), passTo

                    lengthX = (nextX - currentX) * speed
                    nextX = lengthX + currentX

                    lengthY = (nextY - currentY) * speed
                    nextY = lengthY + currentY

                    default_arrow_size = 2
                    if lengthX >= 0: nextX += default_arrow_size
                    else: nextX -= default_arrow_size
                    if lengthY >= 0: nextY += default_arrow_size
                    else: nextY -= default_arrow_size

                    passAnnotation = self.ax.annotate('', xy=(nextX,nextY), xycoords='data', xytext=(currentX,currentY),
                                                textcoords='data',size=20, va="center", ha="center",zorder=2, arrowprops=dict(
                                                arrowstyle="simple", connectionstyle="arc3",fc="cyan", ec="b", lw=2))
                    self.directionSpeed_ofObjects.append(passAnnotation)

                    if teamID in [0]:
                        homeTeamPlayers[jersey_number] = [currentX, currentY]
                    elif teamID in [1]:
                        awayTeamPlayers[jersey_number] = [currentX, currentY]
                    elif teamID in [2]:
                        referees[jersey_number] = [currentX, currentY]
                    else:
                        unknownObjects[jersey_number] = [currentX, currentY]

            if self.eventAnnotation != None: self.eventAnnotation.remove(); del self.eventAnnotation; self.eventAnnotation = None
            if self.passAnnotation != None: self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None
            if self.trailAnnotation!=None: self.trailAnnotation.remove(); del self.trailAnnotation; self.trailAnnotation = None
            if self.ballAnnotation!=None: self.ballAnnotation.remove(); del self.ballAnnotation; self.ballAnnotation = None

            self.remove_previousJerseyNumbers()
            self.text_toDisplayPasses.delete("1.0", END)
            self.setJerseyNumbers_forGivenObjects(homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)

            with open(filename) as fname:
                fname.readline()
                snapshot_data= csv.reader(fname, delimiter="\t")
                for line in snapshot_data:
                    teamID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = line
                    teamID, teamName, jersey_number, currentX, currentY, nextX, nextY, speed, passTo = \
                        teamID, teamName, jersey_number, float(currentX), float(currentY), \
                        float(nextX), float(nextY), float(speed), passTo
                    self.displayPasses_forSnapShot(passTo, currentX, currentY, jersey_number, teamID)

            self.currentTimeVariable.set("Time = %s.%s.%s" %("-", "-", "-"))

            self.canvas.draw()
            #self.master.update()
            self.frame.update()


    def displayPasses_forSnapShot(self, passTo, currentX, currentY, jersey_number, teamID):
        if passTo != "None":
            teams = {(0.0, 0.0, 1.0, 0.5):"0", (1.0, 0.0, 0.0, 0.5):"1",
                            (1.0, 1.0, 0.0, 0.5):"2", (0.0, 0.0, 0.0, 0.5):"-1"}
            p1, p2_s = None, []
            passTo = [pto for pto in passTo.split("@")]
            for jsTo in passTo:
                for i in self.texts:
                    x, y = i.point.get_position()
                    js = i.point.get_text()
                    team_id = teams[i.point.get_bbox_patch().get_facecolor()]
                    if p1 == None:
                        if currentX==x and currentY==y and js==jersey_number:
                            p1 = i.point
                    if team_id==teamID and js==jsTo:
                        p2_s.append(i.point)
            for p2 in p2_s:
                passAnnotation = self.ax.annotate('', xy=(.5, .5), xycoords=(p2), ha="center", va="center",
                    xytext=(.5, .5), textcoords=(p1), size=20, arrowprops=dict(patchA=p1.get_bbox_patch(),
                    patchB=p2.get_bbox_patch(), arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))
                self.definedPasses_forSnapShot.append(passAnnotation)
                self.definePasses.displayDefinedPass(passAnnotation, self.text_toDisplayPasses)


    def rb_define_pass(self):
        if self.directionSpeed_ofObjects:
            self.remove_directionSpeedOfObjects()  # remove previous annotations
        for player_js in self.texts:
            player_js.disconnect()
        self.definePasses.connect()


    def rb_drag_objects(self):
        if self.directionSpeed_ofObjects:
            self.remove_directionSpeedOfObjects()  # remove previous annotations
        self.definePasses.disconnect()
        for player_js in self.texts:
            player_js.connect()


    def scaleDraw(self):
        scale_value = self.scaleVariable.get()
        minute, sec_milisec = str(scale_value).split(".")
        sec_milisec_real = self.scale_timeInterval(int(sec_milisec), src=(0.0, 300.0), dst=(0.0, 18.0))
        sec, milisec = str(sec_milisec_real).split(".")
        minute_final, sec_final, milisec_final = self.time_adjust(minute, sec, milisec)

        self.currentTimeVariable.set("Time = %s.%s.%s" %(minute_final, sec_final, milisec_final))
        minute_final, sec_final, milisec_final = int(minute_final), int(sec_final), int(milisec_final)

        if self.trailAnnotation != None:
            self.trailAnnotation.remove(); del self.trailAnnotation; self.trailAnnotation = None
        try:
            self.visualizeCurrentPosition(1, minute_final, sec_final, milisec_final, None)
            self.currentTime_whenPause = (1, minute_final, sec_final, milisec_final)
        except KeyError:
            self.visualizeCurrentPosition(2, minute_final, sec_final, milisec_final, None)
            self.currentTime_whenPause = (2, minute_final, sec_final, milisec_final)


    def play(self):
        if self.directionSpeed_ofObjects: self.remove_directionSpeedOfObjects()
        self.text_toDisplayPasses.delete("1.0", END)
        self.pauseButtonClicked = False


        current_half, current_minute, current_second, current_milisecond = self.currentTime_whenPause
        time = Time(current_half, current_minute, current_second, current_milisecond)
        time.set_minMaxOfHalf(self.minMaxOfHalf)
        while not self.pauseButtonClicked:
            next_half, next_minute, next_second, next_milisecond = current_half, current_minute, current_second, current_milisecond
            chosenSkip = int(self.skipPlayVariable.get())
            for skipTimes in range(chosenSkip+1):
                next_time = time.next()
                next_half, next_minute, next_second, next_milisecond = next_time.half, next_time.minute, \
                                                                        next_time.second, next_time.mili_second
                if next_half not in self.minMaxOfHalf:
                    break
            #print next_half, next_minute, next_second, next_milisecond
            self.visualizeCurrentPosition(next_half, next_minute, next_second, next_milisecond, chosenSkip)
            self.currentTime_whenPause = (next_half, next_minute, next_second, next_milisecond)
            self.currentTimeVariable.set("Time = %s.%s.%s" %(next_minute, next_second, next_milisecond))
            chosenMotion = self.playVariable.get()
            if chosenMotion == "normal":
                tm.sleep(0.1)
            elif chosenMotion == "slow":
                tm.sleep(0.2)


    def pause(self):
        self.pauseButtonClicked = True
        current_half, current_minute, current_second, current_milisecond = self.currentTime_whenPause
        self.annotateDirectionSpeedOfObjects_forGivenTime(current_half, current_minute, current_second, current_milisecond)


    def remove_directionSpeedOfObjects(self):
        if self.directionSpeed_ofObjects:
            for i in self.directionSpeed_ofObjects:
                i.remove()
            del self.directionSpeed_ofObjects[:]
            self.canvas.draw()


    def remove_allDefinedPassesForSnapShot(self):
        if self.displayPasses_forSnapShot:
            for i in self.definedPasses_forSnapShot:
                i.remove()
            del self.definedPasses_forSnapShot[:]
            self.canvas.draw()


    def annotateDirectionSpeedOfObjects_forGivenTime(self, half, minute, second, milisecond):
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getDirectionOfObjects_forGivenTime(
            half, minute, second, milisecond)
        teams = self.getSpeedOfObjects_forGivenTime(half, minute, second, milisecond)
        for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
            for player in team:
                currentX, nextX = team[player][0]
                currentY, nextY = team[player][1]
                speed = teams[index][player]

                lengthX = (nextX - currentX) * speed
                nextX = lengthX + currentX

                lengthY = (nextY - currentY) * speed
                nextY = lengthY + currentY

                default_arrow_size = 2
                if lengthX >= 0: nextX += default_arrow_size
                else: nextX -= default_arrow_size
                if lengthY >= 0: nextY += default_arrow_size
                else: nextY -= default_arrow_size

                passAnnotation = self.ax.annotate('', xy=(nextX,nextY), xycoords='data', xytext=(currentX,currentY),
                                                  textcoords='data',size=20, va="center", ha="center", arrowprops=dict(
                        arrowstyle="simple", connectionstyle="arc3",
                        fc="cyan", ec="b", lw=2))
                self.directionSpeed_ofObjects.append(passAnnotation)
        self.canvas.draw()


    def getDirectionOfObjects_forGivenTime(self, half, minute, sec, milisec): # should be rewritten
        time = Time(half, minute, sec, milisec)
        time.set_minMaxOfHalf(self.minMaxOfHalf)
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = \
                self.getObjectsCoords_forGivenTime(half, minute, sec, milisec)
        teams = [homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]
        for team in teams:
            for player in team:
                coordX, coordY = team[player]
                team[player] = ([coordX],[coordY])
        next_time = time.next()
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = \
                self.getObjectsCoords_forGivenTime(next_time.half, next_time.minute,
                                                   next_time.second, next_time.mili_second)
        for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for player in team:
                    try:
                        coordX, coordY= team[player]
                        x, y = teams[index][player][0], teams[index][player][1]
                        x.append(coordX), y.append(coordY)
                    except:
                        pass
        return (team for team in teams)


    def getSpeedOfObjects_forGivenTime(self, half, minute, sec, milisec): # should be rewritten
        time = Time(half, minute, sec, milisec)
        time.set_minMaxOfHalf(self.minMaxOfHalf)
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = \
                self.getObjectsCoords_forGivenTime(half, minute, sec, milisec)
        teams = [homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]
        for team in teams:
            for player in team:
                coordX, coordY = team[player]
                team[player] = ([coordX],[coordY])
        for i in range(5):
            pre_time = time.back()
            homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = \
                self.getObjectsCoords_forGivenTime(pre_time.half, pre_time.minute, pre_time.second, pre_time.mili_second)
            for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for player in team:
                    coordX, coordY= team[player]
                    x, y = teams[index][player][0], teams[index][player][1]
                    x.append(coordX), y.append(coordY)
        for team in teams:
            for player in team:
                coordsX, coordsY = team[player]
                total = 0.0
                for i in range(5):
                    try:
                        x_current, y_current = coordsX[i], coordsY[i]
                        x_previous, y_previous = coordsX[i+1], coordsY[i+1]
                        total += math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                    except:
                        pass
                team[player] = total
        return teams


    def getObjectsCoords_forGivenTime(self, half, minute, sec, milisec):
        coordinatesData_current = self.coordinatesData_byTime[half][minute][sec][milisec]
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = [], [], [], []
        for object_info in coordinatesData_current:
            player_base = Player_base(object_info)
            q = player_base.getObjectType()
            if q in [0,3]: homeTeamPlayers.append(player_base)
            elif q in [1,4]: awayTeamPlayers.append(player_base)
            elif q in [2,6,7,8,9]: referees.append(player_base)
            else: unknownObjects.append(player_base)
        return (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)


    def setJerseyNumbers_forGivenObjects(self, homeTeamPlayers, awayTeamPlayers, referees, unknownObjects):
        BoxStyle._style_list["circle"] = CircleStyle
        colors = ["blue", "red", "yellow", "black"]
        for index, players in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
            for player_base in players:
                player_js = self.ax.text(player_base.getPositionX(), player_base.getPositionY(), player_base.getJerseyNumber(),
                                color="w", fontsize=(11 if len(str(player_base.getJerseyNumber()))==1 else 10), picker=True,
                                zorder=1, bbox=dict(boxstyle="circle,pad=0.3", fc=colors[index], ec=colors[index], alpha=0.5))
                player_js.object_type = player_base.getObjectType()
                player_js.object_id = player_base.getObjectID()
                dr = DraggableText(player_js)
                self.texts.append(dr)
        self.definePasses = DraggablePass(self.ax, self.texts)
        self.definePasses.set_effectivenessWithComponentsLabel_forChosenPoint(self.effec_withCompVariable_forChosenPoint)
        self.definePasses.set_passDisplayer(self.text_toDisplayPasses)
        self.definePasses.set_variables(self.heatmapTypeVariable, self.resolutionLevelVariable,
                                        self.componentsOfEffectivenessVariable)

        for i in self.texts:
            i.set_passDisplayer(self.text_toDisplayPasses)
            i.set_definedPasses(self.definePasses.definedPasses)
            i.set_coordinatesOfObjects(self.texts)


    def getObjectsCoords_forSnapShot(self):
        teams = {(0.0, 0.0, 1.0, 0.5): "home", (1.0, 0.0, 0.0, 0.5): "away",
                      (1.0, 1.0, 0.0, 0.5): "referee", (0.0, 0.0, 0.0, 0.5): "unknown"}
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = dict(), dict(), dict(), dict()
        for object_info in self.texts:
            q = object_info.point
            positionX, positionY = q.get_position()
            team = teams[q.get_bbox_patch().get_facecolor()]
            jersey_number = q.get_text()
            jersey_number, positionX, positionY = int(jersey_number), float(positionX), float(positionY)
            if team  == "home":
                homeTeamPlayers[jersey_number] = [positionX, positionY]
            elif team == "away":
                awayTeamPlayers[jersey_number] = [positionX, positionY]
            elif team == "referee":
                referees[jersey_number] = [positionX, positionY]
            else:
                unknownObjects[jersey_number] = [positionX, positionY]
        return (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)


    def remove_previousJerseyNumbers(self):
        for player_js in self.texts:
            player_js.point.remove()
        del self.texts[:]

        if self.definePasses != None:
            for i in self.definePasses.definedPasses:
                i.remove(); del i


    def visualizeCurrentPosition(self, half, minute, sec, milisec, skip_times):
        self.remove_previousJerseyNumbers()

        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = \
            self.getObjectsCoords_forGivenTime(half, minute, sec, milisec)

        self.setJerseyNumbers_forGivenObjects(homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)

        self.annotate_currentEvent(half, minute, sec, milisec, homeTeamPlayers, awayTeamPlayers, skip_times)

        self.canvas.draw()
        #self.master.update()
        self.frame.update()


    def detectParticularPlayer(self, js, x, y):
        for plyr in self.texts:
            x1, y1 = plyr.point.get_position()
            js1 = plyr.point.get_text()
            if x1==x and y1==y and int(js1)==js:
                return plyr.point


    def annotate_currentEvent(self, half, minute, second, milisec, homeTeamPlayers, awayTeamPlayers, skip_times): # not completed
        eventData_current = self.get_currentEventData(half, minute, second, milisec)
        current_teamName, current_js, current_eventID = eventData_current[0]
        homeTeamName, awayTeamName = self.teamNames
        player_current = None
        xBall, yBall = None, None
        try:
            if current_teamName == homeTeamName:
                xBall, yBall = homeTeamPlayers[current_js]
                player_current = self.detectParticularPlayer(current_js, xBall, yBall)
            elif current_teamName == awayTeamName:
                xBall, yBall = awayTeamPlayers[current_js]
                player_current = self.detectParticularPlayer(current_js, xBall, yBall)
        except KeyError:
            print "missing data"

        self.count_forEventAndPassEffect += 1
        if self.count_forEventAndPassEffect == 5:
            if self.eventAnnotation != None: self.eventAnnotation.remove(); del self.eventAnnotation; self.eventAnnotation = None
            if self.passEffectivenessAnnotation != None: self.passEffectivenessAnnotation.remove(); del self.passEffectivenessAnnotation; self.passEffectivenessAnnotation = None
            self.count_forEventAndPassEffect = 0
        if self.passAnnotation != None: self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None

        if current_eventID != 1:
            if self.trailAnnotation!=None: self.trailAnnotation.remove(); del self.trailAnnotation; self.trailAnnotation = None
            if self.ballAnnotation!=None: self.ballAnnotation.remove(); del self.ballAnnotation; self.ballAnnotation = None
            self.eventAnnotation = self.ax.annotate(self.event_id_explanation[current_eventID], xy=(52.5,32.5),  xycoords='data',
                                                    va="center", ha="center", xytext=(0, 0), textcoords='offset points', size=20,
                                                    bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5)))
        else:
            eventData_previous = self.get_previousEventData(half, minute, second, milisec, skip_times)
            previous_teamName, previous_js, previous_eventID = eventData_previous[0]
            if previous_teamName != current_teamName or previous_js != current_js:
                if self.trailAnnotation!=None: self.trailAnnotation.remove(); del self.trailAnnotation; self.trailAnnotation = None
                if self.ballAnnotation!=None: self.ballAnnotation.remove(); del self.ballAnnotation; self.ballAnnotation = None
                player_previous = None
                previous_xBall, previous_yBall = None, None
                try:
                    if previous_teamName == homeTeamName:
                        previous_xBall, previous_yBall = homeTeamPlayers[previous_js]
                        player_previous = self.detectParticularPlayer(previous_js, previous_xBall, previous_yBall)
                    elif previous_teamName == awayTeamName:
                        previous_xBall, previous_yBall = awayTeamPlayers[previous_js]
                        player_previous  = self.detectParticularPlayer(previous_js, previous_xBall, previous_yBall)
                except KeyError:
                    print "missing data 2"
                if (previous_eventID not in [4, 12]) and previous_xBall != None and xBall != None:
                    self.passAnnotation = self.ax.annotate('', xy=(.5, .5), xycoords=(player_current), xytext=(.5, .5),
                        textcoords=(player_previous), size=20, arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none", connectionstyle="arc3"))

                    #HeatMap(self.ax).draw(self.passAnnotation)

                    effectiveness = self.definePasses.displayDefinedPass(self.passAnnotation, self.text_toDisplayPasses)

                    current_coordX, current_coordY = player_current.get_position()
                    pre_coordX, pre_coordY = player_previous.get_position()
                    ultX, ultY = ((current_coordX + pre_coordX) / 2.), ((current_coordY + pre_coordY) / 2.)
                    self.passEffectivenessAnnotation = self.ax.annotate(("effectiveness %.2f"%(effectiveness)), xy=(ultX-10, ultY),
                        xycoords="data", va="center", ha="center", xytext=(ultX-10, ultY), textcoords="offset points",
                        size=10, bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5)))
            else:
                if self.trailAnnotation == None:
                    self.entire_trailX, self.entire_trailY = [],[]
                    self.entire_trailX.append(xBall), self.entire_trailY.append(yBall)
                    self.trailAnnotation, = self.ax.plot(self.entire_trailX, self.entire_trailY, "--", color="yellow")
                    self.ballAnnotation, = self.ax.plot(xBall, yBall, "o", markersize=26,mfc="none",markeredgewidth=3.0,markeredgecolor="yellow")
                else:
                    self.entire_trailX.append(xBall), self.entire_trailY.append(yBall)
                    self.trailAnnotation.set_data(self.entire_trailX, self.entire_trailY)
                    self.ballAnnotation.set_data(xBall, yBall)


    def get_currentEventData(self, half, minute, second, milisec):
        try:
            eventData_current = self.eventData_byTime[half][minute][second]
            return eventData_current
        except KeyError:
            time = Time(half, minute, second, milisec)
            back_time = time.back()
            #print back_time.half, back_time.minute, back_time.second, back_time.mili_second
            return self.get_currentEventData(back_time.half, back_time.minute, back_time.second, back_time.mili_second)


    def get_previousEventData(self, half, minute ,second, milisec, chosenSkip):
        if chosenSkip == None: chosenSkip = 0
        time = Time(half, minute, second, milisec)
        back_half, back_minute, back_second, back_milisec = time.half, time.minute, time.second, time.mili_second
        for skipTimes in range(chosenSkip+1):
            back_time = time.back()
            back_half, back_minute, back_second, back_milisec = back_time.half, back_time.minute, back_time.second, back_time.mili_second
        eventData_previous = self.get_currentEventData(back_half, back_minute, back_second, back_milisec)
        return eventData_previous


    def time_adjust(self, minute, sec, milisec):
        if len(milisec) == 1:
            return (minute), (sec), (milisec)
        elif milisec[0] =="9":
            return (minute), str(int(sec)+1), str(0)
        else:
            return (minute), (sec), (str(round(int(milisec),-1))[0])


    def scale_timeInterval(self, val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


    def quit(self):
        self.master.quit()     # stops mainloop
        self.master.destroy()


    def __str__(self):
        pass
