from re import I
import string
from unicodedata import name
import numpy as np
import matplotlib.pyplot as plt
import time


class Neuron():
    def __init__(self, name):
        self.name = name
        self.I = 200
        self.dt = 0.1
        self.V_th = -65.
        self.V_reset = -75.
        self.tau_m = 5.
        self.g_L = 10.
        self.V = -75.
        self.E_L = -75.
        self.start_t = time.time()
        self.dur = 0
        self.V_hist = []
        self.V_hist.append(-75.)
        self.alive = True
        self.time_alive()
    
    def calc_V(self):
        dvdt = (-(self.V - self.V_reset) + (self.I/self.g_L))/self.tau_m
        self.V = self.V_hist[-1] + dvdt * self.dt
        self.V_hist.append(self.V)
        return self.V

    def updateMembranePotential(self):
        if self.V > self.V_th:
            V = self.V_reset
            self.V_hist.append(V)
        
        else:
            V = self.calc_V()

    def time_alive(self):
        while self.alive == True:
            curr_time = time.time()
            self.dur = curr_time - self.start_t
            if self.dur > 10.0:
                self.alive = False
                print("Time limit reached! Killing neuron")
                break


            if self.alive == True:
                print("Neuron: ",self.name, 'alive for', self.dur)

            self.updateMembranePotential()
            print(self.V_hist[-1])
            #wait for time to reach +100ms from curr_time
            amt = 0.1 - (time.time()-curr_time)
            time.sleep(amt)
        
        plt.plot(self.V_hist)
        plt.show()
        del self

def main():
    neu1 = Neuron('neu1')


if __name__=='__main__':
    main()
        
        

#TODO:  explore live graphing in matplotlib, make neurons spike again, allow for multineuron connections.



        


