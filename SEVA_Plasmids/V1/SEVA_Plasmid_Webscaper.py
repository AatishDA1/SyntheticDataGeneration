import random
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

class SEVA_Plasmid_Webscraper:
    """This is a class for webscraping information about the canonical SEVA plasmids from the SEVA and NCBI website."""
    
    @staticmethod
    def extract_seva_table(url, num_rows=None, include_gadget=True):
        """
        Extracts the canonical SEVA plasmids table from the SEVA website.
        
        Parameters:
            url (str): The URL of the SEVA canonical plasmids list page.
            num_rows (int, optional): The number of rows (plasmids) to extract. If None, extract all rows.
            include_gadget (bool): Whether to include rows that have data in the gadget column.
        
        Returns:
            pd.DataFrame: A DataFrame containing the name, resistance, ori, cargo, gadget, 
                          GenBank number, GenBank link, and developer for each plasmid.
        """
        # Make a request to the website.
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table containing the plasmid information.
        table = soup.find('table')
        
        if not table:
            raise ValueError("Table not found on the webpage.")
        
        # Initialize a list to store the plasmid information.
        plasmids = []
        
        # Iterate over the rows of the table.
        rows = table.find_all('tr')[1:num_rows+1] if num_rows else table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 9:
                continue  # Skip rows that do not have enough columns.
            name = cells[0].text.strip()
            resistance = cells[1].text.strip()
            ori = cells[2].text.strip()
            cargo = cells[3].text.strip()
            gadget = cells[4].text.strip()
            genbank_number = cells[5].text.strip()
            genbank_link = cells[5].find('a')['href'] if cells[5].find('a') else ''
            developer = cells[8].text.strip()  
            
            if not include_gadget and gadget:
                continue  # Skip rows that have data in the gadget column if include_gadget is False.
            
            plasmids.append({
                'name': name,
                'resistance': resistance,
                'ori': ori,
                'cargo': cargo,
                'gadget': gadget,
                'genbank_number': genbank_number,
                'genbank_link': genbank_link,
                'developer': developer
            })
        
        # Convert the list to a DataFrame.
        df = pd.DataFrame(plasmids)
        return df
    
    @staticmethod
    def get_genbank_file(genbank_number):
        """
        Fetches the GenBank file content from NCBI using the given GenBank accession number and formats it for writing to a .gb file.
        
        Parameters:
            genbank_number (str): The GenBank accession number.
        
        Returns:
            str: The GenBank file content formatted for a .gb file.
        """
        # Define the base URL for the NCBI efetch API.
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        
        # Define the parameters for the API request.
        params = {
            'db': 'nucleotide',
            'id': genbank_number,
            'rettype': 'gb',
            'retmode': 'text'
        }
        
        # Make a request to the NCBI efetch API.
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch GenBank file for {genbank_number}")
        
        # Return the content of the GenBank file.
        return response.text

    @staticmethod
    def write_to_genbank_file(genbank_content, filename):
        """
        Writes the GenBank content to a .gb file.
        
        Parameters:
            genbank_content (str): The content of the GenBank file.
            filename (str): The name of the file to write the GenBank content to.
        """
        with open(filename, 'w') as file:
            file.write(genbank_content)


