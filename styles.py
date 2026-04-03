import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    .stApp{ 
    background-color: #f8f9fa; 
    }

    .main-container{ 
    border: 1px solid #dee2e6; 
    padding:20px ; 
    border-radius:10px; 
    background-color: white;
    min-height:400px
    }
    .timestamp { 
    color: #6c757d; 
    font-weight:bold; 
    margin-right: 10px; 
    }
    .translation{ 
    color: #28a745; 
    margin-left:10px; 
    border-left :10px;
    }
    </style>
    """,unsafe_allow_html=True)