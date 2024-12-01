from linkedin_api import Linkedin
import json
from collections import defaultdict
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
from transformation import transform_linkedin_lead
load_dotenv()

class ExtendedLinkedin(Linkedin):
    def getPost(self, entityUrn):
        """Fetch data for a given LinkedIn post.

        :param entityUrn: LinkedIn URN ID for a post
        :type entityUrn: str

        :return: Post data
        :rtype: dict
        """
        res = self._fetch(f"/feed/updates/{entityUrn}")

        data = res.json()

        # if data and "status" in data and data["status"] != 200:
        #     self.logger.info("request failed: {}".format(data["message"]))
        #     return {}

        return data


linkedin_email = os.getenv('LINKEDIN_EMAIL')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')
api = ExtendedLinkedin(linkedin_email, linkedin_password)


# add the function to read a text file and save the data in an array
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

keywords_file_path = 'keywords.txt'
keywords = read_text_file(keywords_file_path)

def save_post_data(post):
    json.dumps(post)
    file_path = "postData.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as postData_file:
            json.dump([], postData_file)
    
    with open(file_path, "r+") as postData_file:
        data = json.load(postData_file)
        data.append(post)
        postData_file.seek(0)
        json.dump(data, postData_file, indent=4)


def extract_content_from_posts(post):
    try:
        return post['summary']['text']
    except KeyError as e:
        print(f"Key error extracting content from post: {e}")
        return None

def save_post_data(post):
    json.dumps(post)
    file_path = "postData.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as postData_file:
            json.dump([], postData_file)
    
    with open(file_path, "r+") as postData_file:
        data = json.load(postData_file)
        data.append(post)
        postData_file.seek(0)
        json.dump(data, postData_file, indent=4)

def save_profile_data(profile):
    if profile is None:
        return
    
    json.dumps(profile)
    file_path = "profileData.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as profileData_file:
            json.dump([], profileData_file)
    
    with open(file_path, "r+") as profileData_file:
        data = json.load(profileData_file)
        data.append(profile)
        profileData_file.seek(0)
        json.dump(data, profileData_file, indent=4)



def get_post_details(urn_id):
    try:
        post = api.getPost(urn_id)
        # save_post_data(post)
        return post
    except Exception as e:
        print(f"Error getting post details for URN {urn_id}: {e}")
        return {}



def find_actor_identifier(post):
    try:
        return post['value']['com.linkedin.voyager.feed.render.UpdateV2']['actor']['image']['attributes'][0]['miniProfile']['publicIdentifier']
    except KeyError as e:
        save_post_data(post)

        # print(post)
        print(f"Key error finding actor identifier: {e}")
        return None

def search_posts(keyword, search_limit=5):
    try:
        searchParams = defaultdict()
        searchParams["keywords"] = keyword
        searchParams["resultType"] = "CONTENT"
        posts = api.search(searchParams, limit=search_limit)
        return posts
    except Exception as e:
        print(f"Error searching posts with keyword {keyword}: {e}")
        return []

def process_linkedin_url(url):
    # try:
        # Parse the URL
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip('/').split('/')

    # Check if the URL is a profile or a company
    if len(path_segments) > 1:
        if path_segments[0] == 'in':
            urn_id = path_segments[1]
            return api.get_profile(urn_id=urn_id)
        elif path_segments[0] == 'company':
            company_id = path_segments[1]
            return api.get_company(company_id=company_id)
    # except Exception as e:
    #     print(f"Error processing LinkedIn URL {url}: {e}")
    
    return None

def data_transformation(post_content, actor_data):
    return {
        "post_content": post_content,
        "actor_data": actor_data
    }


for keyword in keywords:
    try:
        posts = search_posts(keyword)
        print(len(posts))
        for post in posts:
            if post['actorNavigationContext'] is None:
                continue
            text_content = extract_content_from_posts(post)
            actor_url = post['actorNavigationContext']['url']
            actor_data = process_linkedin_url(actor_url)

            # save_profile_data(actor_data)
            
            transformed_lead = transform_linkedin_lead(actor_data, text_content)

    except Exception as e:
        print(f"Error processing keyword {keyword}: {e}")



