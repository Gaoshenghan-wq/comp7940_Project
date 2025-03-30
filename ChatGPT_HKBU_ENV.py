import os
import requests

class HKBU_ChatGPT():
    def __init__(self):
        self.base_url = os.getenv("CHATGPT_BASE_URL")
        self.model_name = os.getenv("CHATGPT_MODEL_NAME")
        self.api_version = os.getenv("CHATGPT_API_VERSION")
        self.access_token = os.getenv("CHATGPT_ACCESS_TOKEN")

    def submit(self, message):   
        conversation = [{"role": "user", "content": message}]
        
        url = f"{self.base_url}/deployments/{self.model_name}/chat/completions/?api-version={self.api_version}"
        
        headers = { 
            'Content-Type': 'application/json', 
            'api-key': self.access_token 
        }
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f'Error: {response.status_code}, {response.text}'

if __name__ == '__main__':
    ChatGPT_test = HKBU_ChatGPT()
    while True:   
        user_input = input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)