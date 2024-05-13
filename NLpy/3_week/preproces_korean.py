from konlpy.tag import Komoran
import re

# 사용자 사전 경로 지정합
user_dic_path = 'user_dic.txt'

# 사용자 사전을 이용하여 Komoran 객체를 생성
komoran = Komoran(userdic=user_dic_path)

# 불용어 리스트를 정의
stopwords = ['이', '그', '저']

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

        # HTML 태그 제거: '<'로 시작해서 '>'로 끝나는 모든 문자열을 공백으로 대체
        cleaned_text = re.sub(r'<[^>]*>', ' ', self.text)
        # 한글, 숫자, 공백을 제외한 모든 문자 제거
        cleaned_text = re.sub(r"[^가-힣ㄱ-ㅎㅏ-ㅣ0-9\s]", "", cleaned_text)
        # 연속된 공백을 하나의 공백으로 변환
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        # 문자열 양 끝의 공백 제거
        self.text = cleaned_text.strip()
        return self

    def tokenize(self):
        """토큰화: 문장을 의미 있는 최소 단위로 분리"""
        self.tokens = komoran.morphs(self.text)
        return self

    def remove_stopwords(self):
        """불용어 처리: 의미 분석에 불필요한 단어들을 제거"""
        self.tokens = [word for word in self.tokens if word not in stopwords]
        return self

    def normalize(self):
        """정규화: 비슷한 의미의 단어를 통일된 형태로 변환"""
        self.tokens = ['않다' if word in ['안', '않다'] else word for word in self.tokens]
        return self

    def get_preprocessed_text(self):
        """전처리된 텍스트 데이터를 반환"""
        return ' '.join(self.tokens)

# 사용 예시
filepath = 'scraped_data.txt'
file_reader = FileReader(filepath)
text = file_reader.read_text()

preprocessor = TextPreprocessor(text)
preprocessed_text = preprocessor.clean_text().tokenize().remove_stopwords().normalize().get_preprocessed_text()

print(preprocessed_text)

with open('kor_token.txt', 'w') as f:
    f.write(preprocessed_text)