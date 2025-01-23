import streamlit as st
import pandas as pd
import numpy as np

# Title
st.title("Interactive Dashboard")

# Sidebar
st.sidebar.title("Sidebar")
num_points = st.sidebar.slider("Number of Points", 10, 100, 50)

# Generate random data
data = pd.DataFrame({
    "X": np.random.randn(num_points),
    "Y": np.random.randn(num_points)
})

# Scatter Plot
st.subheader("Scatter Plot")
st.write("A scatter plot of randomly generated data.")
st.scatter_chart(data)

# Display Table
if st.checkbox("Show data table"):
    st.subheader("Data Table")
    st.write(data)

# User Input
name = st.text_input("Enter your name", "")
if name:
    st.write(f"Hello, {name}!")
