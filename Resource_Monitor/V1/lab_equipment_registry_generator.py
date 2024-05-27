import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('en_GB')

class Equipment:
    """
    A class to generate synthetic data for laboratory equipment.
    """

    @staticmethod
    def generate_instruments(num_instruments, include_thermocyclers=True, include_heater_shakers=True):
        """
        Generates synthetic data for instruments, including thermocyclers and heater shakers.

        Parameters
        ----------
        num_instruments : int
            Number of instruments to generate. Must be greater than 0.
        include_thermocyclers : bool, optional
            Whether to include thermocyclers in the generated data. Default is True.
        include_heater_shakers : bool, optional
            Whether to include heater shakers in the generated data. Default is True.

        Returns
        -------
        pd.DataFrame
            DataFrame containing synthetic data for instruments.
        """
        if num_instruments <= 0:
            raise ValueError("num_instruments must be greater than 0.")

        companies = ['Bio-Rad', 'Thermo Fisher Scientific', 'Agilent Technologies', 'Eppendorf', 'Roche']
        data = []
        used_serial_numbers = set()
        used_reference_ids = set()

        while len(used_reference_ids) < num_instruments:
            reference_id = f"REF{len(used_reference_ids) + 1:04d}"
            used_reference_ids.add(reference_id)
            if include_thermocyclers and len(used_reference_ids) <= num_instruments:
                # Generate data for a thermocycler
                name = f'Thermocycler {len(used_reference_ids)}'
                instrument_type = 'Thermocycler'
                model = f'{instrument_type} {random.choice(["Pro", "Lite", "Mini"])} {random.randint(99, 900)}'
                brand = random.choice(companies)
                location = fake.address().replace("\n", ", ")
                serial_number = fake.bothify(text='??######').upper()
                
                # Ensure serial number is unique
                while serial_number in used_serial_numbers:
                    serial_number = fake.bothify(text='??######').upper()
                used_serial_numbers.add(serial_number)
                
                purchase_date = fake.date_between_dates(date_start=datetime(2000, 1, 1), date_end=datetime.now() - timedelta(days=1))
                data.append({
                    'reference_id': reference_id,
                    'id': len(used_reference_ids),
                    'name': name,
                    'type': instrument_type,
                    'model': model,
                    'brand': brand,
                    'serial_number': serial_number,
                    'purchase_date': purchase_date,
                    'location': location
                })

            if include_heater_shakers and len(used_reference_ids) < num_instruments:
                reference_id = f"REF{len(used_reference_ids) + 1:04d}"
                used_reference_ids.add(reference_id)
                # Generate data for a heater shaker
                name = f'Heater Shaker {len(used_reference_ids)}'
                instrument_type = 'Heater Shaker'
                model = f'Opentrons {instrument_type}'
                brand = 'Opentrons'
                location = fake.address().replace("\n", ", ")
                serial_number = fake.bothify(text='??######').upper()
                
                # Ensure serial number is unique
                while serial_number in used_serial_numbers:
                    serial_number = fake.bothify(text='??######').upper()
                used_serial_numbers.add(serial_number)
                
                purchase_date = fake.date_between_dates(date_start=datetime(2000, 1, 1), date_end=datetime.now() - timedelta(days=1))
                data.append({
                    'reference_id': reference_id,
                    'id': len(used_reference_ids),
                    'name': name,
                    'type': instrument_type,
                    'model': model,
                    'brand': brand,
                    'serial_number': serial_number,
                    'purchase_date': purchase_date,
                    'location': location
                })

        return pd.DataFrame(data)

    @staticmethod
    def thermocycler(instrument_df):
        """
        Generates synthetic data for thermocyclers from the instrument table.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.

        Returns
        -------
        pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        """
        # Filter thermocyclers from the instrument dataframe
        thermocyclers = instrument_df[instrument_df['type'] == 'Thermocycler']
        
        data = []
        for index, row in thermocyclers.iterrows():
            # Generate thermocycler-specific data
            max_temp = round(random.uniform(95.0, 105.0) * 2) / 2
            min_temp = round(random.uniform(0.5, 25.0) * 2) / 2
            max_heating_rate = round(random.uniform(1.0, 5.0) * 2) / 2
            max_cooling_rate = round(random.uniform(1.0, 5.0) * 2) / 2
            block_capacity = random.choice([48, 96, 384])
            well_capacity = random.choice([112.0, 200.0, 100.0, 2000.0])

            # Append thermocycler data to list
            data.append({
                'reference_id': row['reference_id'],
                'id': row['id'],
                'max_temp (°C)': max_temp,
                'min_temp (°C)': min_temp,
                'max_heating_rate (°C/s)': max_heating_rate,
                'max_cooling_rate (°C/s)': max_cooling_rate,
                'block_capacity': block_capacity,
                'well_capacity (µL)': well_capacity
            })
        
        return pd.DataFrame(data)

    @staticmethod
    def heatershaker(instrument_df):
        """
        Generates synthetic data for heater shakers from the instrument table.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.

        Returns
        -------
        pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        """
        # Filter heater shakers from the instrument dataframe
        heater_shakers = instrument_df[instrument_df['type'] == 'Heater Shaker']
        
        data = []
        for index, row in heater_shakers.iterrows():
            # Generate heater shaker-specific data
            max_temp = round(random.uniform(75.0, 105.0) * 2) / 2
            min_temp = round(random.uniform(0.5, 25.0) * 2) / 2
            max_shake_speed = round(random.uniform(500.0, 3000.0) * 2) / 2
            min_shake_speed = round(random.uniform(100.0, 500.0) * 2) / 2
            block_capacity = random.choice([48, 96, 384])
            well_capacity = random.choice([112.0, 200.0, 100.0, 2000.0])

            # Append heater shaker data to list
            data.append({
                'reference_id': row['reference_id'],
                'id': row['id'],
                'max_temp (°C)': max_temp,
                'min_temp (°C)': min_temp,
                'max_shake_speed (RPM)': max_shake_speed,
                'min_shake_speed (RPM)': min_shake_speed,
                'block_capacity': block_capacity,
                'well_capacity (µL)': well_capacity
            })
        
        return pd.DataFrame(data)

