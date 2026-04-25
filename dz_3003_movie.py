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
        status = "в прокате" if self.is_active else "нет в прокате"
        return f"<ID {self.id} | {self.title} | {self.genre} | {self.year} | {self.duration} мин.| rating: {self.rating} | {status}>"

class MovieManager:
    def __init__(self):
        self.Session = Session
    def create_movie(self, title, genre, year, duration, rating):
        session = self.Session()
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
            print(f"Ошибка при создании фильма {title} : {e}")
            return None

        finally:
            session.close()

    def get_all_movies(self):
        session = self.Session()
        movies = session.query(Movie).all()
        if movies:
            for m in movies:
                print(m)
        else:
            print("Фильм не найден")

# я добавила метод get_all_movies2 чтобы отработал класс class MovieViewer(). изначально
    # код писался без этого класса и весь блок проверки базируется на том, что метод get_all_movies
    # ничего не возвращает, а только выводит инфо. и теперь мне пришлось бы всё переделывать,
    # а это ооооооооооооооооооооооооочень долго. и так потрачено стопицот часов ....

    def get_all_movies2(self):
        session = self.Session()
        movies = session.query(Movie).all()
        return movies


    def get_by_id(self, id):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == id).first()
        if movie:
            print(f"Найдено в базе: {movie}")
        else:
            print(f"фильма с таким ID нет в базе")

    def get_movies_by_genre(self, genre):
        session = self.Session()
        movies = session.query(Movie).filter(Movie.genre == genre).all()
        if movies:
            for m in movies:
                print(m)

        else:
            print("Нет тако жанра")

    def get_movie_by_title(self, title):
        session = self.Session()
        if not title:
            print("Нет такого фильма")
            return
        movie = session.query(Movie).filter(Movie.title == title).first()
        if movie:
            print(f" Фильм {title} есть в фильмотеке")
        else:
            print(f" Фильм {title} не найден")

    def get_high_rated_movies(self, rating):
        session = self.Session()
        if not (0 <= rating <= 10):
            raise ValueError("Введите рейтинг от 1 до 10")
        else:
            return session.query(Movie).filter(Movie.rating >= rating).all()

    def get_movies_after_year(self, year):
        session = self.Session()
        return session.query(Movie).filter(Movie.year > year).all()

    def update_rating(self, id, new_rating):
        if not (0 <= new_rating <= 10):
            raise ValueError("Введите рейтинг от 1 до 10")
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == id).first()
        if movie:
            movie.rating = new_rating
            session.commit()
            print(f"изменение рейтинга фильма {movie.title}, ID {id} на рейтинг {new_rating}")
            session.close()
        else:
            print("фильма с таким ID не обнаружено")

    def update_genre(self, id, new_genre):
        session = self.Session()
        try:
            movie = session.query(Movie).filter(Movie.id == id).first()
            if movie:
                movie.genre = new_genre
                session.commit()
                print(f"изменение жанра фильма {movie.title}, ID {id} на жанр {new_genre}")
            else:
                print(f"фильма c ID {id} не обнаружено")
        except Exception as e:
            session.rollback()
            print(f"возникла ошибка при обновлении жанра ID {id} : {e}")
        finally:
            session.close()

    def update_available(self, id, is_available):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == id).first()
        if movie:
            movie.is_active = is_available
            session.commit()
            status = "в прокате" if is_available else "нет в прокате"
            print(f"статус фильма '{movie.title}', ID {id} изменен на {status}")
            session.close()
        else:
            print("фильма с таким ID не обнаружено")

    def update_full(self, id, **kwargs):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == id).first()
        if movie:
            for key, value in kwargs.items():
                if hasattr(movie, key):
                    setattr(movie, key, value)
                else:
                    print(f" атрибут {key} не найден ")
            session.commit()
            print(f"обновление фильма '{movie.title}', ID {id} прошло успешно")
            session.close()
        else:
            print("фильма с таким ID не обнаружено")

    def delete_by_id(self, id):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == id).first()
        if movie:
            session.delete(movie)
            session.commit()
            print(f"фильм '{movie.title}', ID {id} успешно удален")
            session.close()
        else:
            print("фильма с таким ID не обнаружено")

    def delete_by_title(self, title):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.title == title).first()
        if movie:
            session.delete(movie)
            session.commit()
            print(f"фильм '{title}' успешно удален")
            session.close()
        else:
            print("фильма с таким названием не обнаружено")

    def soft_delete(self, id):
        session = self.Session()
        movie = session.query(Movie).filter(Movie.id == id).first()
        if movie:
            movie.is_active = False
            session.commit()
            print(f"фильм '{movie.title}', ID {id} переведен в статус 'нет в прокате'")
            session.close()
        else:
            print("фильма с таким ID не обнаружено")
