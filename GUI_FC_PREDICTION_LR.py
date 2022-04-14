from tkinter import *
import numpy as np
import pandas as pd
from tkinter import filedialog

master = Tk()
master.configure(background='black')
master.title("Extracted Data Fuel Calculation")
master.geometry("385x520")
master.minsize(385,520)
master.maxsize(385,520)

def consumptionFile():
    global filepath1
    filepath1 = filedialog.askopenfilename(initialdir="/", title="Fuel Consumption Chart",
                                          filetypes= (("CSV files","*.csv"),))
    

def cphChart():
    global filepath2
    filepath2 = filedialog.askopenfilename(initialdir="/", title="CPH Chart",
                                          filetypes= (("CSV files","*.csv"),))


def calculateCPH():
    global filepath1
    global filepath2
    #res=int(e1.get())+int(e2.get())
    
    genset_size_kva = float(e1.get())
    power_factor = float(e2.get())
    genset_size = genset_size_kva*power_factor
    
    df = pd.read_csv(filepath1)
    load_pct = {
        "load":[0.5,0.75,1],
        "cph":[float(load_50_cph.get()),float(load_75_cph.get()),float(load_100_cph.get())]
        }
    load_pct = pd.DataFrame(load_pct)

    df.fillna(method='ffill',inplace=True)

    df.columns = ['time_stamp','fuel_level','genset_run','rect_current','rect_voltage']
    load_pct.columns = ['load','cph']

    fuel_level = list(df['fuel_level'])

    genset_run = 0
    for i in df['genset_run']:
        genset_run = genset_run + i

    length_of_inner_loop_1 = 9
    index = 0
    for i in range(0,len(fuel_level)):
        counter = 0
       
        #Write your code here:
        while index+length_of_inner_loop_1>len(fuel_level)-1:
            length_of_inner_loop_1 -= 1
           
            if length_of_inner_loop_1 == 0:
                break
       
        if length_of_inner_loop_1>1:
            if abs(fuel_level[index+1]-fuel_level[index])>=50:
                for k in range(index+1,index+length_of_inner_loop_1):
                    if abs(fuel_level[k] - fuel_level[index]) < 50:
                        counter += 1
                if (counter < length_of_inner_loop_1-1) and (counter != 0):
                    for k in range(index,index+counter):
                        fuel_level[k] = fuel_level[index]
                if abs(fuel_level[index+1]-fuel_level[index]) > 500:
                    fuel_level[index+1] = fuel_level[index]
                   
        index +=1

    consumption = []
    lower_peak = 0
    length_of_inner_loop_1 = 9
    length_of_inner_loop_2 = 9
    index_upper = 0

    index = 0
    length_of_inner_loop = 9
    for i in range(0,len(fuel_level)):
        counter_first_upper=0
        while index+length_of_inner_loop>len(fuel_level)-1:
            length_of_inner_loop -= 1
            if length_of_inner_loop == 0:
                break
        if length_of_inner_loop>1:
            for j in range(index+1,index+length_of_inner_loop):
                if fuel_level[index] > fuel_level[j]:
                    counter_first_upper += 1
        if counter_first_upper==8:
            break
        else:
            index+=1

    upper_peak=fuel_level[index]

    for i in range(index,len(fuel_level)):
       
        counter_lower = 0
       
        #This condition is to check whether there is a huge dip in next value as compared to previous value
        #This will replace next value with current value if a huge dip occured in next value
        #if index+1<len(fuel_level)-1:
         #   if (fuel_level[index] - fuel_level[index+1] > 30):
          #      fuel_level[index+1] = fuel_level[index]
       
           
        #This loop is to check if we are exceeding from our total length of the list
        #If index+length_of_inner_loop is exceeding the total length, this will decrease 1 from length_of_inner_loop
        #This is for the time when the iteration on the list (fuel_length) is about to end
        while index+length_of_inner_loop_1>len(fuel_level)-1:
            length_of_inner_loop_1 -= 1
            if length_of_inner_loop_1 == 0:
                break    
       
        #Here, checking if length_of_inner_loop>1 (means 2 or more than 2)
        #Because in the inner for loop, it will meet the stopping condition
        if length_of_inner_loop_1>1:
                       
            #Purpose of this loop is to compare the current fuel_level value to the next 8 fuel_level values (Half hour in time)
            #If any next value greater than current value occured, the counter variable would be increased by 1
            for j in range(index+1,index+length_of_inner_loop_1):
                if fuel_level[index] < fuel_level[j]:
                    counter_lower += 1
           
           
            #Below 2 conditions are been checked
           
            #1. If counter == 8 which means all next 8 values are greater than the current value.
            #   It means we have reached to the last fuel level before refill.
           
            #2. If the difference of current and next value is >= 40. This is done to ignore the small fluctuations.
            #   It says, consider only those values whose difference with next value is greater than 40, otherwise ignore them.
            #print("Upper Peak: "+str(upper_peak))
            #print("Lower Peak: "+str(lower_peak))
            if ((counter_lower == length_of_inner_loop_1-1) and (abs(fuel_level[index]-fuel_level[index+length_of_inner_loop_1-1])>=40)):
               
                #Below, we are updating lower_peak, upper_peak and also calculating the consumption
                #If the upper 2 conditions are satified, then:
                #1. Assign the current value to lower peak
                #2. Calculate consumption by subtracting lower peak with current upper_peak
                #3. Update upper_peak with a value 8 units ahead (Half hour in time) of lower peak.
               
                lower_peak = fuel_level[index]
                consumption.append(upper_peak - lower_peak)
                index_upper=index-1
                for i in range(index,len(fuel_level)):
                    counter_upper=0
                    while index_upper+length_of_inner_loop_2>len(fuel_level)-1:
                        length_of_inner_loop_2 -= 1
                        if length_of_inner_loop_2 == 0:
                            break
                    if length_of_inner_loop_2>1:
                        for j in range(index_upper+1,index_upper+length_of_inner_loop_2):
                            if fuel_level[index_upper] > fuel_level[j]:
                                counter_upper += 1
                    if counter_upper==8:
                        break
                    else:
                        index_upper+=1
                upper_peak=fuel_level[index_upper]
                #Now, increasing the index by 7 to ignore the values during refilling
                #This will allow the loop to iterate after the upper_peak index
                index = index_upper
           
            #If the iterations has reached to the end of the dataset, then check below conditions:
            #If counter==0 which means no greater value is after the current value, and
            #If length_of_inner_loop is 2 which means we have reached to the last point, then:
               
                # Assign the current value to lower_peak variable.
                # And calculate the last consumption of the dataset.
               

            elif((counter_lower>=0) and (length_of_inner_loop_1<=2)):
                #print("Upper Peak: "+str(upper_peak))
                #print("Lower Peak: "+str(lower_peak))

                lower_peak = fuel_level[index]
                consumption.append(upper_peak - lower_peak)

        #Increment index variable for next iteration
        index +=1


    # In[49]:


    df['rect_power'] = (df['rect_current']*df['rect_voltage'])/1000


    # In[50]:


    df['time_stamp'] = pd.to_datetime(df['time_stamp'])


    # In[51]:


    df['Day'] = df.time_stamp.dt.day
    df['Month'] = df.time_stamp.dt.month
    df['Hour'] = df.time_stamp.dt.hour


    # In[52]:





    # In[53]:


    df_avg_power = pd.DataFrame(df.groupby(['genset_run','Day','Month','Hour'])['rect_power'].mean()).sort_values(by=['Month','Day'])


    # In[54]:


    df_avg_power['rect_power'] = df_avg_power['rect_power']/genset_size  


    # In[55]:


    # grouped_df.groupby(['genset_run','Day','Month','Hour'])['genset_run'].sum()
    df_sum_genset_run = pd.DataFrame(df.groupby(['genset_run','Day','Month','Hour'])['genset_run'].sum()).sort_values(by=['Month','Day'])


    # In[56]:


    df_sum_genset_run.columns = ['genset_run_grouped']


    # In[57]:


    df_pct_genset_run = pd.DataFrame(df_sum_genset_run['genset_run_grouped']*(5/60))


    # In[58]:


    pd.set_option('Display.max_rows',10)


    # In[59]:


    df_merged = df_avg_power.merge(df_pct_genset_run,on=['genset_run','Day','Month','Hour'],how='inner')


    # In[60]:


    df_merged.columns = ['avg_rect_power','genset_run_per_hour_pct']


    # In[61]:


    df_merged = df_merged.reset_index()


    # In[62]:





    # In[63]:


    from sklearn.linear_model import LinearRegression


    # In[64]:


    lr = LinearRegression()


    # In[65]:


    load_x = pd.DataFrame(load_pct['load'])


    # In[66]:


    load_y = load_pct['cph']


    # In[67]:


    lr.fit(load_x,load_y)


    # In[68]:


    # avg_rect_power = pd.DataFrame(df_merged['avg_rect_power'])
    avg_rect_power = np.array(df_merged['avg_rect_power'])


    # In[69]:


    avg_rect_power = np.where(avg_rect_power<=load_pct.sort_values(by=['load']).iloc[0,0],load_pct.sort_values(by=['load']).iloc[0,0],avg_rect_power)


    # In[70]:


    avg_rect_power = pd.DataFrame(avg_rect_power)


    # In[71]:


    y_pred = lr.predict(avg_rect_power)


    # In[72]:


    y_pred = np.where(y_pred <= 0, 0, y_pred)


    # In[73]:


    predictions = pd.DataFrame(y_pred,columns=['average_CPH_from_LR'])


    # In[74]:


    final_consumptions = pd.concat([df_merged,predictions],axis='columns')


    # In[75]:


    final_consumptions['CPH'] = final_consumptions['genset_run_per_hour_pct']*final_consumptions['average_CPH_from_LR']


    # In[76]:


    CPH = list(final_consumptions['CPH'])
    consumption_counter = []
    consumption_counter.append(0)


    # In[77]:


    for i in range(1,len(CPH)):
        consumption_counter.append(consumption_counter[i-1]+CPH[i])


    # In[78]:


    consumption_counter = pd.DataFrame(consumption_counter,columns=['consumption_counter'])


    # In[79]:


    final_consumptions = pd.concat([final_consumptions,consumption_counter],axis='columns')


    # In[80]:
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(final_consumptions)
    #print("\n\n")
    #print("Consumptions before refilling: "+str(consumption))
    print("Total Genset Consumptions (Actual): "+str(sum(consumption)))
    print("Total Genset Consumptions (Predicted): "+str(final_consumptions.iloc[-1]['consumption_counter']))
   
    myText1.set(str(sum(consumption)))    
    myText2.set(str(final_consumptions.iloc[-1]['consumption_counter']))
    myText3.set(str(genset_run))
    myText4.set(str(sum(consumption)/genset_run))
    myText5.set(str(final_consumptions.iloc[-1]['consumption_counter']/genset_run))

