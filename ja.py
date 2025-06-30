from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import openai
from moviepy.editor import AudioFileClip
import boto3
import romkan
from pykakasi import kakasi
import requests
import html
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

openai.api_key = config['openai_key']
TELEGRAM_API_TOKEN = config['telegram_key']
AWS_KEY_ID = config['aws_key_id']
AWS_ACCESS_KEY = config['aws_access_key']
GOOGLE_TRANSLATE_API_KEY = config['google_key']

start = "You are Saya, let's engage in conversation to practice informal Japanese. Keep your simple and responses concise for effective practice."
messages = [{"role": "system", "content": start}]

kakasi = kakasi()
kakasi.setMode("J", "a")
conv = kakasi.getConverter()

def translate_text(text, language="en"):
    base_url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": GOOGLE_TRANSLATE_API_KEY,
        "q": text,
        "target": language,
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if "data" in data and "translations" in data["data"]:
        translation = html.unescape(data["data"]["translations"][0]["translatedText"])
        return translation
    else:
        return None

def text_message(update, context):
    user = update.effective_user
    user_id = user.id
    if user_id != 6365264388:
        return

    translated_text = translate_text(update.message.text, language="ja")
    update.message.reply_text(text=f"*[You]:* _{translated_text}_", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[You]:* _{romkan.to_roma(conv.do(translated_text))}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": translated_text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(text=f"*[Bot]:* {ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[Bot]:* {romkan.to_roma(conv.do(ChatGPT_reply))}", parse_mode=telegram.ParseMode.MARKDOWN)
    translated_text = translate_text(ChatGPT_reply, language="en")
    update.message.reply_text(text=f"*[Bot]:* {translated_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    polly_client = boto3.Session(
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_KEY,
            region_name='ap-northeast-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Mizuki',
                LanguageCode='ja-JP',
                OutputFormat='mp3', 
                Text = ChatGPT_reply)
    
    with open('ja_output.mp3', 'wb') as audio_file:
        audio_file.write(response['AudioStream'].read())
        audio_file.close()

    with open('ja_output.mp3', 'rb') as voice_file:
        update.message.reply_voice(voice_file)

def voice_message(update, context):
    user = update.effective_user
    user_id = user.id
    if user_id != 6365264388:
        return

    """ voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("ja_voice_message.ogg")
    audio_clip = AudioFileClip("ja_voice_message.ogg")
    audio_clip.write_audiofile("ja_voice_message.mp3")
    audio_file = open("ja_voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ja").text
    update.message.reply_text(text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[You]:* _{romkan.to_roma(conv.do(transcript))}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(text=f"*[Bot]:* {ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[Bot]:* {romkan.to_roma(conv.do(ChatGPT_reply))}", parse_mode=telegram.ParseMode.MARKDOWN)
    translated_text = translate_text(ChatGPT_reply, language="en")
    update.message.reply_text(text=f"*[Bot]:* {translated_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    polly_client = boto3.Session(
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_KEY,
            region_name='ap-northeast-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Mizuki',
                LanguageCode='ja-JP',
                OutputFormat='mp3', 
                Text = ChatGPT_reply)

    with open('ja_output.mp3', 'wb') as audio_file:
        audio_file.write(response['AudioStream'].read())
        audio_file.close()

    with open('ja_output.mp3', 'rb') as voice_file:
        update.message.reply_voice(voice_file) """
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("ja_voice_message.ogg")
    audio_clip = AudioFileClip("ja_voice_message.ogg")
    audio_clip.write_audiofile("ja_voice_message.mp3")
    audio_file = open("ja_voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ja").text
    update.message.reply_text(text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text(text=f"*[You]:* _{romkan.to_roma(conv.do(transcript))}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    translated_text = translate_text(transcript, language="en")
    update.message.reply_text(text=f"*[Bot]:* {translated_text}", parse_mode=telegram.ParseMode.MARKDOWN)

def restart(update, context):
    messages = [{"role": "system", "content": start}]
    update.message.reply_text(text=f"*[Bot]:* OK.", parse_mode=telegram.ParseMode.MARKDOWN)

updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
dispatcher.add_handler(CommandHandler('r', restart))
updater.start_polling()
updater.idle()
