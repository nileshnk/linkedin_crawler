from linkedin_api import Linkedin
import json
from collections import defaultdict
from dotenv import load_dotenv
import os

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
api = ExtendedLinkedin('nilesh.txt@gmail.com', 'R@ndom@123')


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

def extract_content_from_posts(post):
    try:
        return post['summary']['text']
    except KeyError as e:
        print(f"Key error extracting content from post: {e}")
        return None

def get_post_details(urn_id):
    try:
        return api.getPost(urn_id)
    except Exception as e:
        print(f"Error getting post details for URN {urn_id}: {e}")
        return {}

def find_actor_identifier(post):
    try:
        return post['value']['com.linkedin.voyager.feed.render.UpdateV2']['actor']['image']['attributes'][0]['miniProfile']['publicIdentifier']
    except KeyError as e:
        print(post)
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

for keyword in keywords:
    try:
        posts = search_posts(keyword)
        print(len(posts))
        for post in posts:
            post_urn_id = post['trackingUrn']
            post_details = get_post_details(post_urn_id)
            actor_identifier = find_actor_identifier(post_details)
            print(actor_identifier)
            # profile = api.get_profile(actor_identifier)
            # print(profile)
    except Exception as e:
        print(f"Error processing keyword {keyword}: {e}")



