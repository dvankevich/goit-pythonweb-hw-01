from abc import ABC, abstractmethod
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class Book:
    def __init__(self, title: str, author: str, year: str) -> None:
        self.title: str = title
        self.author: str = author
        self.year: str = year

    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"

class LibraryInterface(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        pass

    @abstractmethod
    def show_books(self) -> None:
        pass

class Library(LibraryInterface):
    def __init__(self) -> None:
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        logger.info(f"Book added: {book.title}")

    def remove_book(self, title: str) -> None:
        for book in self.books:
            if book["title"] == title:
                self.books.remove(book)
                break

    def show_books(self) -> None:
        if not self.books:
            logger.info("Library is empty.")
            return
        
        logger.info("--- Library Collection ---")
        for book in self.books:
            logger.info(str(book))

class LibraryManager:
    def __init__(self, library: LibraryInterface) -> None:
        self.library: LibraryInterface = library

    def add_book(self, title: str, author: str, year: str) -> None:
        new_book = Book(title, author, year)
        self.library.add_book(new_book)

    def remove_book(self, title: str) -> None:
        self.library.remove_book(title)

    def show_books(self) -> None:
        self.library.show_books()

def main() -> None:
    library: LibraryInterface = Library()
    manager: LibraryManager = LibraryManager(library)

    while True:
        try:
            command: str = input("Enter command (add, remove, show, exit): ").strip().lower()

            match command:
                case "add":
                    title: str = input("Enter book title: ").strip()
                    author: str = input("Enter book author: ").strip()
                    year: str = input("Enter book year: ").strip()
                    manager.add_book(title, author, year)
                case "remove":
                    title: str = input("Enter book title to remove: ").strip()
                    manager.remove_book(title)
                case "show":
                    manager.show_books()
                case "exit":
                    logger.info("Exiting the program. Goodbye!")
                    break
                case _:
                    logger.warning("Invalid command. Please try again.")
        except EOFError:
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()