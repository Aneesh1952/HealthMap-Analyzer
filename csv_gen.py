import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define regions and their approximate coordinates
regions = {
    'New York': {'lat': 40.7128, 'lon': -74.0060, 'base_health': 82},
    'Los Angeles': {'lat': 34.0522, 'lon': -118.2437, 'base_health': 80},
    'Chicago': {'lat': 41.8781, 'lon': -87.6298, 'base_health': 78},
    'Houston': {'lat': 29.7604, 'lon': -95.3698, 'base_health': 76},
    'Phoenix': {'lat': 33.4484, 'lon': -112.0740, 'base_health': 81},
    'Philadelphia': {'lat': 39.9526, 'lon': -75.1652, 'base_health': 77},
    'San Antonio': {'lat': 29.4241, 'lon': -98.4936, 'base_health': 79},
    'San Diego': {'lat': 32.7157, 'lon': -117.1611, 'base_health': 83},
    'Dallas': {'lat': 32.7767, 'lon': -96.7970, 'base_health': 78},
    'San Jose': {'lat': 37.3382, 'lon': -121.8863, 'base_health': 84}
}

# Generate data
data = []
current_date = datetime.now()

for region_name, region_info in regions.items():
    # Generate multiple data points around each city
    num_points = np.random.randint(80, 120)  # Different number of points per region
    
    for _ in range(num_points):
        # Add some random variation to coordinates (within ~50km)
        lat_variation = np.random.normal(0, 0.15)
        lon_variation = np.random.normal(0, 0.15)
        
        # Generate health metrics with some variation
        base_health = region_info['base_health']
        health_metric = max(0, min(100, np.random.normal(base_health, 5)))
        
        # Generate genetic diversity score (0-100)
        genetic_diversity = np.random.normal(70, 10)
        genetic_diversity = max(0, min(100, genetic_diversity))
        
        # Generate environmental factors
        air_quality = max(0, min(100, np.random.normal(75, 15)))
        water_quality = max(0, min(100, np.random.normal(80, 10)))
        green_space = max(0, min(100, np.random.normal(65, 20)))
        
        # Generate disease prevalence (per 100,000 people)
        heart_disease = max(0, np.random.normal(200, 50))
        diabetes = max(0, np.random.normal(90, 20))
        respiratory = max(0, np.random.normal(150, 40))
        
        # Add random variation to dates
        date_variation = np.random.randint(0, 365)
        measurement_date = (current_date - timedelta(days=date_variation)).strftime('%Y-%m-%d')
        
        data.append({
            'region': region_name,
            'latitude': region_info['lat'] + lat_variation,
            'longitude': region_info['lon'] + lon_variation,
            'measurement_date': measurement_date,
            'health_metric': round(health_metric, 2),
            'genetic_diversity': round(genetic_diversity, 2),
            'air_quality_index': round(air_quality, 2),
            'water_quality_index': round(water_quality, 2),
            'green_space_percent': round(green_space, 2),
            'heart_disease_rate': round(heart_disease, 2),
            'diabetes_rate': round(diabetes, 2),
            'respiratory_disease_rate': round(respiratory, 2),
            'population_density': round(np.random.normal(5000, 2000), 2),
            'healthcare_access_score': round(np.random.normal(75, 15), 2)
        })

# Convert to DataFrame and save
df = pd.DataFrame(data)

# Sort by region and date
df = df.sort_values(['region', 'measurement_date'])

# Save to CSV
df.to_csv('health_data_sample.csv', index=False)

# Print sample and statistics
print(f"Generated {len(df)} rows of data")
print("\nFirst few rows:")
print(df.head())
print("\nSummary statistics:")
print(df.describe())