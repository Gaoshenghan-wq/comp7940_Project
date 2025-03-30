from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext, ConversationHandler)
import logging
import os
import pymongo 
from ChatGPT_HKBU_ENV import HKBU_ChatGPT
import random

# connection_string = os.getenv("AZURE_COSMOS_CONNECTIONSTRING")
connection_string = os.getenv("AZURE_COSMOS_COSMOS_90AE2_CONNECTIONSTRING")

client = pymongo.MongoClient(connection_string)
print('db connect success')
db = client["7940"]
question_collection = db["questions"]
last_questions = []

QUESTION_TYPE, QUESTION_TEXT, QUESTION_ANSWER, QUESTION_OPTIONS, QUESTION_TYPES = range(5)

def start_add_question(update: Update, context: CallbackContext) -> int:
    """启动添加问题的对话流程"""
    update.message.reply_text("Let's add a new question. Please enter the question type (1: Multiple Choice, 2: True/False, 3: Short Answer):")
    return QUESTION_TYPE

def get_question_type(update: Update, context: CallbackContext) -> int:
    """获取问题类型"""
    context.user_data['question_type'] = int(update.message.text)
    if context.user_data['question_type'] not in [1, 2, 3]:
        update.message.reply_text("Invalid question type. Please use 1, 2, or 3.")
        return QUESTION_TYPE

    update.message.reply_text("Please enter the question text:")
    return QUESTION_TEXT

def get_question_text(update: Update, context: CallbackContext) -> int:
    """获取问题内容"""
    context.user_data['question_text'] = update.message.text
    update.message.reply_text("Please enter the answer to the question:")
    return QUESTION_ANSWER

def get_question_answer(update: Update, context: CallbackContext) -> int:
    """获取问题答案"""
    context.user_data['answer'] = update.message.text

    if context.user_data['question_type'] == 1:
        update.message.reply_text("Please enter the options for the question (A, B, C, D):")
        return QUESTION_OPTIONS
    else:
        update.message.reply_text("Please enter the types of the question (e.g., geography, capital cities):")
        return QUESTION_TYPES

def get_question_options(update: Update, context: CallbackContext) -> int:
    """获取问题选项"""
    options = update.message.text.split(',')
    context.user_data['options'] = [
        {"option": "A", "text": options[0].strip()},
        {"option": "B", "text": options[1].strip()},
        {"option": "C", "text": options[2].strip()},
        {"option": "D", "text": options[3].strip()}
    ]
    update.message.reply_text("Please enter the types of the question (e.g., geography, capital cities):")
    return QUESTION_TYPES

def get_question_types(update: Update, context: CallbackContext) -> int:
    """获取问题类别"""
    types = update.message.text.split(',')
    context.user_data['types'] = [type.strip() for type in types]

    question = {
        # "question_content": {
        #     "text": context.user_data['question_text'],
        #     "options": context.user_data.get('options', [])
        # },
        "question_type": context.user_data['question_type'],
        "answer": context.user_data['answer'],
        "type": context.user_data['types']
    }

    if context.user_data['question_type'] == 1:
        question["question_content"] = {
            "text": context.user_data['question_text'],
            "options": context.user_data.get('options', [])
        }
    else: 
        question["question_content"] = context.user_data['question_text']
    result = question_collection.insert_one(question)
    if result.inserted_id:
        update.message.reply_text("Question added successfully.")
    else:
        update.message.reply_text("Failed to add question.")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """取消对话"""
    update.message.reply_text("Adding question canceled.")
    return ConversationHandler.END



