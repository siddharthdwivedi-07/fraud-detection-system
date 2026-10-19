import joblib
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Fraud Detection | Sentinel",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #172338;
        --muted: #64748b;
        --line: #e7edf4;
        --teal: #087f8c;
        --teal-soft: #e7f5f5;
    }
    .stApp {
        background: #f5f8fc;
        color: var(--ink);
        font-family: Arial, sans-serif;
    }
    h1, h2, h3 {
        font-family: Arial, sans-serif !important;
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #14243a;
    }
    [data-testid="stSidebar"] * { color: #e8f0f8; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #b8c7d9;
    }
    .eyebrow {
        color: var(--teal);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .hero-copy {
        color: var(--muted);
        font-size: 1.05rem;
        margin-top: -0.45rem;
    }
    .surface {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 8px 28px rgba(28, 48, 76, 0.045);
        margin-bottom: 1rem;
    }
    .section-label {
        color: var(--ink);
        font-family: Arial, sans-serif;
        font-size: 1.08rem;
        font-weight: 600;
        margin: 0 0 0.1rem;
    }
    .section-hint {
        color: var(--muted);
        font-size: 0.88rem;
        margin: 0 0 1rem;
    }
    .status-pill {
        display: inline-block;
        border-radius: 999px;
        background: var(--teal-soft);
        color: var(--teal);
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.42rem 0.72rem;
    }
    div.stButton > button, div.stFormSubmitButton > button {
        background: #087f8c;
        border: 0;
        border-radius: 10px;
        color: white;
        font-weight: 700;
        min-height: 3rem;
        transition: background 160ms ease, transform 160ms ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: #066b76;
        color: white;
        transform: translateY(-1px);
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1rem 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

model = joblib.load("fraud_detection_model.pkl")

with st.sidebar:
    st.markdown("## 🛡️ Sentinel")
    st.markdown("### Transaction intelligence")
    st.markdown("Run a transaction through the fraud detection model and review its risk assessment.")
    st.divider()
    st.markdown("**Supported transaction types**")
    st.markdown("Payment · Transfer · Cash out · Debit · Cash in")
    st.divider()
    st.caption("Model results are decision support, not a substitute for manual review.")

st.markdown('<p class="eyebrow">Fraud monitoring · Transaction review</p>', unsafe_allow_html=True)
st.title("Transaction risk check")
st.markdown(
    '<p class="hero-copy">Enter the transaction and account balances to assess its fraud risk.</p>',
    unsafe_allow_html=True,
)

form_col, help_col = st.columns([1.65, 0.85], gap="large")

with form_col:
    st.markdown(
        """
        <div class="surface">
            <p class="section-label">Transaction details</p>
            <p class="section-hint">All balances and amounts must be zero or greater.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("transaction_form"):
        transaction_type = st.selectbox(
            "Transaction type",
            ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"],
            help="Choose the transaction category to assess.",
        )
        amount = st.number_input(
            "Transaction amount",
            min_value=0.0,
            value=1000.0,
            step=100.0,
            format="%.2f",
        )
        sender_col, receiver_col = st.columns(2, gap="large")
        with sender_col:
            st.markdown("**Sender account**")
            oldbalance_org = st.number_input(
                "Balance before",
                min_value=0.0,
                value=1000.0,
                step=100.0,
                format="%.2f",
                key="sender_before",
            )
            newbalance_orig = st.number_input(
                "Balance after",
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f",
                key="sender_after",
            )
        with receiver_col:
            st.markdown("**Receiver account**")
            oldbalance_dest = st.number_input(
                "Balance before",
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f",
                key="receiver_before",
            )
            newbalance_dest = st.number_input(
                "Balance after",
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f",
                key="receiver_after",
            )
        submitted = st.form_submit_button("Analyze transaction", width="stretch")

with help_col:
    st.markdown(
        """
        <div class="surface">
            <p class="section-label">What gets evaluated?</p>
            <p class="section-hint">The model uses the transaction category, amount, and both account balance snapshots.</p>
            <span class="status-pill">Secure · Model-assisted review</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Why are balance snapshots important?", expanded=True):
        st.write(
            "Comparing balances before and after a transaction helps the model spot patterns "
            "associated with suspicious transfers or cash-outs."
        )
    with st.expander("How should I read the result?"):
        st.write(
            "A flagged result indicates the model predicts possible fraud. Review the transaction "
            "in context before taking action."
        )
    sender_change = oldbalance_org - newbalance_orig
    receiver_change = newbalance_dest - oldbalance_dest
    st.metric("Sender balance change", f"${sender_change:,.2f}")
    st.metric("Receiver balance change", f"${receiver_change:,.2f}")

if submitted:
    input_data = pd.DataFrame(
        {
            "type": [transaction_type],
            "amount": [amount],
            "oldbalanceOrg": [oldbalance_org],
            "newbalanceOrig": [newbalance_orig],
            "oldbalanceDest": [oldbalance_dest],
            "newbalanceDest": [newbalance_dest],
        }
    )

    prediction = int(model.predict(input_data)[0])
    fraud_probability = None
    if hasattr(model, "predict_proba"):
        classes = list(model.classes_)
        if 1 in classes:
            fraud_probability = float(model.predict_proba(input_data)[0][classes.index(1)])

    st.divider()
    st.markdown('<p class="eyebrow">Assessment complete</p>', unsafe_allow_html=True)
    if prediction == 1:
        st.error("Potential fraud detected — review this transaction.")
    else:
        st.success("No fraud detected — the model considers this transaction likely legitimate.")

    result_cols = st.columns(3)
    with result_cols[0]:
        st.metric("Model decision", "Potential fraud" if prediction == 1 else "Likely legitimate")
    with result_cols[1]:
        st.metric("Transaction type", transaction_type.replace("_", " ").title())
    with result_cols[2]:
        st.metric("Amount reviewed", f"${amount:,.2f}")

    if fraud_probability is not None:
        st.markdown("**Estimated fraud score**")
        st.progress(fraud_probability, text=f"{fraud_probability:.1%} estimated fraud probability")
        st.caption("This is the model's estimated probability, not a guarantee or a confidence rating.")

    with st.expander("Review submitted transaction data"):
        st.dataframe(input_data, width="stretch", hide_index=True)
