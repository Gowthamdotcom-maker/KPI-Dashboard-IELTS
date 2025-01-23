import streamlit as st
import pandas as pd
import numpy as np
import requests

# Title and Header
st.title("KPI Dashboard")
st.subheader("Monitor your project's key performance indicators (KPIs)")

# Sidebar for Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Select a Section", ["Overview", "Unit Testing", "Snyk Vulnerabilities", "Other Metrics"])

# Helper Functions
def fetch_sonar_coverage():
    # Example SonarQube API call for test coverage
    # Replace <your-sonarqube-url>, <project-key>, and <auth-token>
    url = "http://<your-sonarqube-url>/api/measures/component"
    params = {
        "component": "<project-key>",
        "metricKeys": "coverage"
    }
    headers = {"Authorization": "Basic <base64-encoded-token>"}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        coverage = data['component']['measures'][0]['value']
        return float(coverage)
    else:
        return None

def fetch_snyk_issues():
    # Example Snyk API call for vulnerabilities
    # Replace <snyk-api-url> and <auth-token>
    url = "https://snyk.io/api/v1/org/<org-id>/project/<project-id>/issues"
    headers = {"Authorization": "token <your-snyk-token>"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        vulnerabilities = len(data.get("issues", []))
        return vulnerabilities
    else:
        return None

# Overview Section
if section == "Overview":
    st.header("Overview")
    st.write("This section provides an overview of the key metrics.")

    # Example KPIs
    st.metric("Unit Test Coverage (%)", "Loading...", delta="Fetching...")
    st.metric("Snyk Vulnerabilities", "Loading...", delta="Fetching...")
    st.metric("Build Time (mins)", "10", delta="-2 mins")

    # Fetch data and update metrics
    if st.button("Refresh Data"):
        # Fetch SonarQube coverage
        coverage = fetch_sonar_coverage()
        if coverage:
            st.metric("Unit Test Coverage (%)", f"{coverage}%", delta=None)
        else:
            st.error("Failed to fetch coverage from SonarQube.")

        # Fetch Snyk vulnerabilities
        vulnerabilities = fetch_snyk_issues()
        if vulnerabilities is not None:
            st.metric("Snyk Vulnerabilities", vulnerabilities, delta=None)
        else:
            st.error("Failed to fetch vulnerabilities from Snyk.")

# Unit Testing Section
elif section == "Unit Testing":
    st.header("Unit Testing Metrics")
    st.write("Visualize unit testing coverage and related metrics.")

    # Example: Static data for unit testing
    data = {
        "Module": ["Auth", "Payment", "User Management", "Reports"],
        "Coverage (%)": [85, 78, 90, 70],
        "Tests Passed": [150, 120, 200, 95],
        "Tests Failed": [5, 10, 3, 8]
    }
    df = pd.DataFrame(data)

    st.table(df)

    # Visualize coverage as a bar chart
    st.bar_chart(df.set_index("Module")["Coverage (%)"])

# Snyk Vulnerabilities Section
elif section == "Snyk Vulnerabilities":
    st.header("Snyk Vulnerabilities")
    st.write("Monitor security vulnerabilities in your project.")

    # Example: Static data for vulnerabilities
    snyk_data = {
        "Severity": ["Critical", "High", "Medium", "Low"],
        "Count": [5, 12, 20, 30]
    }
    snyk_df = pd.DataFrame(snyk_data)

    # Display data as a table
    st.table(snyk_df)

    # Visualize vulnerabilities as a pie chart
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.pie(snyk_df["Count"], labels=snyk_df["Severity"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)

# Other Metrics Section
elif section == "Other Metrics":
    st.header("Other Metrics")
    st.write("Track additional KPIs such as build time, open issues, etc.")

    # Example: Static data for build time
    build_data = {
        "Build Number": [1, 2, 3, 4, 5],
        "Build Time (mins)": [12, 11, 13, 10, 9],
        "Status": ["Success", "Success", "Failed", "Success", "Success"]
    }
    build_df = pd.DataFrame(build_data)

    st.table(build_df)

    # Visualize build times as a line chart
    st.line_chart(build_df.set_index("Build Number")["Build Time (mins)"])
