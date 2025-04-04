import streamlit as st

# Initialize session state for todo_title if not already set
if "todo_title" not in st.session_state:
    st.session_state.todo_title = "Default Task"

# Function to update text input field
def update_title(new_title):
    st.session_state.todo_title = new_title
    st.rerun()# Update the value properly

st.title("🔄 Update Text Input Dynamically")

# Text Input linked with session state
task_input = st.text_input("Task Name:", key="todo_title")  

# Button to update input field
# if st.button("Update Task Name"):
#     update_title("Hammad")  # Updating the session state properly

col1 ,buff, col2 =  st.columns([1,0.5,1])
if st.button("click next"):
    if st.session_state.selected_option == "Option 1":
        st.session_state.selected_option = "Option 2"

col1.radio("Select an option:", ("Option 1", "Option 2", "Option 3"), key="selected_option")
st.write(st.session_state)