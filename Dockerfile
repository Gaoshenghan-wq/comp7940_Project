
FROM python:3.12


WORKDIR /app


COPY chatBot.py /app/
COPY requirements.txt /app/
COPY ChatGPT_HKBU_ENV.py /app/
COPY testEnv.py /app/

# RUN pip install pip
RUN pip install --no-cache-dir -r requirements.txt

# ENV TELEGRAM_ACCESS_TOKEN="7172815084:AAHnACnyEaAQqEgdak_1TRNmirSRL4eHHcs"
# ENV REDIS_HOST="redis-18794.c44.us-east-1-2.ec2.redns.redis-cloud.com"
# ENV REDIS_PASSWORD="8nViRuqdrhrWc5croORDmLorWqYAsmR9"
# ENV REDIS_PORT="18794"
# ENV REDIS_DECODE_RESPONSES="True"
# ENV REDIS_USERNAME="default"
ENV CHATGPT_BASE_URL="https://genai.hkbu.edu.hk/general/rest"
ENV CHATGPT_MODEL_NAME="gpt-4-o-mini"
ENV CHATGPT_API_VERSION="2024-05-01-preview"
# ENV CHATGPT_ACCESS_TOKEN="7db41f7a-d28a-4228-ad7e-d975aaea8e8a"

CMD ["python", "chatBot.py"]