class MovieViewer():
    def print_headers(self, text):
        print(f"\n{'=' * 100}")
        print(text)
        print(f"{'=' * 100}")
    def print_one(self, movie):
        if movie:
            print(movie)
        else:
            print("фильм не обнаружен")
    def print_all(self, movies):
        if not movies:
            print("фильмы не обнаружены")
            return
        for movie in movies:
            print(movie)
    def print_statistics(self, movies):
        if not movies:
            print("статистика не найдена")
            return
        total_movies = len(movies)
        avai_mov = sum(1 for movie in movies if movie.is_active)
        unavai_mov = total_movies - avai_mov
        years = [movie.year for movie in movies if movie.year]
        min_year = min(years)
        max_year = max(years)
        print(f"\n --- Статистика фильмов --- ")
        print(f" Всего фильмов: {total_movies}")
        print(f"В прокате {avai_mov}")
        print(f"Недоступны {unavai_mov}")
        print(f"Годы выпуска от {min_year} до {max_year} ")
        print(f" ---------------------- ")



if __name__ == "__main__":
    Base.metadata.create_all(engine)


    info = MovieManager()
    vie = MovieViewer()

    # vie.print_headers("Добавляем фильмы")
    # info.create_movie("Эквилибриум", "Драмма", 2002, 106,7.6)
    # info.create_movie("Аладдин", "Мюзикл", 2019, 127,6.9)
    # info.create_movie("Мортал комбат", "Фентези", 2021, 110,6.1)
    # info.create_movie("Оно", "Ужасы", 2017, 134,7.3)
    # info.create_movie("Гнев", "Боевик", 2021, 118,7.2)
    # info.create_movie("Один дома", "Комедия", 1990, 102,7.6)

    # vie.print_headers("---Все фильмы---")
    # info.get_all_movies()

    # я добавила метод get_all_movies2 чтобы отработал класс class MovieViewer(). изначально
    # код писался без этого класса и весь блок проверки базируется на том, что метод get_all_movies
    # ничего не возвращает, а только выводит инфо. и теперь мне пришлось бы всё переделывать,
    # а это ооооооооооооооооооооооооочень долго. и так потрачено стопицот часов ...
    # ниже блок проверки статистики и запрос всех фильмов из класса MovieViewer. всё работает, но больше
    # нигде методы из него не фигурируют, за исключением print_headers. надеюсь, это не повлияет
    # на правильность выполнения задания, так как всё работает

    vie.print_headers("---Все фильмы---")
    all_movies = info.get_all_movies2()
    vie.print_all(all_movies)
    vie.print_statistics(all_movies)


    # vie.print_headers("---фильм по ID---")
    # info.get_by_id(11)

    # vie.print_headers("---Все фильмы по жанру---")
    # info.get_movies_by_genre("Ужасы")

    # vie.print_headers("---Фильм по заголовку---")
    # info.get_movie_by_title("Оно")

    # vie.print_headers("---Все фильмы выше заданного рейтинга---")
    # rate = info.get_high_rated_movies(7.1)
    # print(rate)

    # vie.print_headers("---Все фильмы от 2016 года---")
    # y= info.get_movies_after_year(2016)
    # print(y)

    # vie.print_headers("---Обновление рейтинга---")
    # update_r = info.update_rating(2, 9.1)
    # print(update_r)
    # info.get_by_id(2)

    # vie.print_headers("---Обновление жанра---")
    # update_g = info.update_genre(3, "фантастика")
    # print(update_g)
    # info.get_by_id(3)

    # vie.print_headers("---Обновление доступности---")
    # update_a = info.update_available(4, 0)
    # print(update_a)
    # info.get_by_id(4)

    # vie.print_headers("Добавляем еще фильмов, а то не хватило")
    # info.create_movie("Интерстеллар", "фантастика",2014, 169, 8.2)
    # info.create_movie("Джентельмены", "криминал",2019, 142, 8.1)
    # info.create_movie("1+1", "драма",2011, 118, 8 )
    # info.create_movie("Гладиатор", "история",2000, 178, 7.7)

    # vie.print_headers("---Обнови меня полностью или по частям---")
    # update_all = info.update_full(10, year=2001, duration = 180, is_active = 0)
    # print(update_all)
    # info.get_by_id(10)

    # vie.print_headers("---Удалить фильм по ID ---")
    # del_byid = info.delete_by_id(9)
    # print(del_byid)
    # info.get_by_id(9)

    # vie.print_headers("---Удалить фильм по названию---")
    # del_bytit = info.delete_by_title("Гнев")
    # print(del_bytit)
    # info.get_by_id(5)

    # vie.print_headers("---Изменение статуса фильма---")
    # stat = info.soft_delete(7)
    # print(stat)
    # info.get_by_id(7)
