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
    unemployment_rate REAL,
    median_earnings INTEGER,
    
    -- Age Demographics
    median_age REAL,
    population_under_18 INTEGER,
    population_65_and_over INTEGER,
    
    -- Race/Ethnicity
    white_alone INTEGER,
    black_alone INTEGER,
    hispanic_latino INTEGER,
    
    -- Economic
    median_home_value INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);