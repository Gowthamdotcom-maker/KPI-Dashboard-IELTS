import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set your SonarQube details
SONARQUBE_URL = "http://<your-sonarqube-url>"  # Replace with your SonarQube URL
PROJECT_KEY = "31784208:ielts:python"
AUTH_TOKEN = "squ_33befd7029c81abeb888031cb46113c0df8b2872"

# Function to fetch metrics from SonarQube
def fetch_sonar_metrics(metric_keys):
    url = f"{SONARQUBE_URL}/api/measures/component"
    params = {
        "component": PROJECT_KEY,
        "metricKeys": metric_keys
    }
    auth = (AUTH_TOKEN, "")  # Basic Auth: Token as username, password blank
    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        measures = data.get("component", {}).get("measures", [])
        return {m["metric"]: m["value"] for m in measures}
    else:
        st.error(f"Failed to fetch data from SonarQube (Status: {response.status_code})")
        return {}

# Title and Sidebar
st.title("KPI Dashboard - SonarQube Metrics")
st.sidebar.title("Navigation")
section = st.sidebar.radio("Select a Section", ["Overview", "Detailed Metrics"])

# Overview Section
if section == "Overview":
    st.header("Overview")
    st.write("Key metrics from SonarQube for the project.")

    # Fetch data
    metrics = fetch_sonar_metrics("coverage,code_smells,bugs,vulnerabilities")
    
    # Display KPIs
    st.metric("Test Coverage (%)", metrics.get("coverage", "N/A"))
    st.metric("Code Smells", metrics.get("code_smells", "N/A"))
    st.metric("Bugs", metrics.get("bugs", "N/A"))
    st.metric("Vulnerabilities", metrics.get("vulnerabilities", "N/A"))

# Detailed Metrics Section
elif section == "Detailed Metrics":
    st.header("Detailed Metrics")
    st.write("Detailed breakdown of SonarQube metrics.")

    # Fetch data
    metrics = fetch_sonar_metrics("coverage,code_smells,bugs,vulnerabilities")
    df = pd.DataFrame([
        {"Metric": "Coverage (%)", "Value": metrics.get("coverage", "N/A")},
        {"Metric": "Code Smells", "Value": metrics.get("code_smells", "N/A")},
        {"Metric": "Bugs", "Value": metrics.get("bugs", "N/A")},
        {"Metric": "Vulnerabilities", "Value": metrics.get("vulnerabilities", "N/A")},
    ])

    # Display table
    st.table(df)

    # Pie chart for Code Smells, Bugs, and Vulnerabilities
    if "code_smells" in metrics and "bugs" in metrics and "vulnerabilities" in metrics:
        labels = ["Code Smells", "Bugs", "Vulnerabilities"]
        values = [
            int(metrics["code_smells"]),
            int(metrics["bugs"]),
            int(metrics["vulnerabilities"])
        ]
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
        st.pyplot(fig)
