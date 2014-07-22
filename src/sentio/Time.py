__author__ = 'emrullah'

class Time(object):

    def __init__(self, half=1, minute=0, second=0, millisecond=0):
        self.half = half
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

        self.minMaxOfHalf = {1:[[0,0,0],[44,59,8]], 2:[[45,0,0],[89,59,8]]}


    def __sub__(self, other):
        first = self.time_to_milliseconds(self)
        second = self.time_to_milliseconds(other)
        result = abs(first-second)
        return self.int_to_time(result)


    def __add__(self, other):
        first = self.time_to_milliseconds(self)
        second = self.time_to_milliseconds(other)
        total = first + second
        return self.milliseconds_to_time_self(total)


    def set_minMaxOfHalf(self, minMaxOfHalf):
        self.minMaxOfHalf = minMaxOfHalf
        self.compute_minMaxOfHalf_inMilliseconds()


    @staticmethod
    def milliseconds_to_time(milliseconds):
        milliseconds = milliseconds * 2

        seconds, milliseconds = divmod(milliseconds, 10)
        minutes, seconds = divmod(seconds, 60)
        return Time(minute=minutes, second=seconds, millisecond=milliseconds)


    @staticmethod
    def time_to_milliseconds(time):
        seconds = time.minute * 60 + time.second
        millisecond = seconds * 10 + time.millisecond
        return millisecond


    @staticmethod
    def time_display(time):
        return "Time = %02d.%02d.%02d" % (time.minute, time.second, time.millisecond*10)


    def milliseconds_to_time_self(self, milliseconds):
        milliseconds = milliseconds *2

        seconds, self.millisecond = divmod(milliseconds, 10)
        self.minute, self.second = divmod(seconds, 60)

        if milliseconds < self.time_min:
            if self.half != 1:
                self.half -= 1
                self.minute, self.second, self.millisecond = self.minMaxOfHalf[self.half][1]
            else:
                self.minute, self.second, self.millisecond = self.minMaxOfHalf[self.half][0]
            time = Time(self.half, self.minute, self.second, self.millisecond)
            return time
        elif milliseconds > self.time_max:
            additional_milliseconds = milliseconds - self.time_max
            print additional_milliseconds
            self.half += 1
            self.minute, self.second, self.millisecond = self.minMaxOfHalf[self.half][0]
            time = Time(self.half, self.minute, self.second, self.millisecond) + self.milliseconds_to_time_self(additional_milliseconds)
            print time
            return time
        time = Time(self.half, self.minute, self.second, self.millisecond*2)
        return time


    def int_to_time(self, milliseconds):
        seconds, self.millisecond = divmod(milliseconds, 10)
        self.minute, self.second = divmod(seconds, 60)

        if milliseconds < self.time_min:
            if self.half != 1:
                self.half -= 1
                self.minute, self.second, self.millisecond = self.minMaxOfHalf[self.half][1]
            else:
                self.minute, self.second, self.millisecond = self.minMaxOfHalf[self.half][0]
        elif milliseconds > self.time_max:
            self.half += 1
            self.minute, self.second, self.millisecond = self.minMaxOfHalf[self.half][0]
        time = Time(self.half, self.minute, self.second, self.millisecond)
        time.set_minMaxOfHalf(self.minMaxOfHalf)
        return time


    def compute_minMaxOfHalf_inMilliseconds(self):
        max_minute, max_second, max_millisecond = self.minMaxOfHalf[self.half][1]
        min_minute, min_second, min_millisecond = self.minMaxOfHalf[self.half][0]
        time_max = Time(minute=max_minute, second=max_second, millisecond=max_millisecond)
        time_min = Time(minute=min_minute, second=min_second, millisecond=min_millisecond)
        self.time_min, self.time_max = self.time_to_milliseconds(time_min), self.time_to_milliseconds(time_max)


    def next(self):
        time = Time(half=self.half, minute=self.minute, second=self.second, millisecond=self.millisecond)
        total_milliseconds = self.time_to_milliseconds(time)
        return self.int_to_time(total_milliseconds+2)


    def back(self):
        time = Time(half=self.half, minute=self.minute, second=self.second, millisecond=self.millisecond)
        total_milliseconds = self.time_to_milliseconds(time)
        return self.int_to_time(total_milliseconds-2)


    def __str__(self):
        return "half = %s\n" \
               "minute = %s\n" \
               "second = %s\n" \
               "millisecond = %s" % (self.half, self.minute, self.second, self.millisecond)

