# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab
import matplotlib.pyplot as plt
from types import *

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        assert maxBirthProb > 0 and maxBirthProb < 1 and type(maxBirthProb) is FloatType
        assert clearProb > 0 and clearProb < 1 and type(clearProb) is FloatType

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        return random.random() <= self.clearProb
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()

class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        assert type(viruses) is ListType
        assert type(maxPop) is IntType

        self.viruses = viruses[:]
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        tempViruses = self.viruses[:]
        for virus in tempViruses:
            if virus.doesClear():
                # because all the virus is the same, so we can use the pop() function to remove any one of them
                # self.viruses.pop()
                self.viruses.remove(virus)
        curr_popDensity = float(len(self.viruses)) / self.maxPop
        
        tempViruses = self.viruses[:]
        for virus in tempViruses:
            try:
                self.viruses.append(virus.reproduce(curr_popDensity))
            except NoChildException: 
                pass
        return self.getTotalPop()

#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    viruses = []
    viruse_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    times = 300
    maxPop = 1000  
     
    for i in range(viruse_num):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))

    aPatient = SimplePatient(viruses, maxPop)

    x_axis_time_step = []
    y_axis_pop = []

    for i in range(times):
        x_axis_time_step.append(i)
        y_axis_pop.append(aPatient.getTotalPop()) 
        aPatient.update()
    
    # create the plot
    plt.plot(x_axis_time_step, y_axis_pop)
    plt.axis([0, times, 0, maxPop])
    plt.xlabel("Time step")
    plt.ylabel("Virus population")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()
    
#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        import copy
        assert maxBirthProb >= 0 and maxBirthProb < 1 and type(maxBirthProb) is FloatType
        assert clearProb >= 0 and clearProb < 1 and type(clearProb) is FloatType
        assert type(resistances) is DictType
        assert mutProb >= 0 and mutProb < 1 and type(mutProb) is FloatType
        
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        # use deep copy
        self.resistances = copy.deepcopy(resistances)
        self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        assert type(drug) is StringType
        
        return self.resistances.get(drug, False)
        
        
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        assert type(activeDrugs) is ListType
        assert type(popDensity) is FloatType and popDensity >= 0 and popDensity < 1
        # step 1 -- judge whether resistant the drugs or not
        repro = False
        # check the drug list is null
        if activeDrugs:
            for drug in activeDrugs:
                if self.getResistance(drug):
                    repro = True
                    break
        else:
            repro = True
            
        # step 2 -- the condition that can reproduce
        if repro:
            # have the probability with self.maxBirthProb * (1 - popDensity) to reproduce
            if random.random() <= self.maxBirthProb * (1 - popDensity):
                # simulate the drug resistance mutate 
                new_resistance = {}
                for drug in self.resistances.keys():
                    if random.random() <= 1 - self.mutProb:
                        # inherit the resistance trait from the parent
                        new_resistance[drug] = self.resistances[drug]
                    else:
                        # switch the resistance trait from the parent
                        new_resistance[drug] = not self.resistances[drug]
                # return a new instance of virus
                return ResistantVirus(self.maxBirthProb, self.clearProb, new_resistance, self.mutProb)
            # the virus can produce but does not produce
            else:
                raise NoChildException()
        # step 3 -- the condition that can not reproduce
        else:
            raise NoChildException()
        
class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        assert type(viruses) is ListType
        assert type(maxPop) is IntType
        
        self.viruses = viruses[:]
        self.maxPop = maxPop
        self.prescription = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescription:
            self.prescription.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescription
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count = 0
        for virus in self.viruses:
            resist_all_drug = True
            for drug in drugResist:
                if not virus.getResistance(drug):
                    resist_all_drug = False
                    break
            if resist_all_drug:
                count = count + 1
        return count
        
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # step 1 -- clear the dead virus 
        tempViruses = self.viruses[:]
        for virus in tempViruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        # step 2 -- count new population density
        curr_popDensity = float(len(self.viruses)) / self.maxPop
        # step 3 -- simulate to reproduce virus and update the viruses list
        tempViruses = self.viruses[:]
        for virus in tempViruses:
            try:
                self.viruses.append(virus.reproduce(curr_popDensity, self.prescription))
            except NoChildException: 
                pass
        return self.getTotalPop()
#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    viruses = []
    viruse_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    drug_name = "guttagonol"
    resistances = {drug_name : False}
    mutProb = 0.005
    times = 300
    maxPop = 1000  
    # initiate viruses list 
    for i in range(viruse_num):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    aPatient = Patient(viruses, maxPop)

    x_axis_time_step = []
    y_axis_pop = []
    y_axis_resi_pop = []

    # simulation without drug for 150 times
    for i in range(times):
        x_axis_time_step.append(i)
        y_axis_pop.append(aPatient.getTotalPop()) 
        y_axis_resi_pop.append(aPatient.getResistPop(aPatient.getPrescriptions()))
        if i == 150:
            # simulation with drug guttagonol for another 150 times
            aPatient.addPrescription(drug_name)
        aPatient.update()
    
    # create the plot
    plt.plot(x_axis_time_step, y_axis_pop, "ro", x_axis_time_step, y_axis_resi_pop, "b-",)
    plt.axis([0, times, 0, maxPop])
    plt.xlabel("Time step")
    plt.ylabel("Virus population")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()