class EquipmentCorrupt:
    """A class to corrupt synthetic data for laboratory equipment."""

    @staticmethod
    def corrupt_ids(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Corrupts IDs by creating duplicate IDs across tables.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of IDs to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        num_rows = len(instrument_df)
        instrument_df['corrupt_ids'] = 0
        
        for i in range(num_rows - 1):
            if random.random() < corruption_pct:
                instrument_df.at[i + 1, 'id'] = instrument_df.at[i, 'id']
                instrument_df.at[i + 1, 'corrupt_ids'] = 1

        # Update thermocycler and heatershaker tables based on reference_id
        for i in range(num_rows - 1):
            if instrument_df.at[i, 'type'] == 'Thermocycler':
                thermocycler_df.loc[thermocycler_df['reference_id'] == instrument_df.at[i + 1, 'reference_id'], 'id'] = instrument_df.at[i + 1, 'id']
            elif instrument_df.at[i, 'type'] == 'Heater Shaker':
                heatershaker_df.loc[heatershaker_df['reference_id'] == instrument_df.at[i + 1, 'reference_id'], 'id'] = instrument_df.at[i + 1, 'id']

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def corrupt_serial_numbers(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Corrupts serial numbers by creating duplicate serial numbers in the instrument table.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of serial numbers to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        num_rows = len(instrument_df)
        instrument_df['corrupt_serial_numbers'] = 0
        
        for i in range(num_rows - 1):
            if random.random() < corruption_pct:
                instrument_df.at[i + 1, 'serial_number'] = instrument_df.at[i, 'serial_number']
                instrument_df.at[i + 1, 'corrupt_serial_numbers'] = 1

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def corrupt_purchase_dates(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Corrupts purchase dates by setting them in the future.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of purchase dates to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        num_rows = len(instrument_df)
        instrument_df['corrupt_purchase_dates'] = 0
        
        for index, row in instrument_df.iterrows():
            if random.random() < corruption_pct:
                future_date = fake.date_between(start_date='today', end_date='+10y')
                instrument_df.at[index, 'purchase_date'] = future_date
                instrument_df.at[index, 'corrupt_purchase_dates'] = 1

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def swap_max_min_temps(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Swaps max and min temperatures in the thermocycler and heatershaker tables.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of rows to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        instrument_df['swap_max_min_temps'] = 0
        
        for index, row in thermocycler_df.iterrows():
            if random.random() < corruption_pct:
                max_temp = thermocycler_df.at[index, 'max_temp (°C)']
                min_temp = thermocycler_df.at[index, 'min_temp (°C)']
                thermocycler_df.at[index, 'max_temp (°C)'] = min_temp
                thermocycler_df.at[index, 'min_temp (°C)'] = max_temp
                instrument_df.loc[instrument_df['reference_id'] == thermocycler_df.at[index, 'reference_id'], 'swap_max_min_temps'] = 1

        for index, row in heatershaker_df.iterrows():
            if random.random() < corruption_pct:
                max_temp = heatershaker_df.at[index, 'max_temp (°C)']
                min_temp = heatershaker_df.at[index, 'min_temp (°C)']
                heatershaker_df.at[index, 'max_temp (°C)'] = min_temp
                heatershaker_df.at[index, 'min_temp (°C)'] = max_temp
                instrument_df.loc[instrument_df['reference_id'] == heatershaker_df.at[index, 'reference_id'], 'swap_max_min_temps'] = 1

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def swap_heating_cooling_rates(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Swaps heating and cooling rates in the thermocycler and heatershaker tables.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of rows to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        instrument_df['swap_heating_cooling_rates'] = 0

        for index, row in thermocycler_df.iterrows():
            if random.random() < corruption_pct:
                max_heating_rate = thermocycler_df.at[index, 'max_heating_rate (°C/s)']
                max_cooling_rate = thermocycler_df.at[index, 'max_cooling_rate (°C/s)']
                thermocycler_df.at[index, 'max_heating_rate (°C/s)'] = max_cooling_rate
                thermocycler_df.at[index, 'max_cooling_rate (°C/s)'] = max_heating_rate
                instrument_df.loc[instrument_df['reference_id'] == thermocycler_df.at[index, 'reference_id'], 'swap_heating_cooling_rates'] = 1

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def swap_min_max_shake_speeds(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Swaps min and max shake speeds in the heatershaker table.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of rows to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        instrument_df['swap_min_max_shake_speeds'] = 0

        for index, row in heatershaker_df.iterrows():
            if random.random() < corruption_pct:
                max_shake_speed = heatershaker_df.at[index, 'max_shake_speed (RPM)']
                min_shake_speed = heatershaker_df.at[index, 'min_shake_speed (RPM)']
                heatershaker_df.at[index, 'max_shake_speed (RPM)'] = min_shake_speed
                heatershaker_df.at[index, 'min_shake_speed (RPM)'] = max_shake_speed
                instrument_df.loc[instrument_df['reference_id'] == heatershaker_df.at[index, 'reference_id'], 'swap_min_max_shake_speeds'] = 1

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def swap_block_well_capacities(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Swaps block and well capacities in the thermocycler and heatershaker tables.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of rows to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df).
        """
        instrument_df['swap_block_well_capacities'] = 0

        for index, row in thermocycler_df.iterrows():
            if random.random() < corruption_pct:
                block_capacity = thermocycler_df.at[index, 'block_capacity']
                well_capacity = thermocycler_df.at[index, 'well_capacity (µL)']
                thermocycler_df.at[index, 'block_capacity'] = well_capacity
                thermocycler_df.at[index, 'well_capacity (µL)'] = block_capacity
                instrument_df.loc[instrument_df['reference_id'] == thermocycler_df.at[index, 'reference_id'], 'swap_block_well_capacities'] = 1

        for index, row in heatershaker_df.iterrows():
            if random.random() < corruption_pct:
                block_capacity = heatershaker_df.at[index, 'block_capacity']
                well_capacity = heatershaker_df.at[index, 'well_capacity (µL)']
                heatershaker_df.at[index, 'block_capacity'] = well_capacity
                heatershaker_df.at[index, 'well_capacity (µL)'] = block_capacity
                instrument_df.loc[instrument_df['reference_id'] == heatershaker_df.at[index, 'reference_id'], 'swap_block_well_capacities'] = 1

        return instrument_df, thermocycler_df, heatershaker_df

    @staticmethod
    def run_all_corruptions(instrument_df, thermocycler_df, heatershaker_df, corruption_pct):
        """
        Runs all corruption methods and outputs a summary DataFrame indicating which corruptions have occurred.

        Parameters
        ----------
        instrument_df : pd.DataFrame
            DataFrame containing synthetic data for instruments.
        thermocycler_df : pd.DataFrame
            DataFrame containing synthetic data for thermocyclers.
        heatershaker_df : pd.DataFrame
            DataFrame containing synthetic data for heater shakers.
        corruption_pct : float
            Percentage of rows to corrupt (0-1).

        Returns
        -------
        tuple
            Corrupted dataframes (instrument_df, thermocycler_df, heatershaker_df) and summary corruption DataFrame.
        """
        instrument_df['corrupt_ids'] = 0
        instrument_df['corrupt_serial_numbers'] = 0
        instrument_df['corrupt_purchase_dates'] = 0
        instrument_df['swap_max_min_temps'] = 0
        instrument_df['swap_heating_cooling_rates'] = 0
        instrument_df['swap_min_max_shake_speeds'] = 0
        instrument_df['swap_block_well_capacities'] = 0

        corruptions = [
            EquipmentCorrupt.corrupt_ids,
            EquipmentCorrupt.corrupt_serial_numbers,
            EquipmentCorrupt.corrupt_purchase_dates,
            EquipmentCorrupt.swap_max_min_temps,
            EquipmentCorrupt.swap_heating_cooling_rates,
            EquipmentCorrupt.swap_min_max_shake_speeds,
            EquipmentCorrupt.swap_block_well_capacities
        ]

        for corruption in corruptions:
            instrument_df, thermocycler_df, heatershaker_df = corruption(instrument_df, thermocycler_df, heatershaker_df, corruption_pct)

        # Create summary DataFrame
        corruption_summary = instrument_df[['reference_id', 'corrupt_ids', 'corrupt_serial_numbers', 'corrupt_purchase_dates',
                                            'swap_max_min_temps', 'swap_heating_cooling_rates', 'swap_min_max_shake_speeds',
                                            'swap_block_well_capacities']]
        
        # Drop corruption columns from instrument_df
        instrument_df.drop(columns=['corrupt_ids', 'corrupt_serial_numbers', 'corrupt_purchase_dates',
                                    'swap_max_min_temps', 'swap_heating_cooling_rates', 'swap_min_max_shake_speeds',
                                    'swap_block_well_capacities'], inplace=True)

        return instrument_df, thermocycler_df, heatershaker_df, corruption_summary