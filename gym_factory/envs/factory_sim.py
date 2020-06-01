import pandas as pd
import numpy as np

class TIKTOK:
    def __init__(self, times:int):
        self.cur_idx = 0
        self.max_idx = times

    def TIK(self): # check END
        self.cur_idx += 1
        if self.cur_idx == self.max_idx: return False
        return True

class PRT(TIKTOK):
    def __init__(self, times:int, products:int,
        daily_const:int=500,
        prodct_time:int=23*24, failure_ratio:float=1-98.5):
        super(PRT, self).__init__(times)

        # state
        self.sch_table = np.zeros((products, times))

        # const
        self.daily_const = daily_const
        self.prodct_time = prodct_time
        self.failure_ratio = failure_ratio

    def get_status(self):
        return self.sch_table
    
    def step(self, action):
        # action = [] * producs
        self.sch_table[self.cur_idx] = action
        assert self.const_check()
        return self.TIK(), self.production()
    
    def const_check(self):
        # daily product const
        for i in range(self.times/24):
            if sum(self.sch_table[i:i*24].flatten()) > self.daily_const:
                return False
        return True
    
    def production(self):
        if self.cur_idx >= self.prodct_time:
            # in this simulation, failure ratio is 0% for ease
            return self.sch_table[:, self.cur_idx-self.prodct_time]
        else: return [0] * self.sch_table.shape[0]

class MOL_BLK(TIKTOK):
    def __init__(self, times:int, products:int,
        daily_consts:list, tik_const:float=6.667,
        prodct_time:int=48, failure_ratio:float=1-97.5,
        ):
        super(MOL_BLK, self).__init__(times)

        # state
        self.sch_table = np.zeros((products, times))

        # const
        self.daily_consts = daily_consts
        self.tik_const = tik_const
        self.prodct_time = prodct_time
        self.failure_ratio = failure_ratio

        self.monthly_cut_yield = []
    
    def table2status(self):
        ret_stat = []
        STATUS = ('CHECK', 'PROCESS', 'CHANGE', 'STOP')
        for i in range(self.sch_table.shape[1]):
            if sum(self.sch_table[:, i].flatten()) == 0:
                ret_stat.append([STATUS[0], STATUS[-1]])

    def const_check(self):
        # 1. by time
        for i in range(self.times):
            if sum(self.sch_table[i].flatten()) > self.tik_const:
                return False
        # 2. by day
        for i in range(self.times/24):
            if sum(self.sch_table[i:i*24].flatten()) > self.daily_consts[i]:
                return False
        return True

    def production(self):
        if self.cur_idx >= self.prodct_time:
            # in this simulation, failure ratio is 0% for ease
            return self.sch_table[:, self.cur_idx-self.prodct_time] * self.failure_ratio * [506, 506, 400, 400] * self.monthly_cut_yield[self.cur_idx]
        else: return [0] * self.sch_table.shape[0]