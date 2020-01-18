from ckiptagger import WS, POS, NER
from gaisTokenizer import Tokenizer


gt = Tokenizer()
ws = WS('./data', disable_cuda=True)
pos = POS('./data', disable_cuda=True)
ner = NER('./data', disable_cuda=True)


sentence = '美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。'
result_token = gt.tokenize(sentence)
result_token = [result_token]
# result_token = ws([sentence])
result_pos = pos(result_token)
print(result_pos, result_token)
result_ner = ner(result_token, result_pos)

print(result_ner)
