import random
import string
import operator

SOLUTION = 'Hello, World!'
MAX_SCORE = len(SOLUTION)
MAX_DNA_LENGTH = 20
CHANCES_TO_EVOLVE = (
    (0.05, 3),
    (0.15, 2),
    (0.30, 1),
)
POPULATION = 1000
POPULATION_TO_CARRY = 50
PARENT_COUPLES = 100
SONS_PER_COUPLE = 3
RANDOM_DNAS = POPULATION - POPULATION_TO_CARRY - PARENT_COUPLES * SONS_PER_COUPLE
assert RANDOM_DNAS >= 0


def score(index, character):
    if index >= len(SOLUTION):
        return -0.01
    return int(SOLUTION[index] == character)


def fitness(dna):
    return sum([score(i, each) for i, each in enumerate(dna)])


def generate_dna():
    size = random.randint(1, MAX_DNA_LENGTH)
    chars = (random.choice(string.printable) for _ in xrange(size))
    return ''.join(chars)


def generate_dnas(amount):
    return [generate_dna() for _ in xrange(amount)]


def random_chromosome(dna_one, dna_two, index):
    # Assuming that len(dna_one) > index or len(dna_two) > index
    all_dnas = [dna_one, dna_two]
    chosen = all_dnas.pop(random.randint(0, 1))
    if index >= len(chosen):
        chosen = all_dnas.pop()
    return chosen[index]


def make_son(dna_one, dna_two):
    son_length = (len(dna_one) + len(dna_two) + random.randint(0, 1))/2
    chromosomes = (
        random_chromosome(dna_one, dna_two, i) for i in xrange(son_length)
    )
    son = ''.join(chromosomes)

    evolution = random.Random()
    for chance, amount in CHANCES_TO_EVOLVE:
        if evolution < amount:
            for _ in xrange(amount):
                index = random.randint(0, len(son) - 1)
                son[index] = random.choice(string.printable)
            break
    return son


def make_sons(parent_couples, sons_per_couple):
    sons = [
        make_son(a, b)
        for a, b in parent_couples
        for _ in xrange(sons_per_couple)
    ]
    return sons


def make_couples(dnas_with_fitness, number_of_couples):
    dnas = dnas_with_fitness
    couples = [
        (weighted_choice(dnas), weighted_choice(dnas))
        for _ in xrange(number_of_couples)
    ]
    return couples


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w


def score_population(population):
    data = [(dna, fitness(dna)) for dna in population]
    return sorted(data, key=operator.itemgetter(1), reverse=True)


if __name__ == '__main__':
    generation = 0
    dnas = generate_dnas(POPULATION)
    scores = score_population(dnas)
    dna, value = scores[0]

    while generation < 100:
        if value == MAX_SCORE:
            break

        # Build new generation
        best_values = scores[:POPULATION_TO_CARRY]
        couples = make_couples(scores, PARENT_COUPLES)
        sons = make_sons(couples, SONS_PER_COUPLE)
        random_dnas = generate_dnas(RANDOM_DNAS)

        dnas = [x for x, _ in best_values] + sons + random_dnas

        # Eval built generation
        scores = score_population(dnas)
        best = scores[0]
        dna, value = best

        print 'Best score for generation {} is: {}'.format(
            generation, value
        )

        generation += 1

    print '======================================='
    print 'Best candidate found after {} generations:'.format(generation)
    print dna
    print 'Fitness score: {}'.format(value)
