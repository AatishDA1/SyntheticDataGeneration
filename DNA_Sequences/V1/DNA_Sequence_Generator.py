import random
from datetime import datetime

class DNA_Sequence_Generator:
    """This is a class for generating DNA sequences and creating FASTA Files from them."""
    @staticmethod
    def generate_sequence(length, gc_content):
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
    def sequence_to_fasta(sequence, sequence_id="unknown_id", 
                      mutation_status="original", 
                      date_of_generation="unknown_date", 
                      file_name="default_sequence.fasta"):
        """
        Writes a DNA sequence to a FASTA file format.

        Parameters:
        - sequence (str): The input DNA sequence to be written to a FASTA file format.
        - sequence_id (str): Identifier for the sequence.
        - mutation_status (str): Mutation status of the sequence.
        - date_of_generation (str): Date when the sequence was generated.
        - file_name (str): The name of the output FASTA file.
        """
        # Ensure the file name ends with .fasta.
        if not file_name.endswith('.fasta'):
            file_name += '.fasta'
        
        # Set the date of generation to today if it is unknown.
        if date_of_generation == "unknown_date":
            date_of_generation = datetime.today().strftime('%Y-%m-%d')
        
        # Constructs the header.
        header = f"{sequence_id} | {mutation_status} | {date_of_generation}"
        
        with open(file_name, 'w') as fasta_file:
            fasta_file.write(f">{header}\n")
            fasta_file.write(f"{sequence}\n")

class DNA_Sequence_Mutations:
    """This is a class for applying mutations to DNA sequences. The individual mutations that can be applied are insertions, deletions and substitutions."""
    @staticmethod
    def insert(fasta_file, num_insertions, max_bases_per_insertion):
        """
        Mutates a DNA sequence by adding insertions at random positions.

        Parameters:
        - fasta_file (str): Path to the input FASTA file containing the DNA sequence.
        - num_insertions (int): Number of separate insertions to be added to the sequence.
        - max_bases_per_insertion (int): Maximum number of bases per insertion.

        Returns:
        - list: A list of each insertion made.
        """
        # Reads the sequence from the input FASTA file.
        with open(fasta_file, 'r') as file:
            lines = file.readlines()
            header = lines[0].strip()
            sequence = ''.join(line.strip() for line in lines[1:])

        # List to store the insertions done.
        mutation_list = []

        # Loop to perform the specified number of insertions.
        for _ in range(num_insertions):
            # Generates a random insertion.
            insertion_length = random.randint(1, max_bases_per_insertion)
            insertion_sequence = ''.join(random.choice(['A', 'T', 'C', 'G']) for _ in range(insertion_length))
            insertion_position = random.randint(0, len(sequence))

            # Inserts the mutation into the sequence.
            sequence = sequence[:insertion_position] + insertion_sequence + sequence[insertion_position:]

            # Records the mutation in the list.
            mutation_list.append(f"{insertion_position}_{insertion_position + 1}ins{insertion_sequence}")

        # Updates the mutation status in the header.
        header_parts = header.split('|')
        if len(header_parts) > 1:
            header_parts[1] = " Mutated (Insertions)"
            header = '|'.join(header_parts)

        # Writes the mutated sequence to a new FASTA file.
        mutated_file_name = fasta_file.replace('.fasta', '_mut_i.fasta')
        with open(mutated_file_name, 'w') as file:
            file.write(header + '\n')
            file.write(sequence + '\n')

        # Returns the list of insertions done.
        return mutation_list


    @staticmethod
    def delete(fasta_file, num_deletions, max_bases_per_deletion):
        """
        Mutates a DNA sequence by adding deletions at random positions.

        Parameters:
        - fasta_file (str): Path to the input FASTA file containing the DNA sequence.
        - num_deletions (int): Number of separate deletions to be added to the sequence.
        - max_bases_per_deletion (int): Maximum number of bases per deletion.

        Returns:
        - list: A list of each deletion made.
        """
        # Reads the sequence from the input FASTA file.
        with open(fasta_file, 'r') as file:
            lines = file.readlines()
            header = lines[0].strip()
            sequence = ''.join(line.strip() for line in lines[1:])

        # List to store the deletions done.
        mutation_list = []

        # Loop to perform the specified number of deletions.
        for _ in range(num_deletions):
            # Generates a random deletion.
            deletion_length = random.randint(1, min(max_bases_per_deletion, len(sequence)))
            deletion_position = random.randint(0, len(sequence) - deletion_length)

            # Deletes the mutation from the sequence.
            sequence = sequence[:deletion_position] + sequence[deletion_position + deletion_length:]

            # Records the mutation in the list.
            mutation_list.append(f"{deletion_position + 1}_{deletion_position + deletion_length}del")

        # Updates the mutation status in the header.
        header_parts = header.split('|')
        if len(header_parts) > 1:
            header_parts[1] = " Mutated (Deletions)"
            header = '|'.join(header_parts)

        # Writes the mutated sequence to a new FASTA file.
        mutated_file_name = fasta_file.replace('.fasta', '_mut_d.fasta')
        with open(mutated_file_name, 'w') as file:
            file.write(header + '\n')
            file.write(sequence + '\n')

        # Returns the list of deletions done.
        return mutation_list

    @staticmethod
    def substitute(fasta_file, num_substitutions):
        """
        Mutates a DNA sequence by adding substitutions at random positions.

        Parameters:
        - fasta_file (str): Path to the input FASTA file containing the DNA sequence.
        - num_substitutions (int): Number of separate substitutions to be added to the sequence.

        Returns:
        - list: A list of each substitution made.
        """
        # Reads the sequence from the input FASTA file.
        with open(fasta_file, 'r') as file:
            lines = file.readlines()
            header = lines[0].strip()
            sequence = ''.join(line.strip() for line in lines[1:])

        # List to store the substitutions done.
        mutation_list = []

        # Loop to perform the specified number of substitutions.
        for _ in range(num_substitutions):
            # Generates a random substitution.
            substitution_position = random.randint(0, len(sequence) - 1)
            original_base = sequence[substitution_position]
            new_base = random.choice([base for base in ['A', 'T', 'C', 'G'] if base != original_base])

            # Substitutes the base in the sequence.
            sequence = sequence[:substitution_position] + new_base + sequence[substitution_position + 1:]

            # Records the mutation in the list.
            mutation_list.append(f"{substitution_position + 1}{original_base}>{new_base}")

        # Updates the mutation status in the header.
        header_parts = header.split('|')
        if len(header_parts) > 1:
            header_parts[1] = " Mutated (Substitutions)"
            header = '|'.join(header_parts)
        
        # Writes the mutated sequence to a new FASTA file.
        mutated_file_name = fasta_file.replace('.fasta', '_mut_s.fasta')
        with open(mutated_file_name, 'w') as file:
            file.write(header + '\n')
            file.write(sequence + '\n')

        # Returns the list of substitutions done.
        return mutation_list
            
            