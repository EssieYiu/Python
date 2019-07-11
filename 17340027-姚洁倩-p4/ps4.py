# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random
import copy

random.seed(0)
##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    def __init__(self, birth_prob, death_prob):
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        return random.random() < self.death_prob
 
    def reproduce(self, pop_density):
        if random.random() < self.birth_prob*(1 - pop_density):
            return SimpleBacteria(self.birth_prob,self.death_prob)
        else:
            raise NoChildException


class Patient(object):
    def __init__(self, bacteria, max_pop):
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        return len(self.bacteria)

    def update(self):
        surviving_bacteria = []
        for bacterium in self.bacteria:
            if not bacterium.is_killed():
                surviving_bacteria.append(bacterium)
        density = len(surviving_bacteria)/self.max_pop
        new_breed = []
        for bacterium in surviving_bacteria:
            try:
                new_child = bacterium.reproduce(density)
            except:
                continue
            new_breed.append(new_child)
        self.bacteria = surviving_bacteria + new_breed
        return self.get_total_pop()


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    total = 0
    for trial in populations:
        total += trial[n]
    return total/len(populations)



def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    populations = []
    for i in range(num_trials):
        simple_bacteria = []
        bacteria_num_this_trial = []
        for j in range(num_bacteria):
            bacterium = SimpleBacteria(birth_prob,death_prob)
            simple_bacteria.append(bacterium)
        sick_people = Patient(simple_bacteria,max_pop)
        for k in range(300):
            if k == 0:
                bacteria_num_this_trial.append(sick_people.get_total_pop())
            else:
                bacteria_num_this_trial.append(sick_people.update())
        populations.append(bacteria_num_this_trial)
    x_cor = np.linspace(0,300,300)
    #print(x_cor)
    y_cor = []
    temp_total = 0
    for k in range(300):
        temp_total = 0
        for t in range(num_trials):
            temp_total += populations[t][k]
        y_cor.append(temp_total/num_trials)
    make_one_curve_plot(x_cor,y_cor,"Timestep","Average population","Without Antibiotic")
    return populations



# When you are ready to run the simulation, uncomment the next line
populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    avg_pop = calc_pop_avg(populations,t)
    square_sum_deviation = 0
    trial_num = len(populations)
    for i in range(trial_num):
        square_sum_deviation += (populations[i][t] - avg_pop)**2
    std_deviation = np.sqrt(square_sum_deviation/trial_num)
    return std_deviation


def calc_95_ci(populations, t):
    mean = calc_pop_avg(populations,t)
    SEM = calc_pop_std(populations,t)/np.sqrt(len(populations))
    width = 1.96*SEM
    return (mean,width)


#compute confidence interval of time step 299 by using data from above 
(mean,width) = calc_95_ci(populations,299)
print("95% confidence interval of simple simulation at timestep 299 is:",'('+str(mean-width)+','+str(mean+width)+')')
##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        SimpleBacteria.__init__(self,birth_prob,death_prob)
        self.resistant = resistant
        self.mut_prob = mut_prob

    def get_resistant(self):
        return self.resistant

    def is_killed(self):
        if self.get_resistant():
            return random.random() < self.death_prob
        else:
            return random.random() < self.death_prob/4

    def reproduce(self, pop_density):
        if random.random() < self.birth_prob*(1 - pop_density):
            if self.get_resistant():
                offspring = ResistantBacteria(self.birth_prob,self.death_prob,self.get_resistant(),self.mut_prob)
            else:
                get_mutate = (random.random() < self.mut_prob*(1 - pop_density))
                offspring = ResistantBacteria(self.birth_prob,self.death_prob,get_mutate,self.mut_prob)
            return offspring
        else:
            raise NoChildException



class TreatedPatient(Patient):
    def __init__(self, bacteria, max_pop):
        Patient.__init__(self,bacteria,max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        self.on_antibiotic = True

    def get_resist_pop(self):
        resist_num = 0
        for bacterium in self.bacteria:
            if bacterium.get_resistant():
                resist_num += 1
        return resist_num

    def update(self):
        surviving_bacteria = []
        for bacterium in self.bacteria:
            if not bacterium.is_killed():
                surviving_bacteria.append(bacterium)
        if self.on_antibiotic:
            temp_survive = copy.deepcopy(surviving_bacteria)
            surviving_bacteria = []
            for b in temp_survive:
                if b.get_resistant():
                    surviving_bacteria.append(b)
        density = len(surviving_bacteria)/self.max_pop
        new_breed = []
        for b in surviving_bacteria:
            try:
                offspring = b.reproduce(density)
            except:
                continue
            new_breed.append(offspring)
        self.bacteria = surviving_bacteria + new_breed
        return len(self.bacteria)



##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    total_populations = []
    resistant_populations = []
    for i in range(num_trials):
        bacteria_num_this_trial = []
        bacteria_resistant_this_trial = []
        bacteria = []
        for j in range(num_bacteria):
            bacteria.append(ResistantBacteria(birth_prob,death_prob,resistant,mut_prob))
        sick = TreatedPatient(bacteria,max_pop)
        for k in range(150):
            if k == 0:
                bacteria_num_this_trial.append(sick.get_total_pop())
            else:
                bacteria_num_this_trial.append(sick.update())
            bacteria_resistant_this_trial.append(sick.get_resist_pop())
        sick.set_on_antibiotic()
        for k in range(250):
            bacteria_num_this_trial.append(sick.update())
            bacteria_resistant_this_trial.append(sick.get_resist_pop())
        total_populations.append(bacteria_num_this_trial)
        resistant_populations.append(bacteria_resistant_this_trial)
    #print('total:\n',total_populations,'\nresistant:\n',resistant_populations)
    x_cord = np.linspace(0,400,400)
    y_cord1 = []
    y_cord2 = []
    for k in range(400):
        total_temp = 0
        resist_temp = 0
        for j in range(num_trials):
            total_temp += total_populations[j][k]
            resist_temp += resistant_populations[j][k]
        y_cord1.append(total_temp/num_trials)
        y_cord2.append(resist_temp/num_trials)
    make_two_curve_plot(x_cord,y_cord1,y_cord2,"Total","Resistant","Timestep","Average Population","With an Antibiotic")
    return (total_populations,resistant_populations)


# When you are ready to run the simulations, uncomment the next lines one
# at a time

total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.3,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)
meanA_total, widthA_total = calc_95_ci(total_pop,299)
meanA_resist,widthA_resist = calc_95_ci(resistant_pop,299)
print("95% confidence interval of total population in simulation A at time step 299 is",'('+str(meanA_total-widthA_total)+','+str(meanA_total+widthA_total)+')')
print("95% confidence interval of resistant population in simulation A at time step 299 is",'('+str(meanA_resist-widthA_resist)+','+str(meanA_resist+widthA_resist)+')')
total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.17,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)
meanB_total, widthB_total = calc_95_ci(total_pop,299)
meanB_resist,widthB_resist = calc_95_ci(resistant_pop,299)
print("95% confidence interval of total population in simulation B at time step 299 is",'('+str(meanB_total-widthB_total)+','+str(meanB_total+widthB_total)+')')
print("95% confidence interval of resistant population in simulation B at time step 299 is",'('+str(meanB_resist-widthB_resist)+','+str(meanB_resist+widthB_resist)+')')