filepath1 = ""
filepath2 = ""


myText1=StringVar()
myText2=StringVar()
myText3=StringVar()
myText4=StringVar()
myText5=StringVar()
Label(master, text="Extracted Data: ", bg='black',fg='white',font=("none 12 bold")).grid(row=0,sticky="nsew", padx=5, pady=10)
Label(master, text="Load: ", bg='black',fg='white',font=("none 12 bold")).grid(row=1,sticky="nsew", padx=5, pady=10)
Label(master, text="50%", bg='black',fg='white',font=("none 10 bold")).grid(row=1,column=1,pady=10)
Label(master, text="75%", bg='black',fg='white',font=("none 10 bold")).grid(row=1,column=2,pady=10)
Label(master, text="100%", bg='black',fg='white',font=("none 10 bold")).grid(row=1,column=3,pady=10)
Label(master, text="CPH: ", bg='black',fg='white',font=("none 12 bold")).grid(row=2,sticky="nsew", padx=5, pady=10)
Label(master, text="Genset Size (in KVa): ", bg='black',fg='white',font=("none 12 bold")).grid(row=3,sticky="nsew", padx=5, pady=10)
Label(master, text="Power Factor: ", bg='black',fg='white',font=("none 12 bold")).grid(row=4,sticky="nsew", padx=5, pady=10)
Label(master, text="Actual Fuel Consumption:", bg='black',fg='white',font=("none 12 bold")).grid(row=8,sticky="nsew", padx=5, pady=10)
Label(master, text="Calculated Fuel Consumption:", bg='black',fg='white',font=("none 12 bold")).grid(row=9,sticky="nsew", padx=5, pady=10)
Label(master, text="Genset Run:", bg='black',fg='white',font=("none 12 bold")).grid(row=10,sticky="nsew", padx=5, pady=10)
Label(master, text="CPH (Actual):", bg='black',fg='white',font=("none 12 bold")).grid(row=11,sticky="nsew", padx=5, pady=10)
Label(master, text="CPH (Calculated):", bg='black',fg='white',font=("none 12 bold")).grid(row=12,sticky="nsew", padx=5, pady=10)
result1=Label(master, text="", textvariable=myText1).grid(row=8,column=1,sticky="nsew", columnspan=3, padx=5, pady=10)
result2=Label(master, text="", textvariable=myText2).grid(row=9,column=1,sticky="nsew", columnspan=3, padx=5, pady=10)
result3=Label(master, text="", textvariable=myText3).grid(row=10,column=1,sticky="nsew", columnspan=3, padx=5, pady=10)
result4=Label(master, text="", textvariable=myText4).grid(row=11,column=1,sticky="nsew", columnspan=3, padx=5, pady=10)
result5=Label(master, text="", textvariable=myText5).grid(row=12,column=1,sticky="nsew", columnspan=3, padx=5, pady=10)

#e1 = Entry(master)
#e2 = Entry(master)
btn1 = Button(master, text="Fuel Consump. File", width=18, command=consumptionFile)
btn1.grid(columnspan=3)
#btn2 = Button(master, text="CPH chart", width=15, command=cphChart)
e1 = Entry(master)
e2 = Entry(master)

load_50_cph = Entry(master,width=5)
load_75_cph = Entry(master,width=5)
load_100_cph = Entry(master,width=5)

btn1.grid(row=0, column=1)
#btn2.grid(row=1, column=1)
load_50_cph.grid(row=2,column=1)
load_75_cph.grid(row=2,column=2)
load_100_cph.grid(row=2,column=3)
e1.grid(row=3, column=1, columnspan=3)
e2.grid(row=4, column=1, columnspan=3)


b = Button(master, width=25,height=2, text="Calculate",font=("none 12 bold"), bg="green", command=calculateCPH)
b.grid(row=6, column=0,columnspan=5, rowspan=2,sticky="nsew", padx=5, pady=10)
 
 
mainloop()