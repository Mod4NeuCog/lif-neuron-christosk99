import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
import multiprocessing


#TODO:  model refractory period with function (1ms/0.001s), explore live graphing in matplotlib, make neurons spike again, allow for multineuron connections.

#slowed down x100 since we use 0.1s intervals ?? unsure

class Neuron():
    def __init__(self, name, fig, ax):
        #pre-set parameters
        self.name = name
        self.fig = fig
        self.ax = ax
        self.maxdur = 20.0
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
        self.spike = False
        self.graph_data = collections.deque(np.full(shape=250,fill_value=-75.))
        self.graph, = ax.plot(self.graph_data)
        self.time_alive() #not ideal but I want to keep track of neuron "lifespans"

    #func to calc V
    def calc_V(self):
        dvdt = (-(self.V - self.V_reset) + (self.I/self.g_L))/self.tau_m
        self.V = self.V_hist[-1] + dvdt * self.dt
        return self.V

    #func to update membrane potential
    def updateMembranePotential(self):
        if self.V > self.V_th:
            V = self.V_reset
            self.V_hist.append(V)
            self.spike = True

        else:
            V = self.calc_V()
            self.V_hist.append(V)

    #func to check whether to keep or kill the neuron. Idea was to compute in real time (still not ideal and bad solution) and not precompute data.
    def time_alive(self):
        while self.alive == True:
            curr_time = time.time()
            self.dur = curr_time - self.start_t
            if self.dur > self.maxdur: #total duration we keep neuron alive
                self.alive = False
                print("Time limit reached! Killing neuron")
                break


            if self.alive == True:
                print("Neuron: ",self.name, 'alive for', self.dur)

            self.updateMembranePotential()

            self.graph_data.popleft()
            self.graph_data.append(self.V)
            self.graph.set_ydata(self.graph_data)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()


            print(self.V_hist[-1])
            #wait for time to reach +100ms from curr_time
            amt = 0.1 - (time.time()-curr_time)
            #throttle the program based on computing time
            #time.sleep(amt)

            if self.spike:
                for i in range(int(1./0.1)): #better solution needed although replaced once func for refrac. per.
                    self.V_hist.append(self.V_reset)
                    self.graph_data.popleft()
                    self.graph_data.append(self.V_reset)
                    self.graph.set_ydata(self.graph_data)
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
                    #time.sleep(0.1) #refractory period slowed down x1000
                V = self.calc_V()
                self.V_hist.append(V)
                self.spike = False
        
        #plt.plot(self.V_hist)
        #plt.show()
        del self

def main():
    plt.ion()
    fig, ax = plt.subplots(figsize=(12,6), facecolor='#DEDEDE')
    plt.title("TEStsadgagd")
    plt.xlabel("time window")
    plt.ylabel("V")
    ax.set_ylim(-85.,-55.)
    neu1 = Neuron('neu1', fig, ax)

if __name__=='__main__':
    main()
        



        

