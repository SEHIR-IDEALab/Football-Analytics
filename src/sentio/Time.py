__author__ = 'emrullah'

class Time(object):

    def __init__(self, half=1, milliseconds=0):
        self.half = half
        self.milliseconds = milliseconds

        self.converted_to_time = False


    @staticmethod
    def time_to_milliseconds(time):
        seconds = time.minute * 60 + time.second
        millisecond = seconds * 10 + time.millisecond
        return millisecond


    @staticmethod
    def toMilliseconds((minute, second, millisecond)):
        seconds = minute * 60 + second
        milliseconds = seconds * 10 + millisecond
        return milliseconds


    @staticmethod
    def milliseconds_to_time(milliseconds):
        seconds, millisecond = divmod(milliseconds, 10)
        minute, second = divmod(seconds, 60)
        return minute, second, millisecond


    def get_in_time(self):
        return Time.milliseconds_to_time(self.milliseconds)


    def convertToTime(self):
        self.converted_to_time = True
        self.minute, self.second, self.millisecond = Time.milliseconds_to_time(self.milliseconds)


    @staticmethod
    def time_display(time):
        time.convertToTime()
        return "Time = %d_%02d:%02d:%02d" % (time.half, time.minute, time.second, time.millisecond*10)


    def next(self):
        self.milliseconds += 2


    def back(self):
        self.milliseconds -= 2


    def __str__(self):
        if self.converted_to_time:
            return "half = %s\n" \
                   "minute = %s\n" \
                   "second = %s\n" \
                   "millisecond = %s" % (self.half, self.minute, self.second, self.millisecond)
        else:
            return "half: %s\n" \
                   "milliseconds = %s" % (self.half, self.milliseconds)

