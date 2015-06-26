__author__ = 'emrullah'

class Time(object):

    def __init__(self, half=1, minute=0, second=0, millisecond=0):
        self.half = half
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

        self.minMaxOfHalf = {1: ((0,0,0), (44,59,8)), 2: ((45,0,0), (89,59,8))}
        self.minMaxOfHalf_inMilliseconds = {1: (0, 26998), 2: (27000, 53998)}


    @staticmethod
    def compute_minMaxOfHalf_inMilliseconds(minMaxOfHalf):
        minMaxOfHalf_inMilliseconds = {}
        for half in minMaxOfHalf:
            min_minute, min_second, min_millisecond = minMaxOfHalf[half][0]
            max_minute, max_second, max_millisecond = minMaxOfHalf[half][1]
            half_min_milliseconds = (min_minute * 60 + min_second) * 10 + min_millisecond
            half_max_milliseconds = (max_minute * 60 + max_second) * 10 + max_millisecond
            minMaxOfHalf_inMilliseconds[half] = (half_min_milliseconds, half_max_milliseconds)
        return minMaxOfHalf_inMilliseconds


    def set_minMaxOfHalf(self, minMaxOfHalf):
        self.minMaxOfHalf = minMaxOfHalf
        self.minMaxOfHalf_inMilliseconds = self.compute_minMaxOfHalf_inMilliseconds(minMaxOfHalf)


    @staticmethod
    def time_to_milliseconds(time):
        seconds = time.minute * 60 + time.second
        millisecond = seconds * 10 + time.millisecond
        return millisecond


    @staticmethod
    def time_display(time):
        return "Time = %d_%02d:%02d:%02d" % (time.half, time.minute, time.second, time.millisecond*10)


    @staticmethod
    def milliseconds_to_time_base(milliseconds):
        seconds, millisecond = divmod(milliseconds, 10)
        minute, second = divmod(seconds, 60)
        return minute, second, millisecond


    def milliseconds_to_time(self, milliseconds):
        seconds, self.millisecond = divmod(milliseconds, 10)
        self.minute, self.second = divmod(seconds, 60)

        half_min_milliseconds, half_max_milliseconds = self.minMaxOfHalf_inMilliseconds[self.half]
        if milliseconds < half_min_milliseconds:
            if self.half != 1:
                self.half -= 1
        elif milliseconds > half_max_milliseconds:
            if (self.half+1) in self.minMaxOfHalf:
                self.half += 1
                temp_half_min_milliseconds = self.minMaxOfHalf_inMilliseconds[self.half][0]
                final_milliseconds = milliseconds - (half_max_milliseconds - temp_half_min_milliseconds) - 2
                self.minute, self.second, self.millisecond = self.milliseconds_to_time_base(final_milliseconds)
        time = Time(self.half, self.minute, self.second, self.millisecond)
        time.set_minMaxOfHalf(self.minMaxOfHalf)
        return time


    def get_in_milliseconds(self):
        initial_time_in_milliseconds = {1: (0, 26998), 2: (27000, 53998)}
        milliseconds = 0
        for half in range(1, self.half):
            init_min_milliseconds, init_max_milliseconds = initial_time_in_milliseconds[half]
            min_milliseconds, max_milliseconds = self.minMaxOfHalf_inMilliseconds[half]
            final_init_difference = init_max_milliseconds - init_min_milliseconds
            final_temp_difference = max_milliseconds - min_milliseconds
            milliseconds = final_temp_difference - final_init_difference
        return self.time_to_milliseconds(self) + milliseconds


    def next(self):
        total_milliseconds = self.time_to_milliseconds(self)
        return self.milliseconds_to_time(total_milliseconds+2)


    def back(self):
        total_milliseconds = self.time_to_milliseconds(self)
        if total_milliseconds <= 0:
            return Time()
        return self.milliseconds_to_time(total_milliseconds-2)


    def __eq__(self, other):
        return (self.half, self.minute, self.second, self.millisecond) == \
               (other.half, other.minute, other.second, other.millisecond)


    def __ne__(self, other):
        return not (self.half, self.minute, self.second, self.millisecond) == \
               (other.half, other.minute, other.second, other.millisecond)


    def __str__(self):
        return "half = %s\n" \
               "minute = %s\n" \
               "second = %s\n" \
               "millisecond = %s" % (self.half, self.minute, self.second, self.millisecond)

