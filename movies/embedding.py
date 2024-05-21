from transformers import AutoTokenizer, AutoModel
import torch
from .models import Movie

# 사전 학습된 토크나이저, 언어 모델 가져오기
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def calculate_movie_embeddings():
    movies = Movie.objects.all()

    for idx, movie in enumerate(movies):
        print(idx, movie)
        # 모델이 해석 할 수 있도록 텍스트 입력을 숫자로 변환
        title_tokens = tokenizer(movie.title, return_tensors='pt', truncation=True, padding=True)

        # 토크나이저의 결과를 이용해 모델을 통해 임베딩 계산
        with torch.no_grad():
            title_embedding = model(**title_tokens).last_hidden_state.mean(dim=1).squeeze().tolist()

        movie.embedding = title_embedding

        # 장르 임베딩 계산
        genre_embeddings = []
        for genre in movie.genres.all():
            genre_tokens = tokenizer(genre.name, return_tensors='pt', truncation=True, padding=True)
            with torch.no_grad():
                genre_embedding = model(**genre_tokens).last_hidden_state.mean(dim=1).squeeze().tolist()
            genre_embeddings.append(genre_embedding)

        # 여러 장르의 임베딩을 평균 -> 하나의 임베딩으로 결합
        if genre_embeddings:
            genre_embedding_avg = [sum(embeds) for embeds in zip(*genre_embeddings)]
        else:
            genre_embedding_avg = []

        movie.genre_embedding = genre_embedding_avg

        movie.save()

        

