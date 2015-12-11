__author__ = 'emrullah'


class EventAnnotationManager:

    def __init__(self, ax):
        self.ax = ax

        self.pass_event_annotations = []
        self.event_title_annotation = None

        self.effectiveness_annotation = None
        self.effectiveness_count = 0


    def updatePassEventAnnotations(self):
        if self.pass_event_annotations != []:
            temp_pass_event_annotations = []
            for pass_event_annotation in self.pass_event_annotations[-3:-1]:
                temp_pass_event_annotation = self.ax.annotate('', xy=pass_event_annotation.xy, xytext=pass_event_annotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=pass_event_annotation.arrowprops["fc"],
                                                  ec=pass_event_annotation.arrowprops["ec"], alpha=0.5))
                temp_pass_event_annotations.append(temp_pass_event_annotation)

            c_pass_annotation = self.pass_event_annotations[-1]
            temp_pass_event_annotations.append(self.ax.annotate('', xy=c_pass_annotation.xy, xytext=c_pass_annotation.xytext,
                         size=20, arrowprops=dict(arrowstyle="->", fc=c_pass_annotation.arrowprops["fc"],
                                                  ec=c_pass_annotation.arrowprops["ec"], alpha=1.0)))

            for passAnnotation in self.pass_event_annotations: passAnnotation.remove()
            self.pass_event_annotations = temp_pass_event_annotations


    @staticmethod
    def annotateAnalysisResults(canvas, ax, results):
        result_annotation = ax.annotate(results,
                                        xy=(52.5,32.5),
                                        xycoords='data',
                                        va="center",
                                        ha="center",
                                        xytext=(0, 0),
                                        textcoords='offset points',
                                        size=13,
                                        bbox=dict(
                                            boxstyle="round",
                                            fc=(1.0, 0.7, 0.7),
                                            ec=(1., .5, .5),
                                            alpha=0.5))
        canvas.draw()
        return result_annotation


    def annotateEventTitle(self, current_event):
        self.event_title_annotation = self.ax.annotate(current_event.event_name,
                                                       xy=(52.5,32.5),
                                                       xycoords='data',
                                                       va="center",
                                                       ha="center",
                                                       xytext=(0, 0),
                                                       textcoords='offset points',
                                                       size=20,
                                                       bbox=dict(
                                                           boxstyle="round",
                                                           fc=(1.0, 0.7, 0.7),
                                                           ec=(1., .5, .5),
                                                           alpha=0.5))


    def annotatePassEvent(self, pass_event):
        pass_event_annotation = self.ax.annotate('',
                                                 xy=pass_event.pass_target.get_position(),
                                                 xytext=pass_event.pass_source.get_position(),
                                                 size=20,
                                                 arrowprops=dict(
                                                     arrowstyle="->",
                                                     fc=pass_event.pass_source.getObjectColor(),
                                                     ec=pass_event.pass_source.getObjectColor(),
                                                     alpha=1.0))
        self.pass_event_annotations.append(pass_event_annotation)


    def annotateEffectiveness(self, pass_event, effectiveness):
        ultX = ((pass_event.pass_target.getX() + pass_event.pass_source.getX()) / 2.)
        ultY = ((pass_event.pass_target.getY() + pass_event.pass_source.getY()) / 2.)

        self.effectiveness_annotation = self.ax.annotate(("effectiveness %.2f"%effectiveness),
                                                         xy=(ultX-10, ultY),
                                                         xycoords="data",
                                                         va="center",
                                                         ha="center",
                                                         xytext=(ultX-10, ultY),
                                                         textcoords="offset points",
                                                         size=10,
                                                         bbox=dict(
                                                             boxstyle="round",
                                                             fc=(1.0, 0.7, 0.7),
                                                             ec=(1., .5, .5),
                                                             alpha=0.5))
        self.effectiveness_count = 0


    def updateEffectivenessCount(self):
        if self.effectiveness_count < 5: self.effectiveness_count += 1
        if self.effectiveness_count == 5: self.removeEffectivenessAnnotation()


    def removeEventTitleAnnotation(self):
        if self.event_title_annotation != None:
            self.event_title_annotation.remove()
            del self.event_title_annotation
            self.event_title_annotation = None


    def removePassEventAnnotations(self):
        if self.pass_event_annotations != []:
            for pass_event_annotation in self.pass_event_annotations:
                pass_event_annotation.remove()
            del self.pass_event_annotations[:]


    def removeEffectivenessAnnotation(self):
        if self.effectiveness_annotation != None:
            self.effectiveness_annotation.remove()
            del self.effectiveness_annotation
            self.effectiveness_annotation = None


    def __str__(self):
        pass
