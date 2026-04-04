from abc import ABC, abstractmethod
import logging
from typing import List
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class Book:
    def __init__(self, title: str, author: str, year: str) -> None:
        self.title = title
        self.author = author
        self.year = year

    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"

class IBookCommand(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        pass

class IBookQuery(ABC):
    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass

class Library(IBookCommand, IBookQuery):
    def __init__(self) -> None:
        self._books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)
        logger.info(f"Book added: {book.title}")

    def remove_book(self, title: str) -> None:
        for book in self._books:
            if book.title == title:
                self._books.remove(book)
                logger.info(f"Book removed: {title}")
                break
        else:
            logger.warning(f"Book '{title}' not found.")

    def get_all_books(self) -> List[Book]:
        return self._books
    
class FileLibrary(Library):
    """
    store library in JSON file
    """
    def __init__(self, filename: str = "library_data.json") -> None:
        super().__init__()
        self.filename = filename
        self._load_from_file()

    def _save_to_file(self) -> None:
        try:
            data = [
                {"title": b.title, "author": b.author, "year": b.year} 
                for b in self._books
            ]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Дані записано у файл {self.filename}")
        except Exception as e:
            logger.error(f"Помилка запису: {e}")

    def _load_from_file(self) -> None:
        """load data from file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._books = [Book(**item) for item in data]
            logger.info(f"Завантажено {len(self._books)} книг з файлу.")
        except FileNotFoundError:
            logger.info("Файл даних не знайдено, створено нову базу.")
        except Exception as e:
            logger.error(f"Помилка читання: {e}")

    def add_book(self, book: Book) -> None:
        super().add_book(book)
        self._save_to_file()

    def remove_book(self, title: str) -> None:
        super().remove_book(title)
        self._save_to_file()

class LoggingLibrary(Library):
    def add_book(self, book: Book) -> None:
        logger.info("Спроба додати книгу")
        super().add_book(book)

class LibraryManager:
    def __init__(self, command_channel: IBookCommand, query_channel: IBookQuery) -> None:
        self.commands = command_channel
        self.queries = query_channel

    def add_book(self, title: str, author: str, year: str) -> None:
        self.commands.add_book(Book(title, author, year))

    def remove_book(self, title: str) -> None:
        self.commands.remove_book(title)

    def show_books(self) -> None:
        books = self.queries.get_all_books()
        if not books:
            logger.info("Library is empty.")
            return
        
        logger.info("--- Current Collection ---")
        for book in books:
            logger.info(str(book))

def main() -> None:
    #storage = LoggingLibrary() 
    storage = FileLibrary("my_library.json")
    
    manager = LibraryManager(storage, storage)

    while True:
        try:
            cmd = input("Enter command (add, remove, show, exit): ").strip().lower()

            match cmd:
                case "add":
                    title: str = input("Enter book title: ").strip()
                    author: str = input("Enter book author: ").strip()
                    year: str = input("Enter book year: ").strip()
                    manager.add_book(title, author, year)
                case "remove":
                    manager.remove_book(input("Title to remove: "))
                case "show":
                    manager.show_books()
                case "exit":
                    logger.info("Goodbye!")
                    break
                case _:
                    logger.warning("Invalid command. Please try again.")
        except EOFError:
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()