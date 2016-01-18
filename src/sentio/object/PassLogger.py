from src.sentio import Parameters
from src.sentio.pass_evaluate.Pass import Pass

__author__ = 'emrullah'



class PassLogger:

    def __init__(self, logger):
        self.pass_evaluate = Pass()
        self.logger = logger


    def clear(self):
        self.logger.Clear()


    def display_effectiveness(self, coordinates, components):
        overall_risk, gain, pass_advantage, goal_chance, effectiveness = components

        self.logger.WriteText("\n(%.1f, %.1f)\n" %coordinates)
        self.logger.WriteText("overall_risk = %.2f\n" %overall_risk)
        if gain:
            self.logger.WriteText("gain = %.2f\n" %gain)
        if pass_advantage:
            self.logger.WriteText("pass_advantage = %.2f\n" %pass_advantage)
        if goal_chance:
            self.logger.WriteText("goal_chance = %.2f\n" %goal_chance)
        self.logger.WriteText("effectiveness = %.2f\n" %effectiveness)

        self.logger.SetInsertionPoint(0)


    def displayDefinedPass(self, defined_pass):
        p1 = defined_pass.pass_source
        p2 = defined_pass.pass_target

        self.pass_evaluate.teams = defined_pass.teams

        (overallRisk, gain, passAdvantage, pa_player, goalChance, effectiveness) = \
            self.pass_evaluate.effectiveness_withComponents(p1, p2,
                (self.gain_listener.GetValue(), self.effectiveness_listener.GetValue(),
                self.pass_advantage_listener.GetValue(), self.goal_chance_listener.GetValue()))

        if Parameters.IS_DEBUG_MODE_ON:
            (x1,y1) = p1.get_position(); (x2,y2) = p2.get_position()
            self.logger.WriteText("\n(%.1f, %.1f) --> (%.1f, %.1f)\n" %(x1,y1,x2,y2))
        else:
            self.logger.WriteText("\n")
        self.logger.WriteText("%s --> %s\n" %(p1.getJerseyNumber(), p2.getJerseyNumber()))
        self.logger.WriteText("overall_risk = %.2f\n" %overallRisk)
        if gain:
            self.logger.WriteText("gain = %.2f\n" %gain)
        if passAdvantage:
            self.logger.WriteText("pass_advantage = %.2f (%s)\n" %(passAdvantage, pa_player))
        if goalChance:
            self.logger.WriteText("goal_chance = %.2f\n" %goalChance)
        self.logger.WriteText("effectiveness = %.2f\n" %effectiveness)

        self.logger.SetInsertionPoint(0)

        return effectiveness


    def setEffectivenessCompListeners(self, gain_listener, effectiveness_listener,
                                      pass_advantage_listener, goal_chance_listener):
        self.gain_listener = gain_listener
        self.effectiveness_listener = effectiveness_listener
        self.pass_advantage_listener = pass_advantage_listener
        self.goal_chance_listener = goal_chance_listener


    def __str__(self):
        pass