class Sequence_Mutations:
    """This is a class for applying mutations to DNA sequences. The individual mutations that can be applied are insertions, deletions and substitutions."""
    @staticmethod
    def mutate_seva(genbank_content, enable_oriT, enable_T1, enable_T0, enable_insertion, enable_deletion, enable_substitution, num_mutations, min_bases, max_bases):
        """
        Mutates the DNA sequence in the GenBank file content in the oriT, T0, or T1 regions of the SEVA plasmid.
        
        Parameters:
            genbank_content (str): The content of the GenBank file.
            enable_oriT (bool): Whether to mutate the oriT region.
            enable_T1 (bool): Whether to mutate the T1 region.
            enable_T0 (bool): Whether to mutate the T0 region.
            enable_insertion (bool): Whether to perform insertions.
            enable_deletion (bool): Whether to perform deletions.
            enable_substitution (bool): Whether to perform substitutions.
            num_mutations (int): The number of mutations to apply per region.
            min_bases (int): The minimum length of each mutation.
            max_bases (int): The maximum length of each mutation.
        
        Returns:
            tuple: (str, str, pd.DataFrame) - The mutated GenBank file content, the filename extension, and a DataFrame row with mutation details.
        """
        # Define the regions to be mutated.
        regions = {
            'oriT': enable_oriT,
            'T1': enable_T1,
            'T0': enable_T0
        }
        
        # Extract the sequence from the GenBank content.
        sequence_match = re.search(r'ORIGIN\s+(.*?)\s*//', genbank_content, re.DOTALL)
        if not sequence_match:
            raise ValueError("Failed to extract sequence from GenBank content.")
        
        sequence = sequence_match.group(1)
        sequence = re.sub(r'[^atgc]', '', sequence, flags=re.IGNORECASE)
        
        # Initialize mutation details.
        locus_name_match = re.search(r'LOCUS\s+(\S+)', genbank_content)
        locus_name = locus_name_match.group(1) if locus_name_match else "Unknown"
        mutation_details = {
            'locus': locus_name,
            'oriT_mutations': [],
            'T1_mutations': [],
            'T0_mutations': []
        }
        
        # Find the regions in the GenBank file content.
        region_patterns = {
            'oriT': r'misc_feature\s+(\d+)\.\.(\d+)\n\s+/note="oriT"',
            'T1': r'regulatory\s+(\d+)\.\.(\d+)\n\s+/regulatory_class="terminator"\n\s+/note="T1"',
            'T0': r'regulatory\s+(\d+)\.\.(\d+)\n\s+/regulatory_class="terminator"\n\s+/note="T0"'
        }
        region_locations = {}
        
        for region, pattern in region_patterns.items():
            match = re.search(pattern, genbank_content)
            if match:
                region_locations[region] = (int(match.group(1)), int(match.group(2)))
        
        # Perform mutations.
        for region, enabled in regions.items():
            if enabled and region in region_locations:
                start, end = region_locations[region]
                for _ in range(num_mutations):
                    mutation_type = random.choice(
                        ['insertion', 'deletion', 'substitution'] if enable_insertion and enable_deletion and enable_substitution
                        else ['insertion', 'deletion'] if enable_insertion and enable_deletion
                        else ['insertion', 'substitution'] if enable_insertion and enable_substitution
                        else ['deletion', 'substitution'] if enable_deletion and enable_substitution
                        else ['insertion'] if enable_insertion
                        else ['deletion'] if enable_deletion
                        else ['substitution']
                    )
                    
                    length = random.randint(min_bases, max_bases)
                    position = random.randint(start, end)
                    
                    if mutation_type == 'insertion':
                        insertion = ''.join(random.choice('atcg') for _ in range(length))
                        sequence = sequence[:position] + insertion + sequence[position:]
                        mutation_details[f'{region}_mutations'].append(f"{position + 1}_{position + 1 + length}ins{insertion}")
                    
                    elif mutation_type == 'deletion':
                        sequence = sequence[:position] + sequence[position + length:]
                        mutation_details[f'{region}_mutations'].append(f"{position + 1}_{position + length}del")
                    
                    elif mutation_type == 'substitution':
                        original_base = sequence[position]
                        new_base = random.choice([base for base in 'atcg' if base != original_base])
                        sequence = sequence[:position] + new_base + sequence[position + 1:]
                        mutation_details[f'{region}_mutations'].append(f"{position + 1}{original_base}>{new_base}")

        # Format the mutated sequence for GenBank output.
        formatted_sequence = Sequence_Mutations.format_genbank_sequence(sequence)
        
        # Update the GenBank content with the mutated sequence.
        mutated_content = re.sub(r'(ORIGIN\s+)(.*?)\s*//', f'\\1{formatted_sequence}\n//', genbank_content, flags=re.DOTALL)
        
        # Update the base pair count in the LOCUS line.
        new_bp_count = len(sequence)
        mutated_content = re.sub(r'(LOCUS\s+\S+\s+)(\d+)(\s+bp\s+)', fr'\g<1>{new_bp_count}\g<3>', mutated_content)
        
        # Add the appropriate filename extension.
        mutated_filename_extension = '_mut'
        for region, enabled in regions.items():
            if enabled:
                mutated_filename_extension += f'_{region}'

        # Update the locus name with the extension.
        new_locus_name = locus_name + mutated_filename_extension
        mutated_content = re.sub(r'(LOCUS\s+)\S+', fr'\1{new_locus_name}', mutated_content)
        mutation_details['locus'] = new_locus_name
        
        # Convert mutation details to DataFrame row.
        mutation_df = pd.DataFrame([mutation_details])
        
        return mutated_content, mutated_filename_extension, mutation_df

    @staticmethod
    def format_genbank_sequence(sequence):
        """
        Formats the sequence for GenBank output.
        
        Parameters:
            sequence (str): The DNA sequence.
        
        Returns:
            str: The formatted DNA sequence.
        """
        formatted_sequence = ""
        for i in range(0, len(sequence), 60):
            segment = sequence[i:i + 60]
            formatted_sequence += " " + str(i + 1).rjust(9) + " "
            formatted_sequence += " ".join(segment[j:j + 10] for j in range(0, len(segment), 10)) + "\n"
        return formatted_sequence