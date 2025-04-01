import os
import json
import streamlit as st
import datetime
TODOS_FILE_PATH = "todos.json"

def get_todos():
    if os.path.exists(TODOS_FILE_PATH) and os.path.getsize(TODOS_FILE_PATH) > 0:
        with open(TODOS_FILE_PATH, "r") as file:
            todos = json.load(file) 
            return todos
    else:
         return []

def save_todos(todo):
    todos = get_todos()
    with open(TODOS_FILE_PATH, "w") as file:
        todos.append(todo)
        json.dump(todos, file, indent=4)

todo_title = st.sidebar.text_input("Todo title")
todo_des = st.sidebar.text_area("Todo description")


# print(len(todo_title))
if st.sidebar.button("Add todo") and len(todo_title) > 0 and len(todo_des) > 0: 
    now = datetime.datetime.now()
    todo = {
        "title": todo_title,
        "description": todo_des,
        "time": now.strftime("%I:%M %p"),
        "date": now.strftime("%B %d, %Y")
    }
    save_todos(todo)



if st.button("Show todos"):
    todos = get_todos()
    for todo in todos:
        st.write(todo["title"])
        st.write(todo["description"])
        st.write(todo["time"])
        st.write(todo["date"])

