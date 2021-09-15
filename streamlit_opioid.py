import streamlit as st

st.title('MME Checker')
st.subheader('Enter the parameters on the left to check if your prescription is in compliance with CDC recommendations for daily MME limits.')

#form = st.form(key='my_form')
st.sidebar.text('Parameters')

with st.sidebar.form(key = "userformat"):
    pill_count = st.number_input(label='How many pills are you prescribing ?',step=1)
    dosage = st.number_input(label='What is the opioid pill dosage in mg ?',step=1)
    min_quantity = st.text_input(label='What is the Min,Max pills per dosage (i.e. 1,2)')
    max_frequency = st.text_input(label="What is the max,min doses per day (Every 2 to 4 hours = 2,4) ?")
    calculate = st.form_submit_button(label = "Calculate MME")


pill_cnt = pill_count

st.write('You are prescribing: ',pill_cnt,"pills.")