def equipped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
def main():
    # Load configuration from environment variables
    telegram_access_token = os.getenv("TELEGRAM_ACCESS_TOKEN")
    chatgpt_base_url = os.getenv("CHATGPT_BASE_URL")
    chatgpt_model_name = os.getenv("CHATGPT_MODEL_NAME")
    chatgpt_api_version = os.getenv("CHATGPT_API_VERSION")
    chatgpt_access_token = os.getenv("CHATGPT_ACCESS_TOKEN")

    print(123)
    # Create an Updater for your Bot
    updater = Updater(token=telegram_access_token, use_context=True)
    dispatcher = updater.dispatcher


    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Initialize ChatGPT instance
    global chatgpt
    chatgpt = HKBU_ChatGPT()



    # Command handlers
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("anzureConnect", gitFly))
    dispatcher.add_handler(CommandHandler("findQuestion", find_question))
    dispatcher.add_handler(CommandHandler("answer", answer))
    dispatcher.add_handler(CommandHandler("askGpt", ask_gpt))
    dispatcher.add_handler(CommandHandler("deleteQuestion", delete_question))

    add_question_handler = ConversationHandler(
        entry_points=[CommandHandler('add_question', start_add_question)],
        states={
            QUESTION_TYPE: [MessageHandler(Filters.text & ~Filters.command, get_question_type)],
            QUESTION_TEXT: [MessageHandler(Filters.text & ~Filters.command, get_question_text)],
            QUESTION_ANSWER: [MessageHandler(Filters.text & ~Filters.command, get_question_answer)],
            QUESTION_OPTIONS: [MessageHandler(Filters.text & ~Filters.command, get_question_options)],
            QUESTION_TYPES: [MessageHandler(Filters.text & ~Filters.command, get_question_types)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(add_question_handler)

    # Register handlers
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equipped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
    # Start the bot
    updater.start_polling()
    updater.idle()

def ask_gpt(update: Update, context: CallbackContext) -> None:
    try:
        question_number = int(context.args[0]) - 1 
        if question_number < 0 or question_number >= len(last_questions):
            update.message.reply_text("Invalid question number. Please use /findQuestion first.")
            return

        question = last_questions[question_number]
        question_text = question['question_content']
        if question['question_type'] == 1:
            question_text = question['question_content']['text']
            for option in question['question_content']['options']:
                question_text += f"\n{option['option']}. {option['text']}"
        global chatgpt
        gpt_response = chatgpt.submit(question_text)
        update.message.reply_text(f"GPT Response: {gpt_response}")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /ask_gpt <question_number>")

def answer(update: Update, context: CallbackContext) -> None:
    if not last_questions:
        update.message.reply_text("No questions have been retrieved yet. Please use /findQuestion first.")
        return

    response = "Answers:\n"
    for index, question in enumerate(last_questions, start=1):
        response += f"{index}. Answer: {question['answer']}\n"
    update.message.reply_text(response)
def find_question(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    try:
        question_type = context.args[0]  
        number_of_questions = int(context.args[1])  
        questions = list(question_collection.find({"type": {"$in": [question_type]}}))
        logging.info(questions)
        response = ""
        last_questions.clear() 
        if len(questions) > number_of_questions:
            questions = random.sample(questions, number_of_questions)
        for index, question in enumerate(questions, start=1):
            logging.info(question)
            if question['question_type'] == 1: 
                response += f"{index}. Question: {question['question_content']['text']}\n"
                for option in question['question_content']['options']:
                    response += f"{option['option']}. {option['text']}\n"
                response += "\n"
            elif question['question_type'] == 2: 
                response += f"{index}. Question: {question['question_content']}\n\n"
            elif question['question_type'] == 3: 
                response += f"{index}. Question: {question['question_content']}\n\n"
            last_questions.append(question)
        if not response:
            response = "No questions found."
        update.message.reply_text(response)
    except (IndexError, ValueError):
        logging.info(ValueError, IndexError)
        update.message.reply_text("Usage: /findQuestion <questionType> <numberOfQues>")

def delete_question(update: Update, context: CallbackContext) -> None:
    try:
        question_number = int(context.args[0]) - 1  # 用户输入的序号从1开始，实际索引从0开始
        if question_number < 0 or question_number >= len(last_questions):
            update.message.reply_text("Invalid question number. Please use /findQuestion first.")
            return

        # 获取要删除的问题
        question_to_delete = last_questions[question_number]
        question_id = question_to_delete["_id"]

        # 从数据库中删除问题
        result = question_collection.delete_one({"_id": question_id})
        if result.deleted_count > 0:
            # 从 last_questions 中删除问题
            del last_questions[question_number]
            update.message.reply_text("Question deleted successfully.")
        else:
            update.message.reply_text("Failed to delete question.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /delete <questionNumber>")

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def hello(update: Update, context: CallbackContext) -> None:
    try:
        name = context.args[0]  # Get the name from the command argument
        update.message.reply_text(f"Good day, {name}!")
    except IndexError:
        update.message.reply_text("Usage: /hello <name>")

def gitFly(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"anzure connect success!")



if __name__ == '__main__':
    main()