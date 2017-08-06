from apscheduler.scheduler import Scheduler

class evExecuter:

    def __init__(self):
        self.executer = Scheduler()
        self.executer.start()

    def addEvt(self,func,hr):
        self.executer.add_cron_job(func,year='*',month='*',day='*',hour='*', minute='*', second='0')
        #self.executer.add_cron_job(func,year='*',month='*',day='*',hour=hr, minute='0', second='0')
