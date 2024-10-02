import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import openai
import random
import logging
import requests
# import ffmpeg

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()  # take environment variables from .env.

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.277',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
]

# You can then use random.choice() to select a random user agent from this list
user_agent = random.choice(user_agents)

class YARS:
    def __init__(self, user_agent='Mozilla/5.0', proxy=None):
        self.headers = {'User-Agent': user_agent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        if proxy:
            self.session.proxies.update({
                'http': proxy,
                'https': proxy
            })
    
    def fetch_subreddit_posts(self, subreddit, limit=10, category='hot', time_filter='all'):
        if category not in ['hot', 'top', 'new']:
            raise ValueError("Category must be either 'hot', 'top' or 'new'")

        batch_size = min(100, limit)
        total_fetched = 0
        after = None
        all_posts = []

        while total_fetched < limit:
            url = f"https://www.reddit.com/r/{subreddit}/{category}.json"
            params = {
                'limit': batch_size,
                'after': after,
                'raw_json': 1,
                't': time_filter
            }

            response = self.session.get(url, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code}")
                return all_posts

            data = response.json()
            posts = data['data']['children']

            if not posts:
                break

            for post in posts:
                post_data = post['data']
                post_info = {
                    'title': post_data['title'],
                    'author': post_data['author'],
                    'permalink': post_data['permalink'],
                    'score': post_data['score'],
                    'num_comments': post_data['num_comments'],
                    'created_utc': post_data['created_utc']
                }

                if post_data.get('post_hint') == 'image' and 'url' in post_data:
                    post_info['image_url'] = post_data['url']
                elif 'preview' in post_data and 'images' in post_data['preview']:
                    post_info['image_url'] = post_data['preview']['images'][0]['source']['url']

                if 'thumbnail' in post_data and post_data['thumbnail'] and post_data['thumbnail'] != 'self':
                    post_info['thumbnail_url'] = post_data['thumbnail']

                all_posts.append(post_info)
                total_fetched += 1

                if total_fetched >= limit:
                    break

            after = data['data'].get('after')

            if not after:
                print("No more posts to fetch.")
                break

            time.sleep(0.5)

        return all_posts[:limit]

class OpenAIProcessor:
    def __init__(self, client):
        self.client = client

    def generate_unique_story(self, posts):
        print("Generating unique story based on scraped posts...")
        prompt = (
            "Based on the following Reddit stories, create a completely unique and uncensored story that combines elements from these posts. "
            "The story should be engaging, dramatic, and suitable for a short video. Here are the stories:\n\n"
        )
        for post in posts:
            prompt += f"Title: {post['title']}\nContent: {post.get('content', 'No content available')}\n\n"
        
        prompt += "Now, create a unique story that's different from these but inspired by their themes and drama."

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative storyteller who can craft unique, uncensored narratives based on various inputs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.9
        )

        unique_story = response.choices[0].message.content.strip()
        
        # Generate a title for the unique story
        title_prompt = f"Create a catchy, short title for the following story:\n\n{unique_story}\n\nThe title should be attention-grabbing and suitable for a short video."
        
        title_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative title generator."},
                {"role": "user", "content": title_prompt}
            ],
            max_tokens=17,
            n=1,
            stop=None,
            temperature=0.2
        )

        unique_title = title_response.choices[0].message.content.strip()

        print(f"Unique story generated. Title: {unique_title}")
        return {
            'title': unique_title,
            'content': unique_story
        }

    def text_to_speech(self, text, output_path):
        print(f"Generating audio for the story...")
        try:
            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="alloy",
                input=text
            )
            response.stream_to_file(output_path)
            print(f"Audio generated successfully and saved to {output_path}")
        except Exception as e:
            logging.error(f"Error generating audio: {e}")
            print(f"Error generating audio: {e}")

def main():
    # Create Posts folder if it doesn't exist
    posts_folder = Path("Posts")
    posts_folder.mkdir(exist_ok=True)

    # Initialize YARS
    yars = YARS(user_agent=random.choice(user_agents))

    # Default values
    default_subreddit = "AmIOverreacting"
    default_num_posts = 5

    # Get user input for subreddit and number of posts, or use defaults
    subreddit = input(f"Enter a subreddit name (default: {default_subreddit}): ").strip() or default_subreddit
    num_posts_input = input(f"Enter the number of posts to scrape (default: {default_num_posts}): ").strip()
    num_posts = int(num_posts_input) if num_posts_input else default_num_posts

    print(f"Fetching {num_posts} posts from r/{subreddit}...")

    # Use YARS to fetch Reddit posts
    posts = yars.fetch_subreddit_posts(subreddit, limit=num_posts)

    if not posts:
        logging.error("No posts were successfully fetched. Exiting.")
        print("No posts were successfully fetched. Exiting.")
        return

    # Save all posts to a single file
    all_posts_file = posts_folder / "all_posts.json"
    with open(all_posts_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    logging.info(f"Saved all posts to {all_posts_file}")

    # Initialize OpenAIProcessor
    openai_processor = OpenAIProcessor(openai.Client())

    # Generate the story based on fetched posts
    story = openai_processor.generate_unique_story(posts)

    # Create a new folder for this story
    story_folder = posts_folder / f"Story_{len(list(posts_folder.glob('Story_*'))) + 1}"
    story_folder.mkdir()

    # Save the story as a text file
    with open(story_folder / "story.txt", "w", encoding='utf-8') as f:
        f.write(f"Title: {story['title']}\n\n{story['content']}")

    # Generate audio for the story
    audio_file = story_folder / "story_audio.mp3"
    openai_processor.text_to_speech(story['content'], str(audio_file))

    print(f"Story and audio saved in {story_folder}")

if __name__ == "__main__":
    main()