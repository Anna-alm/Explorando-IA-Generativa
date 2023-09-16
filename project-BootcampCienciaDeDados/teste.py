import pandas as pd
import requests
import json
import openai

# EXTRACT
sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"
df = pd.read_csv("sdw_2023.csv")
user_ids = df["UserID"].tolist()
print(user_ids)


def get_user(id):
    response = requests.get(f"{sdw2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

# TRANSFORM
openai.api_key = "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"


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em marketing bancário",
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']}, sobre como juntar pontos no cartão de crédito (máximo de 100 caracteres).",
            },
        ],
    )
    return completion.choices[0].message.content.strip('"')


for user in users:
    news = generate_ai_news(user)
    print(news)
    user["news"].append({"description": news})


# LOAD
def update_user(user):
    response = requests.put(f"{sdw2023_api_url/{user['id']}}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")
