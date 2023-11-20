# LLM-Powered-WebSearch

Have a question that you need an answer to but don't want to comb through large amounts of text from news articles or other websites? This tool allows you to ask questions that depend on real time data, for example “What is the latest update regarding the change in OpenAI leadership” or “Who won the most recent F1 race in Las Vegas” and get concise, summarized answers along with sources. 

Advantages of this tool:
- Ask questions in natural language.
- Get answers to questions that require realtime data , unlike what ChatGPT (with GPT 3.5) can provide (as of Nov 20th, 2023).
- Get more comprehensive answers since the tool refers to from multiple websites on the internet to answer the user query.
- Tool provides URL to the sources that it referred, greatly improving trust in the search results.

Usage:
1. Clone/Download the repository
2. Create a .env file and enter the below:
```
OPENAI_API_KEY=<Enter your OpenAI API here. You need access to GPT4 to run this>
```
3. Open a terminal and run:
```
streamlit run app.py
```
4. Open `http://localhost:8501/` on a browser and you should be ready to ask questions to the tool!

