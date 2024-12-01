import json
from datetime import datetime, timedelta
import uuid

def transform_linkedin_lead(actor_data, post_content):
    """
    Transform LinkedIn profile data into a standardized lead format.
    
    :param actor_data: Dictionary containing LinkedIn profile information
    :param post_content: String containing additional notes from the post
    :return: Dictionary with transformed lead information
    """
    # Generate a unique lead ID
    lead_id = str(uuid.uuid4())
    
    # Extract contact name
    first_name = actor_data.get('firstName', 'Unknown')
    last_name = actor_data.get('lastName', '')
    
    # Extract job title and skills from headline
    job_title = actor_data.get('headline', 'Software Developer')
    
    experience = actor_data.get('experience', [])
    company_name = ""
    if experience:
        company_name = experience[0].get('companyName', 'Not Specified')
    else:
        company_name = 'No Experience Listed'
    # Extract skills
    skills = [skill.get('name', '').strip() for skill in actor_data.get('skills', [])]
    
    # Prepare interested services based on skills
    interested_services = []
    skill_service_mapping = {
        'React.js': 'Web Application Development',
        'Java': 'Backend Development',
        'SQL': 'Database Management',
        'Full-Stack Development': 'Full-Stack Development'
    }
    
    for skill in skills:
        for key, service in skill_service_mapping.items():
            if key.lower() in skill.lower() and service not in interested_services:
                interested_services.append(service)
    
    # If no services found, use a default
    if not interested_services:
        interested_services = ['Custom Software Development', 'IT Consulting']
    
    # Prepare lead transformation
    lead = {
        "lead_id": lead_id,
        "contact_name": f"{first_name} {last_name}".strip(),
        "job_title": job_title,
        "company_name": company_name,
        "company_size": "1-50 employees",  # Default assumption for individual profile
        "industry": actor_data.get('industryName', 'Technology'),
        "email": None,  # LinkedIn data doesn't provide email
        "phone": None,  # LinkedIn data doesn't provide phone
        "website": None,
        "location": {
            "city": actor_data.get('geoLocationName', None),
            "state": None,  # Not provided in the data
            "country": actor_data.get('geoCountryName', None)
        },
        "source": "LinkedIn",
        "lead_status": "New",
        "interested_services": interested_services,
        "estimated_budget": "$10,000 - $50,000",  # Estimated based on individual profile
        "preferred_contact_method": "LinkedIn Message",
        "notes": post_content or "Potential lead from LinkedIn profile",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "last_contacted_at": None,
        "next_follow_up_date": (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"
    }
    
    return lead

print("we are in transformation")
print("******")
# Example usage
sample_linkedin_data = {
    "title": {"text": "Francesco Longo"},
    "primarySubtitle": {"text": "Software Developer | JS, TS, ReactJS, NextJS, React Native, Firebase 🔥| AI Enthusiast 💡| SoC Mentor 👨🏻‍🏫 | Lifelong Learner 📊"}
}

sample_post_content = "Exciting Opportunity Alert! Big news—I'm available for hire! I've worked with great tech like NextJs, Firebase, React, and various other libraries and APIs."



# Transform the data
def start_transformation():
    # read from json file profileData.json
    with open('profileData.json', 'r') as file:
        data = json.load(file)
        
        # Check if data is a list and get the first element if so
        if isinstance(data, list):
            actor_data = data[0]  # Assuming you want the first item
        else:
            actor_data = data
        
        transformed_lead = transform_linkedin_lead(actor_data, sample_post_content)
        print(json.dumps(transformed_lead, indent=2))
        
        # write to a new json file
        with open('transformed_lead.json', 'w') as file:
            json.dump(transformed_lead, file, indent=2)

start_transformation()