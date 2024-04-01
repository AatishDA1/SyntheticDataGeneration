import random

def sequence_generator(length, gc_content):
    """
    Generate a random DNA sequence of a specified length with a specified GC content.
    
    Parameters:
    - length (int): The length of the DNA sequence to generate.
    - gc_content (float): Desired GC content (between 0 and 1) of the DNA sequence.
    
    Returns:
    - str: A random DNA sequence of the specified length and GC content.
    """
    # Validate gc_content
    if not 0 <= gc_content <= 1:
        raise ValueError("GC content must be between 0 and 1.")
    
    gc_count = int(length * gc_content)
    at_count = length - gc_count
    
    # Generate sequence with desired GC content
    sequence = ''.join(random.choices(['G', 'C'], k=gc_count)) + \
               ''.join(random.choices(['A', 'T'], k=at_count))
    
    # Shuffle the sequence to randomize the order
    sequence_list = list(sequence)
    random.shuffle(sequence_list)
    return ''.join(sequence_list)