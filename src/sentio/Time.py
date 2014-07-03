__author__ = 'emrullah'

class Time(object):

    def __init__(self, half=1, minute=0, second=0, mili_second=0):
        self.half = half
        self.minute = minute
        self.second = second
        self.mili_second = mili_second

        self.minMaxOfHalf = {1:[[0,0,0],[44,59,8]], 2:[[45,0,0],[89,59,8]]}


    def __sub__(self, other):
        first = self.time_to_int(self)
        second = self.time_to_int(other)
        result = abs(first-second)
        return self.int_to_time(result)


    def set_minMaxOfHalf(self, minMaxOfHalf):
        self.minMaxOfHalf = minMaxOfHalf
        self.compute_minMaxOfHalf_inMiliseconds()


    def time_to_int(self, time):
        seconds = time.minute * 60 + time.second
        mili_seconds = seconds * 10 + time.mili_second
        return mili_seconds


    def compute_minMaxOfHalf_inMiliseconds(self):
        max_minute, max_second, max_milisecond = self.minMaxOfHalf[self.half][1]
        min_minute, min_second, min_milisecond = self.minMaxOfHalf[self.half][0]
        time_max = Time(minute=max_minute, second=max_second, mili_second=max_milisecond)
        time_min = Time(minute=min_minute, second=min_second, mili_second=min_milisecond)
        self.time_min, self.time_max = self.time_to_int(time_min), self.time_to_int(time_max)


    def int_to_time(self, mili_seconds):
        seconds, self.mili_second = divmod(mili_seconds, 10)
        self.minute, self.second = divmod(seconds, 60)

        if mili_seconds < self.time_min:
            if self.half != 1:
                self.half -= 1
                self.minute, self.second, self.mili_second = self.minMaxOfHalf[self.half][1]
            else:
                self.minute, self.second, self.mili_second = self.minMaxOfHalf[self.half][0]
        elif mili_seconds > self.time_max:
            self.half += 1
            self.minute, self.second, self.mili_second = self.minMaxOfHalf[self.half][0]
        time = Time(self.half, self.minute, self.second, self.mili_second)
        time.set_minMaxOfHalf(self.minMaxOfHalf)
        return time


    def next(self):
        time = Time(half=self.half, minute=self.minute, second=self.second, mili_second=self.mili_second)
        total_miliseconds = self.time_to_int(time)
        return self.int_to_time(total_miliseconds+2)


    def back(self):
        time = Time(half=self.half, minute=self.minute, second=self.second, mili_second=self.mili_second)
        total_miliseconds = self.time_to_int(time)
        return self.int_to_time(total_miliseconds-2)


    def __str__(self):
        return "half = %s\nminute = %s\nsecond = %s\nmili_second = %s" % (self.half, self.minute, self.second, self.mili_second)

