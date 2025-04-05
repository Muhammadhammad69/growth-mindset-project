import os
import json
import streamlit as st
import datetime
import random
import time

TODOS_FILE_PATH = "todos.json"

# Todos card styling
st.markdown("""
    <style>
        .card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            margin-bottom: 10px;
            
        }
        .card-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .card-desc {
            font-size: 16px;
            color: #555;
            margin-bottom: 10px;
        }
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .btn {
            padding: 5px 10px;
            border: none;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .edit-btn {
            background-color: #ffc107;
        }
        .del-btn {
            background-color: #dc3545;
        }
    </style>
""", unsafe_allow_html=True)
    
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
        st.toast('Todo added successfully', icon="✅")

@st.dialog("Update Todo")
def update_todos(todo_id):    
    update_title = st.text_input("Update todo title")
    update_description = st.text_area("Update Todo Description")
    is_button_clicked = st.button("Submit")
    if is_button_clicked and len(update_title) > 0 or len(update_description) > 0:    
        todos = get_todos()
        now = datetime.datetime.now()
        
        for ind, get_todo in enumerate(todos):
            if get_todo["id"] == todo_id:
                todo_index = ind
                todo = todos[todo_index]
                if len(update_title) > 0:
                    todo["title"] = update_title
                if len(update_description) > 0:
                    todo["description"] = update_description
                todo["date"] = now.strftime("%B %d, %Y")
                todo["creation_time"] = now.strftime("%I:%M %p")
                todos[todo_index] = todo
                
                with open(TODOS_FILE_PATH, "w") as file:
                    json.dump(todos, file, indent=4)
                    st.toast("Todo updated successfully", icon="✅")
                    time.sleep(1)
                st.rerun()
                
    elif is_button_clicked:
        st.warning("Please enter a valid todo title and description")
        
        

# ya per edit todos k function hain to todo ko edit kr raha hain
def edit_todo(index):
    update_todos(index)

def del_todo(id):
    todos = get_todos()
    for index, todo in enumerate(todos):
        if todo["id"] == id:
            todos.remove(todos[index])
            break
    # todos.remove(todos[index - 1])
    with open(TODOS_FILE_PATH, "w") as file:
        json.dump(todos, file, indent=4)
    st.toast("Todo deleted successfully", icon="✅")
    

st.title("My Todo App")
def display_todos():
    todos = get_todos()
    if len(todos) > 0:
        for index, todo in enumerate(todos):
            with st.container(border=True):
                todo_card_html = f"""
                <div class="card">
                    <div class="card-title">{todo['title']}</div>
                    <div class="card-desc">{todo['description']}</div>
                    <div class="card-footer">
                        <span>📅 {todo['date']} | ⏰ {todo['creation_time']}</span>
                    </div>
                </div>
                    """         
                st.markdown(todo_card_html, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1,1],)
                with col1:
                    st.button(f"✏️ Edit" , key=f"edit_{index}" , on_click= edit_todo, args=(todo["id"],))
                with col2:
                    st.button(f"🗑️ Delete", key=f"del_{index}", on_click= del_todo, args=(todo["id"],))

    else:
        st.write("You have no todos yet")


todo_title = st.sidebar.text_input("Todo title", )
todo_des = st.sidebar.text_area("Todo description",)


# print(len(todo_title))
if st.sidebar.button("Add todo") and len(todo_title) > 0 and len(todo_des) > 0: 
    todo_id_gen =0
    todos = get_todos()
    is_id_exist = False
    while not is_id_exist:
        todo_id_gen = random.randint(1000, 100000)
        for todo in todos:
            if todo["id"] == todo_id_gen:
                is_id_exist = True
                
        if is_id_exist:
            is_id_exist = False
        else:
            is_id_exist = True
    now = datetime.datetime.now()
    todo = {
        "id": todo_id_gen,
        "title": todo_title,
        "description": todo_des,
        "creation_time": now.strftime("%I:%M %p"),
        "date": now.strftime("%B %d, %Y")
    }
    save_todos(todo)


display_todos()