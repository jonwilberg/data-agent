-- Create read-only user for the agent
CREATE USER census_reader WITH PASSWORD 'readonly_password';

-- Grant necessary permissions
GRANT CONNECT ON DATABASE data_agent TO census_reader;
GRANT USAGE ON SCHEMA public TO census_reader;

-- Create the main table
CREATE TABLE IF NOT EXISTS ny_census_data (
    id SERIAL PRIMARY KEY,
    county_name VARCHAR(100),
    state_code VARCHAR(2),
    county_code VARCHAR(3),
    
    -- Population & Housing
    total_population INTEGER,
    median_household_income INTEGER,
    total_housing_units INTEGER,
    owner_occupied_units INTEGER,
    renter_occupied_units INTEGER,
    
    -- Education
    bachelors_degree_holders INTEGER,
    graduate_degree_holders INTEGER,
    high_school_graduates INTEGER,
    
    -- Employment
    unemployed_count INTEGER,
    median_earnings INTEGER,
    
    -- Age Demographics
    median_age REAL,
    population_under_18 INTEGER,
    population_18_and_over INTEGER,
    
    -- Race/Ethnicity
    white_alone INTEGER,
    black_alone INTEGER,
    hispanic_latino INTEGER,
    
    -- Economic
    median_home_value INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add comments to columns with official Census Bureau definitions
COMMENT ON COLUMN ny_census_data.county_name IS 'Name of the New York county extracted from Census API NAME field';
COMMENT ON COLUMN ny_census_data.state_code IS 'State FIPS code (36 for New York)';
COMMENT ON COLUMN ny_census_data.county_code IS '3-digit county FIPS code within the state';

-- Population & Housing Comments (B01003, B19013, B25001, B25003)
COMMENT ON COLUMN ny_census_data.total_population IS 'B01003_001E: Total Population - Total count of all people residing in the geographic area';
COMMENT ON COLUMN ny_census_data.median_household_income IS 'B19013_001E: Median Household Income in the Past 12 Months (in 2022 Inflation-Adjusted Dollars)';
COMMENT ON COLUMN ny_census_data.total_housing_units IS 'B25001_001E: Housing Units - Total count of all housing units (occupied and vacant)';
COMMENT ON COLUMN ny_census_data.owner_occupied_units IS 'B25003_002E: Tenure - Number of housing units that are owner-occupied';
COMMENT ON COLUMN ny_census_data.renter_occupied_units IS 'B25003_003E: Tenure - Number of housing units that are renter-occupied';

-- Education Comments (DP02) - Population 25 years and over
COMMENT ON COLUMN ny_census_data.bachelors_degree_holders IS 'DP02_0065E: Educational Attainment - Population 25 years and over with bachelor''s degree';
COMMENT ON COLUMN ny_census_data.graduate_degree_holders IS 'DP02_0066E: Educational Attainment - Population 25 years and over with graduate or professional degree';
COMMENT ON COLUMN ny_census_data.high_school_graduates IS 'DP02_0062E: Educational Attainment - Population 25 years and over who are high school graduates (includes equivalency)';

-- Employment Comments (DP03)
COMMENT ON COLUMN ny_census_data.unemployed_count IS 'DP03_0005E: Employment Status - Population 16 years and over in civilian labor force who are unemployed';
COMMENT ON COLUMN ny_census_data.median_earnings IS 'DP03_0062E: Income and Benefits - Median household income in dollars (in 2022 inflation-adjusted dollars)';

-- Age Demographics Comments (DP05)
COMMENT ON COLUMN ny_census_data.median_age IS 'DP05_0018E: Sex and Age - Median age in years of the total population';
COMMENT ON COLUMN ny_census_data.population_under_18 IS 'DP05_0019E: Sex and Age - Number of people under 18 years of age';
COMMENT ON COLUMN ny_census_data.population_18_and_over IS 'DP05_0021E: Sex and Age - Number of people 18 years and over';

-- Race/Ethnicity Comments (DP05)
COMMENT ON COLUMN ny_census_data.white_alone IS 'DP05_0037E: Race - Number of people who identify as White alone (one race)';
COMMENT ON COLUMN ny_census_data.black_alone IS 'DP05_0038E: Race - Number of people who identify as Black or African American alone (one race)';
COMMENT ON COLUMN ny_census_data.hispanic_latino IS 'DP05_0071E: Hispanic or Latino - Number of people of Hispanic or Latino origin (any race)';

-- Economic Comments (DP04)
COMMENT ON COLUMN ny_census_data.median_home_value IS 'DP04_0089E: Housing Value - Median value in dollars of owner-occupied housing units';

-- System field
COMMENT ON COLUMN ny_census_data.created_at IS 'Timestamp when record was inserted into database';

-- Grant SELECT permission on the table to read-only user
GRANT SELECT ON ny_census_data TO census_reader;