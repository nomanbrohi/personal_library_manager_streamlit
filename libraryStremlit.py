import streamlit as st
import json
import os

# 📂 Load Library Data
def load_library(filename="library.json"):
    return json.load(open(filename)) if os.path.exists(filename) else []

# 💾 Save Library Data
def save_library(library, filename="library.json"):
    with open(filename, "w") as file:
        json.dump(library, file, indent=4)

# ➕ Add a New Book
def add_book():
    st.subheader("➕ Add a New Book")

    with st.form("add_book_form"):
        title = st.text_input("📖 Title").strip()
        author = st.text_input("✍🏾 Author").strip()
        genre = st.text_input("📚 Genre").strip()
        publication = st.number_input("📅 Publication", step=1, min_value=1100, max_value=2025, format="%d")
        read = st.checkbox("Have you read this book? ✅/❌")
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if not title or not author:
                st.error("⚠️ Please enter both Title and Author!")
                return

            new_book = {"title": title, "author": author, "genre": genre, "publication": publication, "read": read}
            st.session_state.library.append(new_book)
            save_library(st.session_state.library)
            st.success("📚 Book added successfully!")
            st.rerun()

# ❌ Remove a Book
def remove_book():
    st.subheader("➖ Remove Book")

    if not st.session_state.library:
        st.warning("📭 Your library is empty!")
        return

    book_titles = [book["title"] for book in st.session_state.library]
    selected_title = st.selectbox("Select a book to remove:", book_titles)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑 Remove Book"):
            st.session_state.library = [book for book in st.session_state.library if book["title"] != selected_title]
            save_library(st.session_state.library)
            st.success(f"'{selected_title}' has been removed!")
            st.rerun()
    
    with col2:
        if st.button("🗑 Remove All Books", type="primary"):
            st.session_state.library.clear()
            save_library(st.session_state.library)
            st.success("All books have been removed!")
            st.rerun()

# 🔎 Search a Book
def search_book():
    st.subheader("🔎 Search Book")

    if not st.session_state.library:
        st.warning("No Books available in library")
        return
    
    book_titles = [book["title"] for book in st.session_state.library]
    searched_term = st.selectbox("Enter or Select Book Title: ", book_titles).strip().lower()

    if st.button("Search"):
        if not searched_term:
            st.warning("⚠️ Please enter a book title to search!")
            return

        found_books = [book for book in st.session_state.library if searched_term in book["title"].lower()]
        if found_books:
            st.success(f"📚 Found {len(found_books)} matching book(s):")
            for book in found_books:
                st.markdown(f"""
                **📖 Title:** {book['title']}  
                **✍🏾 Author:** {book['author']}  
                **📚 Genre:** {book['genre']}  
                **📅 Publication:** {book['publication']}  
                """)
        else:
            st.error("❌ No matching book found!")

# 📚 Display All Books
def display_all_books():
    st.subheader("💼 Library")

    if not st.session_state.library:
        st.warning("📭 No books available in your library!")
        return

    for book in st.session_state.library:
        read_status = "✅ Read" if book["read"] else "❌ Not Read"
        st.subheader(f"**{book['title']}**")  
        st.markdown(f"""
        **✍🏾 Author:** {book['author']}  
        **📚 Genre:** {book['genre']}  
        **📅 Publication:** {book['publication']}  
        **Status:** {read_status}  
        """)
        st.markdown("---")  # Horizontal line for separation

# 📊 Library Statistics
def display_stats():
    st.subheader("📊 Statistics")

    total_books = len(st.session_state.library)
    total_read = sum(book["read"] for book in st.session_state.library)

    st.markdown(f"📚 **Total Books:** {total_books}")

    if total_books > 0:
        read_percentage = (total_read / total_books) * 100
        st.markdown(f"📖 **Read Percentage:** {read_percentage:.1f}% ✅")
    else:
        st.warning("📭 No books available to calculate statistics!")

# 📌 Main Menu
def menu():
    st.title("📚 Welcome to Your Personal Library")

    if "library" not in st.session_state:
        st.session_state.library = load_library()

    menu_options = ["📖 Add a Book", "❌ Remove Book", "🔎 Search Book", "📚 Display All Books", "📊 Statistics"]
    choice = st.sidebar.radio("📌 Menu", menu_options)

    if choice == "📖 Add a Book":
        add_book()
    elif choice == "❌ Remove Book":
        remove_book()
    elif choice == "🔎 Search Book":
        search_book()
    elif choice == "📚 Display All Books":
        display_all_books()
    else:
        display_stats()

if __name__ == "__main__":
    menu()
