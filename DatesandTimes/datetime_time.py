import datetime

t = datetime.time(1, 2, 3)
print(t)
print("hour       :", t.hour)
print("minute     :", t.minute)
print("second     :", t.second)
print("microsecond:", t.microsecond)
print("tzinfo     :", t.tzinfo)


print("Earliest  :", datetime.time.min)
print("Latest    :", datetime.time.max)
print("Resolution:", datetime.time.resolution)
