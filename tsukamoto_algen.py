import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from deap import base, creator, tools, algorithms

# Define fuzzy variables
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture')
pores = ctrl.Antecedent(np.arange(0, 101, 1), 'pores')
blackheads = ctrl.Antecedent(np.arange(0, 101, 1), 'blackheads')
telangiactasis = ctrl.Antecedent(np.arange(0, 101, 1), 'telangiactasis')
skincare_type = ctrl.Consequent(np.arange(0, 101, 1), 'skincare_type')

# Ensure bounds are sorted and within the correct range
def validate_bounds(bounds):
    bounds = sorted(bounds)
    bounds = [max(0, min(100, x)) for x in bounds]
    return bounds

# Define membership functions for input variables
def set_membership_functions(bounds):
    bounds = validate_bounds(bounds)
    moisture['low'] = fuzz.trimf(moisture.universe, [0, bounds[0], bounds[1]])
    moisture['medium'] = fuzz.trimf(moisture.universe, [bounds[0], bounds[2], bounds[3]])
    moisture['high'] = fuzz.trimf(moisture.universe, [bounds[2], bounds[4], 100])

    pores['small'] = fuzz.trimf(pores.universe, [0, bounds[5], bounds[6]])
    pores['medium'] = fuzz.trimf(pores.universe, [bounds[5], bounds[7], bounds[8]])
    pores['large'] = fuzz.trimf(pores.universe, [bounds[7], bounds[9], 100])

    blackheads['few'] = fuzz.trimf(blackheads.universe, [0, bounds[10], bounds[11]])
    blackheads['some'] = fuzz.trimf(blackheads.universe, [bounds[10], bounds[12], bounds[13]])
    blackheads['many'] = fuzz.trimf(blackheads.universe, [bounds[12], bounds[14], 100])

    telangiactasis['low'] = fuzz.trimf(telangiactasis.universe, [0, bounds[15], bounds[16]])
    telangiactasis['medium'] = fuzz.trimf(telangiactasis.universe, [bounds[15], bounds[17], bounds[18]])
    telangiactasis['high'] = fuzz.trimf(telangiactasis.universe, [bounds[17], bounds[19], 100])

    skincare_type['type1'] = fuzz.trimf(skincare_type.universe, [0, bounds[20], bounds[21]])
    skincare_type['type2'] = fuzz.trimf(skincare_type.universe, [bounds[20], bounds[22], bounds[23]])
    skincare_type['type3'] = fuzz.trimf(skincare_type.universe, [bounds[22], bounds[24], 100])

# Define fuzzy rules
def create_rules():
    rule1 = ctrl.Rule(moisture['low'] & pores['small'] & blackheads['few'] & telangiactasis['low'], skincare_type['type1'])
    rule2 = ctrl.Rule(moisture['medium'] & pores['medium'] & blackheads['some'] & telangiactasis['medium'], skincare_type['type2'])
    rule3 = ctrl.Rule(moisture['high'] & pores['large'] & blackheads['many'] & telangiactasis['high'], skincare_type['type3'])
    # Adding more general rules to cover possible inputs
    rule4 = ctrl.Rule(moisture['low'] | pores['small'] | blackheads['few'] | telangiactasis['low'], skincare_type['type1'])
    rule5 = ctrl.Rule(moisture['medium'] | pores['medium'] | blackheads['some'] | telangiactasis['medium'], skincare_type['type2'])
    rule6 = ctrl.Rule(moisture['high'] | pores['large'] | blackheads['many'] | telangiactasis['high'], skincare_type['type3'])
    return [rule1, rule2, rule3, rule4, rule5, rule6]

# Fitness function
def fitness(individual):
    set_membership_functions(individual)
    rules = create_rules()
    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    # Assuming we have a dataset to evaluate the accuracy
    dataset = [
        {'moisture': 20, 'pores': 30, 'blackheads': 10, 'telangiactasis': 20, 'expected': 'type1'},
        {'moisture': 50, 'pores': 50, 'blackheads': 50, 'telangiactasis': 50, 'expected': 'type2'},
        {'moisture': 80, 'pores': 70, 'blackheads': 90, 'telangiactasis': 80, 'expected': 'type3'}
    ]
    correct = 0
    for data in dataset:
        try:
            sim.input['moisture'] = data['moisture']
            sim.input['pores'] = data['pores']
            sim.input['blackheads'] = data['blackheads']
            sim.input['telangiactasis'] = data['telangiactasis']
            sim.compute()
            output = sim.output['skincare_type']
            # Fuzzify the expected output to match the categories
            if (output < 33 and data['expected'] == 'type1') or \
               (33 <= output < 66 and data['expected'] == 'type2') or \
               (output >= 66 and data['expected'] == 'type3'):
                correct += 1
        except ValueError:
            continue
    return correct / len(dataset),

# Genetic Algorithm setup
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", np.random.uniform, 0, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=25)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxBlend, alpha=0.4)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=50)
NGEN = 10
CXPB = 0.4
MUTPB = 0.01

for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
    top_ind = tools.selBest(population, k=1)[0]
    print(f"Generation {gen}: Best Fitness = {top_ind.fitness.values[0]}")

best_ind = tools.selBest(population, k=1)[0]
print(f"Best individual: {best_ind}, Fitness: {best_ind.fitness.values[0]}")

# Use the best individual to set the final membership functions
set_membership_functions(best_ind)
rules = create_rules()
system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)
