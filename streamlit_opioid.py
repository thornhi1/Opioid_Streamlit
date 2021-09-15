import streamlit as st
import pandas as pd

st.title('MME Checker')
st.subheader('Enter the parameters on the left to check if your prescription is in compliance with CDC recommendations for daily MME limits.')

#form = st.form(key='my_form')
st.sidebar.text('Parameters')

drug_table = {'DrugNM':['Codeine','Hydrocodone','Hydromorphone','Morphine','Oxycodone','Oxymorphone','Tapentadol'],
    'MME':[0.15,1,4,1,1.5,3,0.4]}

drug_table = pd.DataFrame(drug_table)

drug_list = drug_table['DrugNM'].unique()

with st.sidebar.form(key = "userformat"):
    pill_count = st.number_input(label='How many pills are you prescribing ?',step=1,value=0)
    dosage = st.number_input(label='What is the opioid pill dosage in mg ?',step=1,value=5)
    min_quantity = st.text_input(label='What is the Min,Max pills per dosage (i.e. 1,2)')
    max_frequency = st.text_input(label="What is the max,min doses per day (Every 2 to 4 hours = 2,4) ?")
    drug = st.selectbox("Where do you live?", drug_list)
    calculate = st.form_submit_button(label = "Calculate MME")


pill_cnt = pill_count

st.write('You are prescribing: ',pill_cnt,"pills.")

#try:
#    try:
#        min_quantity = input('Min,Max pills per dosage? (ie. 1,2) ')
#        min_quantity,max_quantity = min_quantity.split(',')
#    except ValueError:
#        max_quantity = min_quantity
#    min_quantity = int(min_quantity)
#    max_quantity = int(max_quantity)
#except ValueError:
#    print('Entered value(s) is not a number or they were not separator by a comma.')
    #input('Min,Max pills per dosage? (ie. 1,2) ')