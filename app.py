import streamlit as st
from RealtimeSearch import *

def process_text(input_text):
    # Implement your processing logic here
    # For now, let's just return the input text as it is
    return input_text*10

def main():
    st.title("Intelligent Web Search")

    # Input field for user text
    user_query = st.text_area("What do you want to know today?", "")

    # Button to trigger processing
    if st.button("Process Text"):
        google_search_query = generate_google_search_query(user_query, call_as_function=True)
        print(f"Converted Google Search Query: {google_search_query}")

        if google_search_query:
            # Fetch news URLs based on the generated query
            print("Fetching news URLs based on the generated query...")
            news_urls = get_google_results(google_search_query)

            # Scrape content from the websites
            if news_urls:
                print("Scraping URL...")
                url, news_content = scrape_website(news_urls[1])

                if news_content is None:
                    raise Exception("news_content is None")

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

                response += "\n\nSources:\n" + url
                print("\nResponse GPT-4:-")
                print(response)

            else:
                print("No news articles found for your query.")

        else:
            print("Failed to generate a Google search query.")

        # Display the processed text
        st.subheader("Processed Text:")
        st.write(response)

if __name__ == "__main__":
    main()
