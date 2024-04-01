import random

class DNA_Sequence_Generator:
    """This is a class for generating DNA sequences and creating FASTA Files from them."""
    @staticmethod
    def sequence_generator(length, gc_content):
        """
        Generates a random DNA sequence of a specified length with a specified GC content.
        
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

    @staticmethod
    def sequence_to_fasta(sequence, header, file_name):
        """
        Writes a DNA sequence to a FASTA file format.
        
        Parameters:
        - sequence (str): The DNA sequence.
        - header (str): Header for the FASTA file, typically starting with '>' and followed by an identifier/description.
        - file_name (str): The name of the output FASTA file.
        """
        # Ensure the file name ends with .fasta.
        if not file_name.endswith('.fasta'):
            file_name += '.fasta'
        
        with open(file_name, 'w') as fasta_file:
            fasta_file.write(f">{header}\n")
            fasta_file.write(f"{sequence}\n")