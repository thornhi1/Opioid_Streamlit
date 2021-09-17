# Load the needed libraries.
import streamlit as st
import pandas as pd

#Create a function to calculate the number of baseline data points needed (Step 3).
def baseline(min_daily_pill_cnt,max_daily_pill_cnt):
    i = 0
    x = []
    y = []
    if min_daily_pill_cnt > max_daily_pill_cnt:
        while i <= min_daily_pill_cnt:
            d = 1+i
            m = 50
            x.append(d)
            y.append(m) #baseline.append({'Day':day_number,'MME':daily_mme},ignore_index=True)
            i += 1
    else:
        while i < max_daily_pill_cnt:
            d = 1+i
            m = 50
            x.append(d)
            y.append(m)
            i += 1
    return (x,y)

#Create custom drug conversion factor table
drug_table = {'DrugNM':['Codeine','Hydrocodone','Hydromorphone','Morphine','Oxycodone','Oxymorphone','Tapentadol'],
    'MME':[0.15,1,4,1,1.5,3,0.4]}

drug_table = pd.DataFrame(drug_table)

# Main Body of the website
st.title('MME Checker')
st.subheader('Enter the parameters on the left to check if your prescription is in compliance with CDC recommendations for daily MME limits.')


#Navigation: User input on the left side of the screen
st.sidebar.text('Parameters')

drug_list = drug_table['DrugNM'].unique()

with st.sidebar.form(key = "userformat"):
    pill_count = st.number_input(label='How many pills are you prescribing ?',step=1,value=0)
    dosage = st.number_input(label='What is the opioid pill dosage in mg ?',step=1,value=5)
    min_quantity = st.number_input(label='What is the Min number of pills per dosage?',step=1,value=0)
    max_quantity = st.number_input(label='What is the Max number of pills per dosage?',step=1)
    max_frequency = st.number_input(label='What is the least time (hours) between doses?',step=1,value=0)
    min_frequency = st.number_input(label='What is the most time (hours) between doses?',step=1)
    drug = st.selectbox('Which drug are you Prescribing?', drug_list)
    calculate = st.form_submit_button(label = "Calculate MME")


# Set the variables based on the user input from the left side.
pill_cnt = pill_count

st.write('You are prescribing: ',pill_cnt,"pills.")


#if test_freq:
#    try:
#        try:
#            test_freq,max_quantity = test_freq.split(',')
#        except ValueError:
#            max_quantity = test_freq
#        test_freq = int(test_freq)
#        max_quantity = int(max_quantity)
#    except ValueError:
#        print('Entered value(s) is not a number or they were not separator by a comma.')


day_number = 0
day_number2 = 0
min_plot = pd.DataFrame(columns=['Day','MME'])
max_plot = pd.DataFrame(columns=['Day','MME'])

# Assign the appropriate pill count for each quanity variable.
# if min_quantity == 0 & max_quantity > 0:
#         min_quantity = max_quantity
# elif min_quantity > 0 & max_quantity == 0:
#     max_quantity = min_quantity
# else:
#     min_quantity = min_quantity
#     max_quantity = max_quantity

# # Assign the appropriate dose frequency based on user input.
# if min_frequency == 0 & max_frequency > 0:
#         min_frequency = max_frequency
# elif min_frequency > 0 & max_frequency == 0:
#     max_frequency = min_frequency
# else:
#     min_frequency = min_frequency
#     max_frequency = max_frequency

#min_daily_pill_cnt = pill_cnt / (24 / (min_frequency*min_quantity))  ## Check this 9.9.21
#max_daily_pill_cnt = pill_cnt / (24 / (min_frequency*min_quantity))  ## Check this 9.9.21
#pill_cnt_counter = pill_cnt
#pill_cnt_counter2 = pill_cnt

mme_multiplier = drug_table.loc[drug_table['DrugNM'] == drug, 'MME'].iloc[0]


