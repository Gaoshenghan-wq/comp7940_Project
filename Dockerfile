
FROM python:3.12


WORKDIR /app


COPY chatBot.py /app/
COPY requirements.txt /app/
COPY ChatGPT_HKBU_ENV.py /app/
COPY testEnv.py /app/

# RUN pip install pip
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENV CHATGPT_BASE_URL="https://genai.hkbu.edu.hk/general/rest"
ENV CHATGPT_MODEL_NAME="gpt-4-o-mini"
ENV CHATGPT_API_VERSION="2024-05-01-preview"



CMD ["python", "chatBot.py"]