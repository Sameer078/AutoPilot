import pandas as pd
import streamlit as st
from core.metrics import MetricsCollector

metrics = MetricsCollector()

st.title("🛡️ Guardrails Monitor")

violations = metrics.get_guardrail_logs()

if not violations:
    st.success("No guardrail violations detected")

df = pd.DataFrame(violations)
if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s").dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    total_violations = len(df)
    unique_types = df["violation"].nunique()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Violations", total_violations)

    with col2:
        st.metric("Violation Types", unique_types)

    st.divider()
    st.subheader("🚨 Violation Logs")
    st.dataframe(df, width="stretch")