# Use for outputting a graph
if calculate:
    st.write('The conversion factor is:',mme_multiplier)
    # Assign the appropriate pill count for each quanity variable.
    if (min_quantity == 0) & (max_quantity > 0):
        min_quantity = max_quantity
    if (min_quantity > 0) & (max_quantity == 0):
        max_quantity = min_quantity


# Assign the appropriate dose frequency based on user input.
    if (min_frequency == 0) & (max_frequency > 0):
        min_frequency = max_frequency
    if (min_frequency > 0) & (max_frequency == 0):
        max_frequency = min_frequency
        
    pill_cnt_counter = pill_cnt
    pill_cnt_counter2 = pill_cnt
    min_daily_pill_cnt = pill_cnt / (24 / (min_frequency*min_quantity))  ## Check this 9.9.21
    max_daily_pill_cnt = pill_cnt / (24 / (min_frequency*min_quantity))  ## Check this 9.9.21
    baseline_plot = baseline(min_daily_pill_cnt,max_daily_pill_cnt)
    st.write('The dose frequency is:',min_frequency,'and ',max_frequency)
    st.write('The pill count frequency is:',min_quantity,'and ',max_quantity)

    # Logic for calculating which graph to use and calculating the MME based on user input.
    if (min_quantity == max_quantity) & (max_frequency == min_frequency):
        daily_pill_cnt = 24 / (max_frequency * min_quantity)
        prescription_length_days = pill_cnt / daily_pill_cnt
        mme_plot = pd.DataFrame(columns=['Day','MME'])
        while pill_cnt_counter >= daily_pill_cnt:
            day_number = 1 + day_number
            daily_mme = dosage*daily_pill_cnt*mme_multiplier
            mme_plot = mme_plot.append({'Day':day_number,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter = pill_cnt_counter - daily_pill_cnt
        if pill_cnt%daily_pill_cnt != 0:
            mme_plot = mme_plot.append({'Day':day_number+1,'MME':dosage*pill_cnt_counter*mme_multiplier},ignore_index=True)
        else:
            pass
        st.write('You prescribed 1 dose and 1 frequency')
    elif (min_quantity == max_quantity) & (max_frequency != min_frequency):
        min_daily_pill_cnt = (24/min_frequency)*min_quantity
        max_daily_pill_cnt = (24/max_frequency)*min_quantity

        min_prescription_days = pill_cnt / max_daily_pill_cnt
        max_prescription_days = pill_cnt / min_daily_pill_cnt

        min_mme_plot = pd.DataFrame(columns=['Day','MME']) # max_mme
        max_mme_plot = pd.DataFrame(columns=['Day','MME']) # min_mme

        while pill_cnt_counter >= min_daily_pill_cnt:
            day_number = 1 + day_number
            daily_mme = dosage*min_quantity*min_daily_pill_cnt*mme_multiplier
            min_mme_plot = min_mme_plot.append({'Day':day_number,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter = pill_cnt_counter - min_daily_pill_cnt
        
        if pill_cnt%min_daily_pill_cnt != 0:
            min_mme_plot = min_mme_plot.append({'Day':day_number+1,'MME':dosage*pill_cnt_counter*mme_multiplier},ignore_index=True)
        else:
            pass

        while pill_cnt_counter2 >= max_daily_pill_cnt:
            day_number2 = 1 + day_number2
            daily_mme = dosage*min_quantity*max_daily_pill_cnt*mme_multiplier
            max_mme_plot = max_mme_plot.append({'Day':day_number2,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter2 = pill_cnt_counter2 - max_daily_pill_cnt

        if pill_cnt%max_daily_pill_cnt != 0:
            max_mme_plot = max_mme_plot.append({'Day':day_number2+1,'MME':dosage*pill_cnt_counter2*mme_multiplier},ignore_index=True)
        else:
            pass
        st.write('You prescribed 1 dose and 2 frequencies')
    #print('You prescribed 1 dose and 2 frequencies')
    elif (min_quantity != max_quantity) & (max_frequency == min_frequency):
        min_daily_pill_cnt = (24/max_frequency)*min_quantity         #The smallest total number of pills in a day.
        max_daily_pill_cnt = (24/max_frequency)*max_quantity         #The largest total number of pills in a day.

        min_prescription_days = pill_cnt / max_daily_pill_cnt   #The shortest amount of time before pills run out.
        max_prescription_days = pill_cnt / min_daily_pill_cnt   #The longest amount of time before pills run out.

        min_mme_plot = pd.DataFrame(columns=['Day','MME']) # min_mme
        max_mme_plot = pd.DataFrame(columns=['Day','MME']) # max_mme

        while pill_cnt_counter >= min_daily_pill_cnt:
            day_number = 1 + day_number
            daily_mme = dosage*min_daily_pill_cnt*mme_multiplier
            min_mme_plot = min_mme_plot.append({'Day':day_number,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter = pill_cnt_counter - min_daily_pill_cnt
        
        if pill_cnt%min_daily_pill_cnt != 0:
            min_mme_plot = min_mme_plot.append({'Day':day_number+1,'MME':dosage*pill_cnt_counter*mme_multiplier},ignore_index=True)
        else:
            pass

        while pill_cnt_counter2 >= max_daily_pill_cnt:
            day_number2 = 1 + day_number2
            daily_mme = dosage*max_daily_pill_cnt*mme_multiplier
            max_mme_plot = max_mme_plot.append({'Day':day_number2,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter2 = pill_cnt_counter2 - max_daily_pill_cnt

        if pill_cnt%max_daily_pill_cnt != 0:
            max_mme_plot = max_mme_plot.append({'Day':day_number2+1,'MME':dosage*pill_cnt_counter2*mme_multiplier},ignore_index=True)
        else:
            pass
        st.write('You prescribed multiple doses and only 1 frequency')
        #print('You prescribed multiple doses and only 1 frequency')
    else:
        min_daily_pill_cnt = (24/min_frequency)*min_quantity         #The smallest total number of pills in a day.
        max_daily_pill_cnt = (24/max_frequency)*max_quantity         #The largest total number of pills in a day.

        min_prescription_days = pill_cnt / max_daily_pill_cnt   #The shortest amount of time before pills run out.
        max_prescription_days = pill_cnt / min_daily_pill_cnt   #The longest amount of time before pills run out.

        min_mme_plot = pd.DataFrame(columns=['Day','MME']) # min_mme
        max_mme_plot = pd.DataFrame(columns=['Day','MME']) # max_mme

        while pill_cnt_counter >= min_daily_pill_cnt:
            day_number = 1 + day_number
            daily_mme = dosage*min_daily_pill_cnt*mme_multiplier
            min_mme_plot = min_mme_plot.append({'Day':day_number,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter = pill_cnt_counter - min_daily_pill_cnt
        
        if pill_cnt%min_daily_pill_cnt != 0:
            min_mme_plot = min_mme_plot.append({'Day':day_number+1,'MME':dosage*pill_cnt_counter*mme_multiplier},ignore_index=True)
        else:
            pass

        while pill_cnt_counter2 >= max_daily_pill_cnt:
            day_number2 = 1 + day_number2
            daily_mme = dosage*max_daily_pill_cnt*mme_multiplier
            max_mme_plot = max_mme_plot.append({'Day':day_number2,'MME':daily_mme},ignore_index=True)
            pill_cnt_counter2 = pill_cnt_counter2 - max_daily_pill_cnt

        if pill_cnt%max_daily_pill_cnt != 0:
            max_mme_plot = max_mme_plot.append({'Day':day_number2+1,'MME':dosage*pill_cnt_counter2*mme_multiplier},ignore_index=True)
        else:
            pass

        st.write('You prescribed multiple doses and frequencies.')