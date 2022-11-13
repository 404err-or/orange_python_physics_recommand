from orangecontrib.text.vectorization.sbert import SBERT
from orangecontrib.text import Corpus
from Orange.util import dummy_callback
import pickle

text = '그림 (가), (나)는 주사 전자 현미경(SEM)으로 동일한 시료를 촬영한 사진을 나타낸 것이다. 촬영에 사용된 전자의 운동 에너지는 (가)에서가 (나)에서보다 작다.'
model = pickle.load(open('model.pkcls', 'rb'))
sbert = SBERT()
corpus = Corpus.from_file("from_junmin/test.csv")

def predict(text):
    # test.csv 파일에 3개 정도는 들어있어야 예측이 가능함.
    # => 미리 3개 넣어두고 list에 추가함으로써 sbert 인코딩.
    data = sbert(texts=corpus.documents + [text], callback=dummy_callback)
    return model(data[-1]) + 1

print(text)
res = predict(text)
print(type(res))
print(res == 7.0)
print(str(res) == '7.0')