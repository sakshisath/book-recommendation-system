import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_with_prefix(node, prefix)

    def _find_words_with_prefix(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._find_words_with_prefix(child_node, prefix + char))
        return words

trie = Trie()
books = []  
user_ratings = {} 

def display_menu():
    print("Options:")
    print("1. Add Book")
    print("2. View Books")
    print("3. Rate Book")
    print("4. Get Recommendations")
    print("5. Search Books")
    print("6. Exit")

def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    genre = input("Enter book genre: ")
    if not title or not author or not genre:
        print("All fields are required.")
        return
    book = {"title": title, "author": author, "genre": genre}
    books.append(book)
    trie.insert(title)
    print("Book added successfully:)")

def view_books():
    if not books:
        print("No books are available in your library")
        return
    for i, book in enumerate(books):
        print(f"{i+1}. {book['title']}, {book['author']}, {book['genre']}")

def rate_book():
    username = input("Enter your username: ")
    if not books:
        print("No books are available to rate")
        return
    view_books()
    try:
        book_index = int(input("Enter the number of the book you want to rate: ")) - 1
        if book_index < 0 or book_index >= len(books):
            print("Invalid book number:(")
            return
        rating = int(input(f"Enter your rating for {books[book_index]['title']} (1-5): "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5")
            return
        if username not in user_ratings:
            user_ratings[username] = {}
        user_ratings[username][books[book_index]['title']] = rating
        print("Rating submitted successfully!")
    except ValueError:
        print("Invalid input. Please enter a number.")

def get_recommendations():
    username = input("Enter your username: ")
    if username not in user_ratings:
        print("No ratings found for user:(")
        return

    user_books = user_ratings[username]
    favorite_genre = get_favorite_genre(user_books)
    recommended_books = [book for book in books if book['genre'] == favorite_genre and book['title'] not in user_books]
    if not recommended_books:
        print("No recommendations available:( Please rate more books to gather recommendations!")
        return
    print("Recommendations:")
    for book in recommended_books:
        print(f"- Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")

def get_favorite_genre(user_books):
    genre_count = {}
    for title, rating in user_books.items():
        for book in books:
            if book['title'] == title:
                genre = book['genre']
                if genre not in genre_count:
                    genre_count[genre] = 0
                genre_count[genre] += rating
    favorite_genre = max(genre_count, key=genre_count.get)
    return favorite_genre

def search_books():
    prefix = input("Enter book title: ")
    search_results = trie.search(prefix)
    if not search_results:
        print("No books found with this title")
    else:
        print("Books found in your library:")
        for title in search_results:
            book = next(book for book in books if book['title'] == title)
            print(f"Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")

def load_data():
    global books, user_ratings
    try:
        with open('books.json', 'r') as file:
            data = json.load(file)
            books = data['books']
            user_ratings = data['ratings']
        for book in books:
            trie.insert(book['title'])
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Starting with empty data.")
    except json.JSONDecodeError:
        print("Error decoding data file. Starting with empty data.")

def save_data():
    data = {
        "books": books,
        "ratings": user_ratings
    }
    with open('books.json', 'w') as file:
        json.dump(data, file)
    print("Data saved successfully.")

def main():
    load_data()
    print("Welcome to Your Library!")
    while True:
        display_menu()
        choice = input("Choose what you would like to do in your library: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            rate_book()
        elif choice == '4':
            get_recommendations()
        elif choice == '5':
            search_books()
        elif choice == '6':
            save_data()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()