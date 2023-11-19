from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import requests
import json

# Load environment variables from the .env file
load_dotenv()

# Create OpenAI client object
client = OpenAI()

def generate_google_search_query(user_query):
    """ Uses GPT4 to convert the query enterred by the user into a more optimized query that can provide good results from a google search.
    """
    system_prompt = "You are a Google Search expert. Your task is to convert unstructured user inputs to optimized Google search queries. Example: USER_INPUT: 'Who was the winner of the 2023 ICC Cricket World Cup?' OPTIMIZED Google search query: 'ICC cricket world cup winner 2023'"
    
    prompt = f"Convert the following user query into an optimized Google search query: {user_query}"

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    if response.choices:
        response_message = response.choices[0].message

        if hasattr(response_message, 'content'):
            return response_message.content.strip()
        else:
            return "No content in response."
    else:
        return "No response from GPT-4 Turbo"


def get_google_results(query, num_results = 3, location="Canada"):
    """Runs a google search and returns URLs of the top results using Beautiful Soup

    Args:
        query (str): Search query to run on Google 
        num_results (int, optional): Number of search result URLs to return. Defaults to 3.
        location (str, optional): [description]. Defaults to "Canada".

    Returns:
        [type]: [description]
    """

    google_url = 'https://www.google.com/search'

    headers = {
        'Accept' : '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
    }
    parameters = {'q': query}

    content = requests.get(google_url, headers = headers, params = parameters).text
    soup = BeautifulSoup(content, 'html.parser')

    search = soup.find(id = 'search')
    urls = search.find_all('a')
    #print(urls)
    urls = [h['href'] for h in urls if h['href'].startswith('https')]
    
    print(urls)
    print("\n")
    return urls[:num_results]


def scrape_website(url):
    """Uses Beautiful Soup to scrape a URL and returns the data

    Args:
        url (str): url to be scraped

    Returns:
        str: Content of the URL
    """
    # Make a GET request to the website
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find and extract the text content of the website
        paragraphs = soup.find_all('p')

        scraped_data = [p.get_text() for p in paragraphs]

        formatted_data = "\n".join(scraped_data)

        return url, formatted_data
    else:
        # If the request was not successful, print an error message
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return url, None
        

if __name__ == "__main__":    
    while True:
        user_query = input("Please enter your query (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break

        google_search_query = generate_google_search_query(user_query)
        print(f"Converted Google Search Query: {google_search_query}")

        if google_search_query:
            # Fetch news URLs based on the generated query
            print("Fetching news URLs based on the generated query...")
            news_urls = get_google_results(google_search_query)

            # Scrape content from the websites
            if news_urls:
                print("Scraping URL...")
                url, news_content = scrape_website(news_urls[0])

                if news_content is None:
                    break

                context = f"Context: {news_content}\nUser Query: {user_query}"
                print(context)

                # Chat completion request with context
                completion = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant, always return only the essencial parts that answer the USER original USER query, but add 3 bullet points to backup your reasoning for the answer."},
                        {"role": "user", "content": context}
                    ]
                )

                # Process and display response
                response = completion.choices[0].message.content if completion.choices[0].message else ""

                print("\nResponse GPT-4:-")
                print(response)

            else:
                print("No news articles found for your query.")

        else:
            print("Failed to generate a Google search query.")