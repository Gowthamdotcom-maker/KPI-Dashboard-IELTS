import base64
import requests
import streamlit as st

# SonarQube details
SONARQUBE_URL = "http://sonarqube.idp.com"  # Replace with your SonarQube URL
PROJECT_KEY = "31784208:ielts:python"  # Your project key
AUTH_TOKEN = "squ_33befd7029c81abeb888031cb46113c0df8b2872"  # Your SonarQube token

# Function to fetch metrics from SonarQube
def fetch_sonar_metrics(metric_keys):
    url = f"{SONARQUBE_URL}/api/measures/component"
    params = {
        "component": PROJECT_KEY,
        "metricKeys": coverage
    }

    # Manually construct the Authorization header
    auth_string = f"{AUTH_TOKEN}:"  # Token as username, password is blank
    encoded_auth = base64.b64encode(auth_string.encode()).decode()  # Base64 encode
    headers = {
        "Authorization": f"Basic {encoded_auth}"  # Add the Basic Auth header
    }

    # Debug: Print the Authorization header
    st.write(f"Authorization Header: {headers['Authorization']}")

    try:
        # Make the request
        response = requests.get(url, params=params, headers=headers)

        # Debug: Print response details
        st.write(f"Response Status Code: {response.status_code}")
        st.write(f"Response Text: {response.text}")

        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        data = response.json()
        measures = data.get("component", {}).get("measures", [])
        return {m["metric"]: m["value"] for m in measures}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching metrics: {e}")
        return {}

# Streamlit App
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
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Test Coverage (%)", metrics.get("coverage", "N/A"))
    col2.metric("Code Smells", metrics.get("code_smells", "N/A"))
    col3.metric("Bugs", metrics.get("bugs", "N/A"))
    col4.metric("Vulnerabilities", metrics.get("vulnerabilities", "N/A"))

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
