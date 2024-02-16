import streamlit as st

# Set page title and background color
st.markdown(
    """
    <style>
    body {
        background-color: #FFFFE0; /* light yellow */
        color: #000000;
    }
    .title {
        color: #FF5733;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #1E90FF; /* blue */
    }
    .stTextInput>div>div>div>input {
        border: 2px solid #FFD700; /* gold */
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add title with custom color and center alignment
st.title("My ChatBot")

# Add Ask Question text input
#ask_question = st.text_input("Ask Question")

# Add toggle button and position it left side center
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        display: flex;
        align-items: center;
        justify-content: flex-start;
    
    }
    </style>
    """,
    unsafe_allow_html=True
)
talk_to_data = st.sidebar.checkbox("Talk to my data", False, key='toggle')

# If toggle button is True, show file upload button
if talk_to_data:
    st.write("Upload your files for personalise Q and A")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

    # Display uploaded files
    if uploaded_files:
        for file in uploaded_files:
            file_details = {"filename": file.name, "filetype": file.type, "filesize": file.size}
            st.write(file_details)



# Add Ask Question text input
#ask_question = st.text_input("Ask Question") 


# Add CSS styling for the text input container
st.markdown(
    """
    <style>
    .text-input-container {
        display: inline-block; /* Ensure container and input field are inline */
        width: 100%; /* Allow container to expand to fit input field */
        border: 2px solid #000000; /* Black border */
        border-radius: 5px; /* Rounded border */
        padding: 5px; /* Add some padding */
        margin-bottom: 40px; /* Add margin at the bottom */
    }
    .text-input-container input {
        width: 100%; /* Ensure input field takes up entire width of container */
        border: #0000FF; /* Remove default input field border */
        outline: none; /* Remove default input field focus outline */
        padding: 0; /* Remove default input field padding */
        margin: 0; /* Remove default input field margin */
        background-color: transparent; /* Set input field background to transparent */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="text-input-container"><input type="text" placeholder="Ask Question"></div>', unsafe_allow_html=True)

# Add submit button
st.button("Submit")
