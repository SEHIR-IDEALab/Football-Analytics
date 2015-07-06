__author__ = 'doktoray'


class Teams:

    def __init__(self, home_team, away_team, referees, unknowns):
        self.home_team = home_team
        self.away_team = away_team
        self.referees = referees
        self.unknowns = unknowns


    def getPlayers(self):
        return self.home_team.getTeamPlayers() + self.away_team.getTeamPlayers()


    def __str__(self):
        return "%s\n%s\n%s\n%s" %(self.home_team, self.away_team, self.referees, self.unknowns)
