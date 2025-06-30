from jamdict import Jamdict
import MeCab

tagger = MeCab.Tagger("-Owakati")
jam = Jamdict()

sentence = "明日は友達と映画館に行く予定です。"
result = tagger.parse(sentence)
words = result.split()

print(words)
