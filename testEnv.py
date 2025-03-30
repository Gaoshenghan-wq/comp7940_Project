import os

telegram_token = os.getenv('TELEGRAM_ACCESS_TOKEN')
# redis_host = os.getenv('REDIS_HOST')
# redis_password = os.getenv('REDIS_PASSWORD')
# redis_port = os.getenv('REDIS_PORT')
# redis_decode_response = os.getenv('REDIS_DECODE_RESPONSE')
# redis_user_name = os.getenv('REDIS_USER_NAME')
chatgpt_baseurl = os.getenv('CHATGPT_BASIC_URL')
chatgpt_modelname = os.getenv('CHATGPT_MODEL_NAME')
chatgpt_apiversion = os.getenv('CHATGPT_API_VERSION')
chatgpt_token = os.getenv('CHATGPT_ACCESS_TOKEN')

print(telegram_token,chatgpt_baseurl,chatgpt_modelname,chatgpt_apiversion,chatgpt_token)