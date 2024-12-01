import json
import re

def find_technology_category(technology, mappings):
    """
    Find the category of a given technology from the JSON mappings.
    
    Args:
        technology (str): The technology to search for
        mappings (dict): The JSON mapping of technologies to services
    
    Returns:
        tuple: A tuple containing (category, service) if found, or (None, None) if not found
    """
    # Remove special characters and convert to lowercase
    def clean_string(s):
        return re.sub(r'[^a-zA-Z0-9\s]', '', s).lower().strip()
    
    # Clean the input technology
    cleaned_technology = clean_string(technology)
    
    # Iterate through each category and its technologies
    for category, tech_services in mappings.items():
        for tech, service in tech_services.items():
            # Clean the current technology from the mapping
            cleaned_current_tech = clean_string(tech)
            
            # Check for exact match or partial match
            if (cleaned_technology == cleaned_current_tech or 
                cleaned_technology in cleaned_current_tech or 
                cleaned_current_tech in cleaned_technology):
                return category, service
    
    return None, None

# Load the JSON mapping
with open('skill_service_mapping.json', 'r') as file:
    it_skills_mapping = json.load(file)

# Example usage demonstration
def demonstrate_technology_lookup():
    test_technologies = [
        'React.js', 
        'react', 
        'React!', 
        'node.js', 
        'Python', 
        'python3', 
        'MySQL', 
        'Kubernetes', 
        'Unknown Tech'
    ]
    
    for tech in test_technologies:
        category, service = find_technology_category(tech, it_skills_mapping)
        if category and service:
            print(f"Technology: {tech}")
            print(f"Category: {category}")
            print(f"Service: {service}")
            print("-" * 40)
        else:
            print(f"Technology: {tech} - Not Found")
            print("-" * 40)

# Inline test
if __name__ == "__main__":
    demonstrate_technology_lookup()