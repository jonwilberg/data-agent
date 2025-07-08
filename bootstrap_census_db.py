import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# Census API configuration
BASE_URL = "https://api.census.gov/data/2022/acs/acs5"
PROFILE_URL = "https://api.census.gov/data/2022/acs/acs5/profile"
API_KEY = os.getenv("CENSUS_API_KEY", "")  # Get your free key from https://api.census.gov/data/key_signup.html

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'data_agent',
    'user': 'postgres',
    'password': 'postgres'
}

# Variables to fetch from main ACS endpoint
MAIN_VARIABLES = [
    "NAME",         # County name
    "B01003_001E",  # Total population
    "B19013_001E",  # Median household income
    "B25001_001E",  # Total housing units
    "B25003_002E",  # Owner-occupied units
    "B25003_003E",  # Renter-occupied units
]

# Variables to fetch from profile endpoint
PROFILE_VARIABLES = [
    "NAME",         # County name (for matching)
    "DP02_0065E",   # Bachelor's degree holders
    "DP02_0066E",   # Graduate/professional degree holders
    "DP02_0062E",   # High school graduates
    "DP03_0005E",   # Unemployment rate
    "DP03_0062E",   # Median earnings
    "DP05_0018E",   # Median age
    "DP05_0019E",   # Population under 18
    "DP05_0021E",   # Population 65 and over
    "DP05_0037E",   # White alone
    "DP05_0038E",   # Black/African American alone
    "DP05_0071E",   # Hispanic/Latino 
    "DP04_0089E",   # Median home value
]

def fetch_census_data():
    """Fetch census data from both main and profile APIs"""
    
    # Fetch main variables
    main_variables_str = ",".join(MAIN_VARIABLES)
    main_url = f"{BASE_URL}?get={main_variables_str}&for=county:*&in=state:36"
    if API_KEY:
        main_url += f"&key={API_KEY}"
    
    print(f"Fetching main data from: {main_url}")
    
    try:
        main_response = requests.get(main_url)
        main_response.raise_for_status()
        main_data = main_response.json()
        main_headers = main_data[0]
        main_rows = main_data[1:]
        
        # Convert to dict for easier lookup
        main_dict = {}
        for row in main_rows:
            county_name = row[0]  # NAME is first column
            main_dict[county_name] = dict(zip(main_headers, row))
        
    except requests.RequestException as e:
        print(f"Error fetching main data: {e}")
        return None, None
    
    # Fetch profile variables
    profile_variables_str = ",".join(PROFILE_VARIABLES)
    profile_url = f"{PROFILE_URL}?get={profile_variables_str}&for=county:*&in=state:36"
    if API_KEY:
        profile_url += f"&key={API_KEY}"
    
    print(f"Fetching profile data from: {profile_url}")
    
    try:
        profile_response = requests.get(profile_url)
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        profile_headers = profile_data[0]
        profile_rows = profile_data[1:]
        
        # Convert to dict for easier lookup
        profile_dict = {}
        for row in profile_rows:
            county_name = row[0]  # NAME is first column
            profile_dict[county_name] = dict(zip(profile_headers, row))
        
    except requests.RequestException as e:
        print(f"Error fetching profile data: {e}")
        return None, None
    
    # Merge the data
    all_headers = MAIN_VARIABLES + [var for var in PROFILE_VARIABLES if var != "NAME"] + ["state", "county"]
    merged_rows = []
    
    for county_name in main_dict.keys():
        if county_name in profile_dict:
            merged_row = []
            main_row = main_dict[county_name]
            profile_row = profile_dict[county_name]
            
            # Add main variables
            for var in MAIN_VARIABLES:
                merged_row.append(main_row[var])
            
            # Add profile variables (skip NAME since it's already included)
            for var in PROFILE_VARIABLES:
                if var != "NAME":
                    merged_row.append(profile_row[var])
            
            # Add state and county codes
            merged_row.append(main_row["state"])
            merged_row.append(main_row["county"])
            
            merged_rows.append(merged_row)
    
    return all_headers, merged_rows


def insert_data(headers, rows):
    """Insert data into PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Clear existing data
        cursor.execute("DELETE FROM ny_census_data")
        
        for row in rows:
            # Create a dictionary from headers and row data
            data_dict = dict(zip(headers, row))
            
            # Extract values, handling nulls and converting to appropriate types
            def safe_int(value):
                try:
                    return int(value) if value and value != '-888888888' else None
                except (ValueError, TypeError):
                    return None
            
            def safe_float(value):
                try:
                    return float(value) if value and value != '-888888888' else None
                except (ValueError, TypeError):
                    return None
            
            # Extract county name from API response (format: "County Name, New York")
            county_name = data_dict['NAME'].split(', ')[0]
            
            insert_query = """
                INSERT INTO ny_census_data (
                    county_name, state_code, county_code,
                    total_population, median_household_income, total_housing_units,
                    owner_occupied_units, renter_occupied_units,
                    bachelors_degree_holders, graduate_degree_holders, high_school_graduates,
                    unemployment_rate, median_earnings, labor_force_participation_rate,
                    median_age, population_under_18, population_65_and_over,
                    white_alone, black_alone, hispanic_latino,
                    families_below_poverty, median_home_value
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            values = (
                county_name,
                data_dict['state'],
                data_dict['county'],
                safe_int(data_dict['B01003_001E']),
                safe_int(data_dict['B19013_001E']),
                safe_int(data_dict['B25001_001E']),
                safe_int(data_dict['B25003_002E']),
                safe_int(data_dict['B25003_003E']),
                safe_int(data_dict['DP02_0065E']),
                safe_int(data_dict['DP02_0066E']),
                safe_int(data_dict['DP02_0062E']),
                safe_float(data_dict['DP03_0005E']),
                safe_int(data_dict['DP03_0062E']),
                safe_float(data_dict['DP05_0018E']),
                safe_int(data_dict['DP05_0019E']),
                safe_int(data_dict['DP05_0021E']),
                safe_int(data_dict['DP05_0037E']),
                safe_int(data_dict['DP05_0038E']),
                safe_int(data_dict['DP05_0071E']),
                safe_int(data_dict['DP04_0089E']),
            )
            
            cursor.execute(insert_query, values)
        
        conn.commit()
        print(f"Successfully inserted {len(rows)} records")
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def main():
    print("Fetching New York Census data...")
    headers, rows = fetch_census_data()
    
    if headers and rows:
        print(f"Retrieved {len(rows)} counties")
        insert_data(headers, rows)
        print("Data insertion complete!")
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    main()