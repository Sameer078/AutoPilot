import pandas as pd
import plotly.express as px
import streamlit as st
from core.metrics import MetricsCollector

metrics = MetricsCollector()

st.title("📊 Analytics Dashboard")

requests_data = metrics.get_recent_requests()

if not requests_data:
    st.info("No request data available")

df = pd.DataFrame(requests_data)
required_columns = [
    "actual_model",
    "latency_ms",
    "cost_usd",
    "selected_tier",
    "timestamp",
]
for col in required_columns:
    if col not in df.columns:
        df[col] = None

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s").dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

total_requests = len(df)
avg_latency = round(df["latency_ms"].mean(), 2)
total_cost = round(df["cost_usd"].sum(), 4)
fallback_count = len(df[df["selected_tier"] != df["actual_model"]])
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Requests", total_requests)

with col2:
    st.metric("Avg Latency", f"{avg_latency} ms")

with col3:
    st.metric("Total Cost", f"${total_cost}")

with col4:
    st.metric("Fallback Count", fallback_count)

st.divider()

st.subheader("🤖 Model Usage")
model_counts = df["actual_model"].value_counts().reset_index()
model_counts.columns = ["model", "count"]
fig = px.pie(
    model_counts, names="model", values="count", title="Model Usage Distribution"
)

st.plotly_chart(fig, width="stretch")
st.subheader("⚡ Latency Trend")
latency_fig = px.line(df, x="timestamp", y="latency_ms", title="Latency Over Time")
st.plotly_chart(latency_fig, width="stretch")
st.subheader("📝 Request History")
st.dataframe(df, width="stretch")