def rank_airport(row):
    a=0
    if row['dist_airport']<=10:
        a+=10 
    elif row['dist_airport']<=20:
        a+=5
    elif row['dist_airport']<=40:
        a+=2
    else:
        a+=0
    return a 

def rank_starbucks(row):
    a=0
    if row['dist_starbucks']<=100:
        a+=10 
    elif row['dist_starbucks']<=200:
        a+=5
    elif row['dist_starbucks']<=500:
        a+=2
    else:
        a+=0
    return a 

def rank_vegan(row):
    a=0
    if row['dist_vegan']<=100:
        a+=10 
    elif row['dist_vegan']<=200:
        a+=5
    elif row['dist_vegan']<=500:
        a+=2
    else:
        a+=0
    return a 

def rank_schools(row):
    a=0
    if row['dist_school']<=500:
        a+=10 
    elif row['dist_school']<=1000:
        a+=5
    elif row['dist_school']<=2000:
        a+=2
    else:
        a+=0
    return a 
