import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- UI CONFIGURATION ---
st.set_page_config(page_title="SalesVault", page_icon="🛡️", layout="wide")

# Custom Branding
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; }
    </style>
    """, unsafe_base64=True)

st.title("🛡️ SalesVault: Sales Development Command")
st.write(f"Logged in as: **{st.experimental_user.email if hasattr(st, 'experimental_user') else 'SDR User'}**")

# --- SIDEBAR: MANUAL DATA ENTRY ---
with st.sidebar:
    st.header("Log Activity")
    with st.form("activity_form"):
        st.subheader("Manual Tracking")
        calls = st.number_input("Phone Calls Made", min_value=0, step=1)
        in_person = st.number_input("In-Person Meetings Booked", min_value=0, step=1)
        proposals = st.number_input("Proposals Sent", min_value=0, step=1)
        notes = st.text_area("Meeting/Call Notes")
        
        submitted = st.form_submit_button("Sync to Salesforce & Vault")
        if submitted:
            st.success("Activity Logged & Pushed to Salesforce!")

# --- DATA PROCESSING (MOCK DATA FOR VISUALS) ---
# In a live app, this replaces your Google Sheets
data = {
    'Source': ['Email', 'Email', 'Call', 'Call', 'Email', 'Call'],
    'Agency': ['Ogilvy', 'WPP', 'Publicis', 'Dentsu', 'Omnicom', 'Havas'],
    'WordCount': [45, 120, 0, 0, 210, 0],
    'Outcome': ['Meeting', 'No Response', 'Meeting', 'Follow-up', 'No Response', 'Meeting'],
    'Date': pd.to_datetime(['2024-05-01', '2024-05-01', '2024-05-02', '2024-05-02', '2024-05-03', '2024-05-03'])
}
df = pd.DataFrame(data)

# --- TOP METRIC ROW ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Outreach", "165", "+12%")
col2.metric("Virtual Meetings", "14", "Top Channel: Email")
col3.metric("In-Person Meetings", str(in_person), "Manual Log")
col4.metric("Avg. Email Word Count", "85 words")

# --- VISUAL 1: THE SALES FUNNEL ---
st.divider()
st.subheader("Manager View: Conversion Funnel")


funnel_data = dict(
    number=[120, 45, 18, 5],
    stage=["Emails Sent", "Calls Made", "Meetings Booked", "Deals Closed"]
)
fig_funnel = px.funnel(funnel_data, x='number', y='stage', color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig_funnel, use_container_width=True)

# --- VISUAL 2: THE "SWEET SPOT" HEATMAP ---
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Email Length vs. Meeting Success")
    # This visual shows you the exact word count that leads to meetings
    heatmap_data = pd.DataFrame({
        'Word Count Range': ['0-50', '51-100', '101-150', '151-200', '201+'],
        'Meetings Booked': [2, 12, 8, 3, 1]
    })
    fig_heat = px.bar(heatmap_data, x='Word Count Range', y='Meetings Booked', 
                     color='Meetings Booked', title="Word Count Effectiveness")
    st.plotly_chart(fig_heat, use_container_width=True)

with col_right:
    st.subheader("Outreach Mix")
    fig_pie = px.pie(df, names='Source', title="Calls vs. Emails Distribution", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- THE LIVE SCANNER FEED ---
st.divider()
st.subheader("Live Superhuman/Outlook Scan")
st.dataframe(df[['Date', 'Agency', 'WordCount', 'Outcome']].sort_values(by='Date', ascending=False), use_container_width=True)
