from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    # def ready(self):
    #     # 서버가 실행될 때 모든 영화 제목의 임베딩 계산
    #     from . import embedding
    #     embedding.calculate_movie_embeddings()
