from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///movie.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50))
    year = Column(Integer)
    duration = Column(Integer)
    rating = Column(Float)
    is_active = Column(Boolean, default=True)
    def __repr__(self):
        return f"<Movie (title: '{self.title}', genre: {self.genre}, year: {self.year})>"

class AddMovie:
    def create_movie(self, title, genre, year, duration, rating):
        session = Session()
        try:
            new_movie = Movie(
            title=title,
            genre = genre,
            year = year,
            duration = duration,
            rating = rating
            )
            session.add(new_movie)
            session.commit()

            print(f"Фильм {title} добавлен в базу. ID {new_movie.id}")
            return new_movie
        except Exception as e:
            session.rollback()
            print(f"Ошибка")
            return None

        finally:
            session.close()
class InfoMovie:
    session = Session()
    # def get_one_movie(self, movie):
    #     if movie:
    #         status = "Есть в кинотеатре" if movie.is_available else "Недоступен"
    #         print(f"ID {movie.id} | {movie.title} | {movie.yesr} | {movie.rating} | {movie.duration} | {status}")
    #     else:
    #         print("Фильм не найден")

    def get_all_movies(self):
        movies = self.session.query(Movie).all()
        if movies:
            for m in movies:
                print(m)
        else:
            print("Фильм не найден")
    def get_movies_by_genre(self, genre):
        if not genre:
            print("Нет тако жанра")
            return
        movies = self.session.query(Movie).filter(Movie.genre == genre).all()
        if movies:
            for m in movies:
                print(m)
    def get_high_rated_movies(self, rating):
        if not (0 <= rating <= 10):
            raise ValueError("Введите рейтинг от 1 до 10")
        else:
            return self.session.query(Movie).filter(Movie.rating >= rating).all()
    def get_movies_after_year(self, year):
        return self.session.query(Movie).filter(Movie.year > year).all()
    def get_movie_by_title(self, title):
        if not title:
            print("Нет такого фильма")
            return
        movie = self.session.query(Movie).filter(Movie.title == title).first()
        if movie:
            print(f" Фильм {title} есть в фильмотеке")
        else:
            print(f" Фильм {title} не найден")

if __name__ == "__main__":
    Base.metadata.create_all(engine)

creator = AddMovie()
info = InfoMovie()

# print("Добавляем фильмы")
# creator.create_movie("Эквилибриум", "Драмма", 2002, 106,7.6)
# creator.create_movie("Аладдин", "Мюзикл", 2019, 127,6.9)
# creator.create_movie("Мортал комбат", "Фентези", 2021, 110,6.1)
# creator.create_movie("Оно", "Ужасы", 2017, 134,7.3)
# creator.create_movie("Гнев", "Боевик", 2021, 118,7.2)
# creator.create_movie("Один дома", "Комедия", 1990, 102,7.6)

# print("Все фильмы")
# info.get_all_movies()а

# print("Все фильмы по жанру")
# info.get_movies_by_genre("Ужасы")

# print("Все фильмы выше заданного рейтинга")
# rate = info.get_high_rated_movies(7)
# print(rate)

# print("Все фильмы от 2016 года")
# y= info.get_movies_after_year(2016)
# print(y)

# print("Фильм по заголовку")
# info.get_movie_by_title("Оно")