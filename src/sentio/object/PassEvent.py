__author__ = 'doktoray'


class PassEvent:

    def __init__(self, pass_source, pass_target, teams):
        self.pass_source = pass_source
        self.pass_target = pass_target
        self.teams = teams


    def getTeams(self):
        return self.teams


    def setPassSource(self, pass_source):
        self.pass_source = pass_source


    def setPassTarget(self, pass_target):
        self.pass_target = pass_target


    def getPassSource(self):
        return self.pass_source


    def getPassTarget(self):
        return self.pass_target


    def __str__(self):
        return "%s\n%s" %(self.pass_source, self.pass_target)