#
# PROBLEM 5
#
        
def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    viruses = []
    viruse_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    drug_name = "guttagonol"
    resistances = {drug_name : False}
    mutProb = 0.005
    pre_timesA = 300
    pre_timesB = 150
    pre_timesC = 75
    pre_timesD = 0
    
    post_times = 150
    
    maxPop = 1000 
    num_patients = 100 
    # initiate viruses list 
    for i in range(viruse_num):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    aPatient = Patient(viruses, maxPop)

    x_axis_virus_pop = []

    """
    # Condition A : simulation without drug for 300 times
    for i in range(num_patients):
        aPatient = Patient(viruses, maxPop)
        for i in range(pre_timesA + post_times): 
            if i == pre_timesA:
                # simulation with drug guttagonol for another 150 times
                aPatient.addPrescription(drug_name)
            aPatient.update()
        x_axis_virus_pop.append(aPatient.getTotalPop())
    
    # create the plot
    plt.hist(x_axis_virus_pop, bins=10)       
    plt.xlabel("Virus population")
    plt.ylabel("Number of patients")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()
    """

    """
    # Condition B : simulation without drug for 150 times
    for i in range(num_patients):
        aPatient = Patient(viruses, maxPop)
        for i in range(pre_timesB + post_times): 
            if i == pre_timesB:
                # simulation with drug guttagonol for another 150 times
                aPatient.addPrescription(drug_name)
            aPatient.update()
        x_axis_virus_pop.append(aPatient.getTotalPop())
    
    # create the plot
    plt.hist(x_axis_virus_pop, bins=50)       
    plt.xlabel("Virus population")
    plt.ylabel("Number of patients")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()
    """
    
    """
    # Condition C : simulation without drug for 75 times
    for i in range(num_patients):
        aPatient = Patient(viruses, maxPop)
        for i in range(pre_timesC + post_times): 
            if i == pre_timesC:
                # simulation with drug guttagonol for another 150 times
                aPatient.addPrescription(drug_name)
            aPatient.update()
        x_axis_virus_pop.append(aPatient.getTotalPop())
    
    # create the plot
    plt.hist(x_axis_virus_pop, bins=50)       
    plt.xlabel("Virus population")
    plt.ylabel("Number of patients")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()
    """
    
    # Condition D : simulation without drug for 0 times
    for i in range(num_patients):
        aPatient = Patient(viruses, maxPop)
        for i in range(pre_timesD + post_times): 
            if i == pre_timesD:
                # simulation with drug guttagonol for another 150 times
                aPatient.addPrescription(drug_name)
            aPatient.update()
        x_axis_virus_pop.append(aPatient.getTotalPop())
    
    # create the plot
    plt.hist(x_axis_virus_pop, bins=50)       
    plt.xlabel("Virus population")
    plt.ylabel("Number of patients")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()
    
#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    viruses = []
    viruse_num = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    drug_nameA = "guttagonol"
    drug_nameB = "grimpex"
    resistances = {drug_nameA : False, drug_nameB : False}
    mutProb = 0.005
    
    pre_times = 150
    
    pre_timesA = 0
    pre_timesB = 150
    pre_timesC = 75
    pre_timesD = 0
    
    post_times = 150
    
    maxPop = 1000 
    num_patients = 30 
    # initiate viruses list 
    for i in range(viruse_num):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    x_axis_virus_pop = []
    
    for i in range(num_patients):
        aPatient = Patient(viruses, maxPop)
        for j in range(pre_times + pre_timesA + post_times): 
            if j == pre_times:
                # simulation with drug guttagonol for another 150 times
                aPatient.addPrescription(drug_nameA)
            if j == pre_times + pre_timesA:
                aPatient.addPrescription(drug_nameB)
            aPatient.update()
        x_axis_virus_pop.append(aPatient.getTotalPop())
    
    # create the plot
    plt.hist(x_axis_virus_pop, bins=50)       
    plt.xlabel("Virus population")
    plt.ylabel("Number of patients")
    plt.title("Simulation Virus Population Dynamics")
    plt.show()
    
    # other conditions are almost the same, ignore...

#
# PROBLEM 7
#
     
def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    # well, the same one with problem 6... so ignore it

if __name__ == "__main__":
    #problem2()
    #problem4()
    #problem5()
    problem6()
    #problem7()
