import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# NLTK 불용어 리스트를 불러옵니다.
stop_words = set(stopwords.words('english'))

class FileReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_text(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

class TextPreprocessor:
    def __init__(self, text):
        self.text = text
        self.tokens = []

    def clean_text(self):
        """데이터 정제: HTML 태그, 특수 문자 제거 및 공백 정리."""

        # HTML 태그 제거
        cleaned_text = re.sub(r'<[^>]*>', ' ', self.text)
        # 영문자, 숫자, 공백을 제외한 모든 문자 제거
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_text)
        # 연속된 공백을 하나의 공백으로 변환
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        # 문자열 양 끝의 공백 제거
        self.text = cleaned_text.strip()
        return self

    def tokenize(self):
        """토큰화: 문장을 단어 단위로 분리"""
        self.tokens = word_tokenize(self.text)
        return self

    def remove_stopwords(self):
        """불용어 처리: 의미 분석에 불필요한 단어들을 제거"""
        self.tokens = [word for word in self.tokens if word.lower() not in stop_words]
        return self

    def lemmatize(self):
        """표제어 추출: 단어를 기본형으로 변환"""
        lemmatizer = WordNetLemmatizer()
        self.tokens = [lemmatizer.lemmatize(word) for word in self.tokens]
        return self

    def get_preprocessed_text(self):
        """전처리된 텍스트 데이터를 반환"""
        return ' '.join(self.tokens)

# 사용 예시
filepath = 'eng_raw_data.txt'
file_reader = FileReader(filepath)
text = file_reader.read_text()

preprocessor = TextPreprocessor(text)
preprocessed_text = preprocessor.clean_text().tokenize().remove_stopwords().lemmatize().get_preprocessed_text()

print(preprocessed_text)

with open('eng_token.txt', 'w', encoding='utf-8') as f:
    f.write(preprocessed_text)
