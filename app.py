import streamlit as st, pandas as pd, joblib

st.set_page_config(page_title="Credit Default Risk", page_icon="💳")
model = joblib.load("model.joblib")

st.title("💳 Credit Card Default Risk Predictor")
st.caption("Enter a customer's details to estimate the chance of defaulting next month.")

c1, c2 = st.columns(2)
limit = c1.number_input("Credit limit", 10000, 1000000, 100000, step=10000)
age = c2.slider("Age", 21, 79, 35)
sex = c1.selectbox("Gender", ["Male", "Female"])
edu = c2.selectbox("Education", ["Graduate school", "University", "High school", "Other"])
mar = c1.selectbox("Marital status", ["Married", "Single", "Other"])

st.subheader("Repayment status")
st.caption("-1 = paid on time, 0 = revolving credit, 1-8 = months of delay")
p1, p2, p3 = st.columns(3)
pay1 = p1.slider("Last month", -2, 8, 0)
pay2 = p2.slider("2 months ago", -2, 8, 0)
pay3 = p3.slider("3 months ago", -2, 8, 0)

avg_bill = st.number_input("Average monthly bill amount", 0, 1000000, 50000, step=5000)
avg_pay = st.number_input("Average monthly payment amount", 0, 1000000, 5000, step=1000)

if st.button("Predict risk", type="primary"):
    row = pd.DataFrame([{
        "LIMIT_BAL": limit,
        "SEX": 1 if sex == "Male" else 2,
        "EDUCATION": ["Graduate school", "University", "High school", "Other"].index(edu) + 1,
        "MARRIAGE": ["Married", "Single", "Other"].index(mar) + 1,
        "AGE": age, "PAY_0": pay0, "PAY_2": pay2, "PAY_3": pay3,
        "AVG_BILL": avg_bill, "AVG_PAY": avg_pay,
    }])
    prob = float(model.predict_proba(row)[0, 1])
    st.metric("Default probability", f"{prob:.1%}")
    st.progress(min(prob, 1.0))
    if prob >= 0.6:
        st.error("High risk")
    elif prob >= 0.35:
        st.warning("Medium risk")
    else:
        st.success("Low risk")
