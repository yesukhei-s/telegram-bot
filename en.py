from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import openai
import eng_to_ipa as p
from moviepy.editor import AudioFileClip
import boto3
import random
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

openai.api_key = config['openai_key']
TELEGRAM_API_TOKEN = config['telegram_key']
AWS_KEY_ID = config['aws_key_id']
AWS_ACCESS_KEY = config['aws_access_key']
GOOGLE_TRANSLATE_API_KEY = config['google_key']

subjects = ['family', 'relationships', 'appearance', 'character & behavior', 'feelings', 'houses and apartments', 'eating', 'movies & books', 'music', 'sports', 'health & sickness', 'computers', 'study', 'academic english', 'work', 'business', 'money', 'travel', 'weather', 'city', 'countryside', 'crime', 'law & justice', 'war & peace', 'global problems', 'time', 'sound', 'size', 'light', 'color', 'texture', 'smell', 'taste', 'statistics', 'movement & speed', 'changes', 'speaking', 'starting & finishing', 'success & failure', 'cause & effect', 'memories', 'agreeing & disagreeing', 'beliefs & doubts', 'deciding & choosing', 'claiming & denying', 'liking & disliking', 'praising & criticizing', 'metaphor', 'confusing words', 'everydays verbs']
subject = subjects[0]

start = "You are English teacher, let's engage in a conversation to practice informal English. Keep your responses simple and concise for effective practice."
messages = [{"role": "system", "content": start}]

def text_message(update, context):
    user = update.effective_user
    user_id = user.id
    if user_id != 6365264388:
        return

    messages.append({"role": "user", "content": update.message.text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(text=f"*[Bot]:* {ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": ChatGPT_reply})

def voice_message(update, context):
    user = update.effective_user
    user_id = user.id
    if user_id != 6365264388:
        return

    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="en").text
    update.message.reply_text(text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(text=f"*[Bot]:* {ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    polly_client = boto3.Session(
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_KEY,
            region_name='ap-northeast-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = ChatGPT_reply)

    with open('output.mp3', 'wb') as audio_file:
        audio_file.write(response['AudioStream'].read())
        audio_file.close()

    with open('output.mp3', 'rb') as voice_file:
        update.message.reply_voice(voice_file)

def restart(update, context):
    random_number = random.randint(0, 48)
    subject = subjects[random_number]
    messages = [{"role": "system", "content": start}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content":  "Generate one short random question with given subject: "+ subject}]
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "system", "content": ChatGPT_reply})
    update.message.reply_text(text=f"*[Bot]:* Subject: {subject}", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[Bot]:* {ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)

    polly_client = boto3.Session(
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_KEY,
            region_name='ap-northeast-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = ChatGPT_reply)

    with open('output.mp3', 'wb') as audio_file:
        audio_file.write(response['AudioStream'].read())
        audio_file.close()

    with open('output.mp3', 'rb') as voice_file:
        update.message.reply_voice(voice_file)

def word(update, context):
    lines = []
    with open('oxford3000.txt', 'r') as file:
        lines = file.readlines()

    max = 3869
    #max = 458
    random_number = random.randint(0, max)
    word = lines[random_number].strip()
    update.message.reply_text(text=f"*[Bot]:* {word}", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[Bot]:* /{p.convert(word)}/", parse_mode=telegram.ParseMode.MARKDOWN)

    polly_client = boto3.Session(
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_KEY,
            region_name='ap-northeast-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = word)

    with open('output.mp3', 'wb') as audio_file:
        audio_file.write(response['AudioStream'].read())
        audio_file.close()

    with open('output.mp3', 'rb') as voice_file:
        update.message.reply_voice(voice_file)

updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
dispatcher.add_handler(CommandHandler('r', restart))
dispatcher.add_handler(CommandHandler('w', word))
updater.start_polling()
updater.idle()
