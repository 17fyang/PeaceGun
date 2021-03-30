# coding=utf-8
class Schedule(object):
    def __init__(self):
        self.tickTime = 0
        self.tickQueue = []

    def tick(self):
        '''
        服务器tick 仅供PeaceServerSystem调用，其他业务不应tick
        :return:
        '''
        self.tickTime = self.tickTime + 1
        while len(self.tickQueue) > 0:
            tickTask = self.tickQueue[0]
            if tickTask.tick > self.tickTime:
                break

            tickTask.task(*tickTask.args)
            self.tickQueue.pop(0)

    def runTaskDelay(self, delayTick, task, *args):
        '''
        提交一个延时任务
        :param task:
        :param delayTick:
        :param args
        :return:
        '''
        tickTask = TickTask(task, self.tickTime + delayTick, args)

        if len(self.tickQueue) == 0 or self.tickQueue[-1].tick <= tickTask.tick:
            self.tickQueue.append(tickTask)
        else:
            for i in range(len(self.tickQueue) - 1, 0, -1):
                if tickTask.tick > self.tickQueue[i - 1].tick:
                    self.tickQueue.insert(i, tickTask)
                    break
            else:
                self.tickQueue.insert(0, tickTask)

    def runNextTick(self, task):
        '''
        提交一个任务，下一个tick执行
        :param task:
        :return:
        '''
        return self.runTaskDelay(1, task)


class TickTask(object):
    def __init__(self, task, delay=None, args=None):
        self.tick = delay
        self.task = task
        self.args = args


schedule = Schedule()
