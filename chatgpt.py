import os
from openai import OpenAI


class ChatGPT:
    client = None

    def __init__(self):
        self.client = OpenAI()

    def ask(self, question):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            model="gpt-4o",
            temperature=0.5
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    # Code to be executed when the script is run as the main script
    chatbot = ChatGPT()
    question = input("Enter a question: ")
    answer = chatbot.ask(question)
    print("Answer:", answer)
