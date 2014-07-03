# coding=utf-8

from Tkconstants import VERTICAL, Y, LEFT, END, NE
import Tkinter as Tk
import time as tm
import math
import tkFileDialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.patches import BoxStyle
import matplotlib.pyplot as plt
import numpy
from src.sentio.CircleStyle import CircleStyle
from src.sentio.DraggablePass import DraggablePass
from src.sentio.DraggableText import DraggableText
from src.sentio.Player_base import Player_base
from src.sentio.SnapShot import SnapShot
from src.sentio.Time import Time

__author__ = 'emrullah'


class Visualization(object):
    def __init__(self, sentio, teamNames):
        self.sentio = sentio
        self.teamNames = teamNames

        self.coordinatesData_byTime = self.sentio.getCoordinateData_byTime()
        self.event_id_explanation = self.sentio.get_ID_Explanation()


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
        displayChosenPoint = Tk.Label(master=self.frame, textvariable=self.effec_withCompVariable_forChosenPoint,
                                      justify=LEFT).pack()

        button_scaleDraw = Tk.Button(master=self.frame, text='Draw', command=self.scaleDraw).pack(side="left")
        button_play = Tk.Button(master=self.frame, text='Play', command=self.play).pack(side="left")

        self.pauseButtonClicked = False
        self.directions_of_objects = list()
        self.currentTime_whenPause = Time(1,0,0,0)

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

        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side='top', fill='both', expand=1)

        self.ax = fig.add_subplot(111)
        im = plt.imread('source/background.png')
        self.ax.imshow(im, zorder=0, extent=[-6.5, 111.5, -1.5, 66.5])
        self.ax.grid()
        self.ax.axes.invert_yaxis()
        self.ax.set_xticks(numpy.arange(-5, 120, 5))
        self.ax.set_yticks(numpy.arange(-5, 75, 5))

        self.definePasses = None
        self.definedPasses_forSnapShot = list()

        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(Time(1,0,0,0))
        self.setJerseyNumbers_forGivenObjects(homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)

        self.trailAnnotation, self.eventAnnotation, self.passAnnotation, self.passEffectivenessAnnotation = None, None, None, None
        self.passEffectiveness_count = 0

        a,b,c,d, = plt.plot([],[],"bo",[],[],"ro",[],[],"yo",[],[],"ko", markersize=15)
        self.ax.legend([a,b,c,d], [self.teamNames[0].decode("utf-8"), self.teamNames[1].decode("utf-8"), 'Referees',
                                   'Unknown Objects'], numpoints=1, fontsize=12, bbox_to_anchor=(0., 1.02, 1., .102),
                       loc=3, ncol=4, mode="expand", borderaxespad=0.5)

        self.frame.pack()
        self.master.config(menu=menubar)
        self.master.mainloop()


    def saveSnapShot(self):
        current_time = self.currentTime_whenPause
        defined_passes = self.definePasses.definedPasses
        directions = self.getDirectionOfObjects_forGivenTime(current_time)
        speeds = self.getSpeedOfObjects_forGivenTime(current_time)

        snapShot = SnapShot()
        snapShot.saveSnapShot(self.teamNames, self.texts, defined_passes, directions, speeds)


    def loadSnapShot(self):
        filename = tkFileDialog.askopenfilename(initialdir="../../SampleScenarios")
        if filename:
            self.remove_directionSpeedOfObjects()
            self.remove_allDefinedPassesForSnapShot()
            self.remove_eventAnnotation()
            self.remove_passAnnotation()
            self.remove_trailAnnotation()
            self.remove_passEffectivenessAnnotation()
            self.remove_previousJerseyNumbers()
            self.text_toDisplayPasses.delete("1.0", END)

            snapShot = SnapShot()
            (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects), list_of_directions = \
                snapShot.loadSnapShot(filename, self.ax)

            self.directions_of_objects.extend(list_of_directions)
            self.setJerseyNumbers_forGivenObjects(homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)

            all_defined_passes = snapShot.displayAllPasses(filename, self.ax, self.texts, self.text_toDisplayPasses)
            self.definedPasses_forSnapShot.extend(all_defined_passes)

            self.currentTimeVariable.set("Time = %s.%s.%s" %("-", "-", "-"))

            self.canvas.draw()
            self.frame.update()


    def rb_define_pass(self):
        if self.directions_of_objects:
            self.remove_directionSpeedOfObjects()
        for player_js in self.texts:
            player_js.disconnect()
        self.definePasses.connect()


    def rb_drag_objects(self):
        if self.directions_of_objects:
            self.remove_directionSpeedOfObjects()
        self.definePasses.disconnect()
        for player_js in self.texts:
            player_js.connect()


    def pause(self):
        self.pauseButtonClicked = True
        current_time = self.currentTime_whenPause
        self.annotateDirectionSpeedOfObjects_forGivenTime(current_time)


    def play(self):
        self.remove_allDefinedPassesForSnapShot()
        if self.directions_of_objects: self.remove_directionSpeedOfObjects()
        self.text_toDisplayPasses.delete("1.0", END)
        self.pauseButtonClicked = False

        current_time = self.currentTime_whenPause
        current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        while not self.pauseButtonClicked:
            next_time = current_time
            chosenSkip = int(self.skipPlayVariable.get())
            for skipTimes in range(chosenSkip+1):
                next_time = current_time.next()
                if next_time.half not in self.sentio.minMaxOfHalf:
                    break

            self.visualizeCurrentPosition(next_time, chosenSkip)
            self.currentTime_whenPause = next_time
            self.currentTimeVariable.set("Time = %s.%s.%s" %(next_time.minute, next_time.second, next_time.mili_second))

            chosenMotion = self.playVariable.get()
            if chosenMotion == "normal": tm.sleep(0.1)
            elif chosenMotion == "slow": tm.sleep(0.2)


    def visualizeCurrentPosition(self, time, skip_times):
        self.remove_previousJerseyNumbers()

        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(time)
        self.setJerseyNumbers_forGivenObjects(homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)
        self.annotate_currentEvent(time, homeTeamPlayers, awayTeamPlayers, skip_times)

        self.canvas.draw()
        self.frame.update()


    def annotate_currentEvent_base(self, event_data, homeTeamPlayers, awayTeamPlayers):
        homeTeamName, awayTeamName = self.teamNames
        teamName, js, eventID = event_data[0]
        player = None
        xBall, yBall = None, None
        try:
            if teamName == homeTeamName:
                player_base = homeTeamPlayers[js]
                xBall, yBall = player_base.get_position()
            elif teamName == awayTeamName:
                player_base = awayTeamPlayers[js]
                xBall, yBall = player_base.get_position()
            player = self.detectParticularPlayer(js, xBall, yBall)
        except KeyError:
            print "missing data"
        return (player, eventID)


    def detectParticularPlayer(self, js, x, y):
        for plyr in self.texts:
            x1, y1 = plyr.point.get_position()
            js1 = plyr.point.get_text()
            if x1==x and y1==y and int(js1)==js:
                return plyr.point


    def annotate_currentEvent(self, time, homeTeamPlayers, awayTeamPlayers, skip_times): # not completed
        eventData_current = self.sentio.get_currentEventData(time)
        player_current, eventID_current = self.annotate_currentEvent_base(eventData_current,
                                                                          homeTeamPlayers, awayTeamPlayers)
        if self.passEffectiveness_count != 0:
            self.passEffectiveness_count += 1
            if self.passEffectiveness_count == 5: self.remove_passEffectivenessAnnotation()
        self.remove_passAnnotation()
        self.remove_eventAnnotation()

        if eventID_current != 1:
            self.remove_trailAnnotation()
            self.eventAnnotation = self.ax.annotate(self.event_id_explanation[eventID_current], xy=(52.5,32.5),  xycoords='data',
                                                    va="center", ha="center", xytext=(0, 0), textcoords='offset points', size=20,
                                                    bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5), alpha=0.5))
        else:
            eventData_previous = self.sentio.get_previousEventData(time, skip_times)
            player_previous, eventID_previous = self.annotate_currentEvent_base(eventData_previous,
                                                                                homeTeamPlayers, awayTeamPlayers)
            if player_previous != player_current:
                self.remove_trailAnnotation()
                self.passAnnotation = self.ax.annotate('', xy=(.5, .5), xycoords=(player_current), xytext=(.5, .5),
                    textcoords=(player_previous), size=20, arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                                                           connectionstyle="arc3"))
                effectiveness = self.definePasses.displayDefinedPass(self.passAnnotation, self.text_toDisplayPasses)

                ultX = ((player_current.get_position()[0] + player_previous.get_position()[0]) / 2.)
                ultY = ((player_current.get_position()[1] + player_previous.get_position()[1]) / 2.)
                self.remove_passEffectivenessAnnotation()
                self.passEffectivenessAnnotation = self.ax.annotate(("effectiveness %.2f"%(effectiveness)),
                    xy=(ultX-10, ultY), xycoords="data", va="center", ha="center", xytext=(ultX-10, ultY),
                    textcoords="offset points", size=10, bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7),
                                                                   ec=(1., .5, .5), alpha=0.5))
                self.passEffectiveness_count = 1
            else:
                if self.trailAnnotation == None:
                    self.entire_trailX, self.entire_trailY = [player_current.get_position()[0]],[player_current.get_position()[1]]
                    self.trailAnnotation, = self.ax.plot(self.entire_trailX, self.entire_trailY, "--", color="yellow")
                else:
                    self.entire_trailX.append(player_current.get_position()[0]), self.entire_trailY.append(player_current.get_position()[1])
                    self.trailAnnotation.set_data(self.entire_trailX, self.entire_trailY)


    def annotateDirectionSpeedOfObjects_forGivenTime(self, time):
        list_of_directions_of_objects = self.getDirectionOfObjects_forGivenTime(time)
        teams = self.getSpeedOfObjects_forGivenTime(time)
        for index, team in enumerate(list_of_directions_of_objects):
            for js in team:
                player = team[js]
                currentX, nextX = player.getPositionX()
                currentY, nextY = player.getPositionY()
                speed = teams[index][js]

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
                self.directions_of_objects.append(passAnnotation)
        self.canvas.draw()


    def getDirectionOfObjects_forGivenTime(self, time): # should be rewritten
        current_time = time
        current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(current_time)
        teams = [homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]
        for team in teams:
            for js in team:
                player_base = team[js]
                coordX, coordY = player_base.get_position()
                player_base.set_position(([coordX],[coordY]))
        next_time = current_time.next()
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(next_time)
        for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for js in team:
                    try:
                        player_base = team[js]
                        coordX, coordY= player_base.get_position()
                        ult_player_base = teams[index][js]
                        x, y = ult_player_base.getPositionX(), ult_player_base.getPositionY()
                        x.append(coordX), y.append(coordY)
                    except:
                        pass
        return teams


    def getSpeedOfObjects_forGivenTime(self, time): # should be rewritten
        current_time = time
        current_time.set_minMaxOfHalf(self.sentio.minMaxOfHalf)
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(current_time)
        teams = [homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]
        for team in teams:
            for js in team:
                player_base = team[js]
                coordX, coordY = player_base.get_position()
                player_base.set_position(([coordX],[coordY]))
        for i in range(5):
            pre_time = current_time.back()
            homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = self.getObjectsCoords_forGivenTime(pre_time)
            for index, team in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
                for js in team:
                    player_base = team[js]
                    coordX, coordY= player_base.get_position()
                    ult_player_base = teams[index][js]
                    x, y = ult_player_base.getPositionX(), ult_player_base.getPositionY()
                    x.append(coordX), y.append(coordY)
        for team in teams:
            for js in team:
                player_base = team[js]
                coordsX, coordsY = player_base.get_position()
                total = 0.0
                for i in range(5):
                    try:
                        x_current, y_current = coordsX[i], coordsY[i]
                        x_previous, y_previous = coordsX[i+1], coordsY[i+1]
                        total += math.sqrt(pow(x_current-x_previous,2) + pow(y_current-y_previous,2))
                    except:
                        pass
                team[js] = total
        return teams


    def getObjectsCoords_forGivenTime(self, time):
        coordinatesData_current = self.coordinatesData_byTime[time.half][time.minute][time.second][time.mili_second]
        homeTeamPlayers, awayTeamPlayers, referees, unknownObjects = {},{},{},{}
        for object_info in coordinatesData_current:
            player = Player_base(object_info)
            q = player.getObjectType()
            if q in [0,3]: homeTeamPlayers[player.getJerseyNumber()] = player
            elif q in [1,4]: awayTeamPlayers[player.getJerseyNumber()] = player
            elif q in [2,6,7,8,9]: referees[player.getJerseyNumber()] = player
            else: unknownObjects[player.getJerseyNumber()] = player
        return (homeTeamPlayers, awayTeamPlayers, referees, unknownObjects)


    def setJerseyNumbers_forGivenObjects(self, homeTeamPlayers, awayTeamPlayers, referees, unknownObjects):
        self.texts = list()
        BoxStyle._style_list["circle"] = CircleStyle
        colors = ["blue", "red", "yellow", "black"]
        for index, players in enumerate([homeTeamPlayers, awayTeamPlayers, referees, unknownObjects]):
            for js in players:
                player = players[js]
                #if player_base.getJerseyNumber() in range(1, 100): # this condition may be changed ***
                player_js = self.ax.text(player.getPositionX(), player.getPositionY(), player.getJerseyNumber(),
                                color="w", fontsize=(11 if len(str(player.getJerseyNumber()))==1 else 10), picker=True,
                                zorder=1, bbox=dict(boxstyle="circle,pad=0.3", fc=colors[index], ec=colors[index], alpha=0.5))
                player_js.object_type = player.getObjectType()
                player_js.object_id = player.getObjectID()
                player_js.jersey_number = player.getJerseyNumber()
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


    def remove_previousJerseyNumbers(self):
        for player_js in self.texts:
            player_js.point.remove()
        del self.texts[:]

        if self.definePasses != None:
            for i in self.definePasses.definedPasses:
                i.remove(); del i


    def remove_directionSpeedOfObjects(self):
        if self.directions_of_objects:
            for i in self.directions_of_objects:
                i.remove()
            del self.directions_of_objects[:]
            self.canvas.draw()


    def remove_allDefinedPassesForSnapShot(self):
        if self.definedPasses_forSnapShot:
            for i in self.definedPasses_forSnapShot:
                i.remove()
            del self.definedPasses_forSnapShot[:]
            self.canvas.draw()


    def remove_eventAnnotation(self):
        if self.eventAnnotation != None:
            self.eventAnnotation.remove(); del self.eventAnnotation; self.eventAnnotation = None


    def remove_passAnnotation(self):
        if self.passAnnotation != None:
            self.passAnnotation.remove(); del self.passAnnotation; self.passAnnotation = None


    def remove_passEffectivenessAnnotation(self):
        if self.passEffectivenessAnnotation != None:
            self.passEffectivenessAnnotation.remove(); del self.passEffectivenessAnnotation; self.passEffectivenessAnnotation = None


    def remove_trailAnnotation(self):
        if self.trailAnnotation!=None:
            self.trailAnnotation.remove(); del self.trailAnnotation; self.trailAnnotation = None


    def time_adjust(self, minute, sec, milisec):
        if len(milisec) == 1:
            return (minute), (sec), (milisec)
        elif milisec[0] =="9":
            return (minute), str(int(sec)+1), str(0)
        else:
            return (minute), (sec), (str(round(int(milisec),-1))[0])


    def scale_timeInterval(self, val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


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
            self.visualizeCurrentPosition(Time(1, minute_final, sec_final, milisec_final), None)
            self.currentTime_whenPause = Time(1, minute_final, sec_final, milisec_final)
        except KeyError:
            self.visualizeCurrentPosition(Time(2, minute_final, sec_final, milisec_final), None)
            self.currentTime_whenPause = Time(2, minute_final, sec_final, milisec_final)


    def quit(self):
        self.master.quit()     # stops mainloop
        self.master.destroy()


    def __str__(self):
        pass
