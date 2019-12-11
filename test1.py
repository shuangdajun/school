from test import *
re1 = taskA.delay(100, 200)
print(re1.result)
# print(re1.status)
# re2 = taskB.delay(1, 2, 3)
# print(re2.result)
# re3 = add.delay(1, 2)
print(re1.status)