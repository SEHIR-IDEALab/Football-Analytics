__author__ = 'doktoray'


class GameEvent:
    def __init__(self, player, event_id, event_name):
        self.player = player
        self.event_id = event_id
        self.event_name = event_name

        self.pass_event = None


    def getEventID(self):
        return self.event_id


    def setPassEvent(self, current_pass):
        self.pass_event = current_pass


    def getPassEvent(self):
        return self.pass_event


    def isPassEvent(self):
        return self.pass_event != None


    def __str__(self):
        return "%s, %s, %s" % (self.player, self.event_id, self.event_name)

