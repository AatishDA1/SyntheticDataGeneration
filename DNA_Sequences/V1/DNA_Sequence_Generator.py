import random

def sequence_generator(length):
    """
    Generates a random DNA sequence of a specified length.
    
    Parameters:
    - length (int): The length of the DNA sequence to generate.
    
    Returns:
    - str: A random DNA sequence of the specified length.
    """
    nucleotides = ['A', 'T', 'C', 'G']
    sequence = ''.join(random.choice(nucleotides) for _ in range(length))
    return sequence