from datetime import datetime
from tokenize import String
'''

"2023":{
        "Guia":{
            "jan":[1,0],
            "fev":[1,0],
            "mar":[1,0],
            "abr":[1,0],
            "mai":[1,0],
            "jun":[1,0],
            "jul":[1,0],
            "ago":[1,0],
            "set":[1,0],
            "out":[1,0],
            "nov":[1,0],
            "dez":[1,0]},
        "DC":{
            "jan":[1,0],
            "fev":[1,0],
            "mar":[1,0],
            "abr":[1,0],
            "mai":[1,0],
            "jun":[1,0],
            "jul":[1,0],
            "ago":[1,0],
            "set":[1,0],
            "out":[1,0],
            "nov":[1,0],
            "dez":[1,0]},
    }

'''

CURRENTYEAR = String(datetime.now().year)
CURRENTMONTH = datetime.now().month - 1 
print(CURRENTMONTH)
ALLMONTHS = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]

logValues = ""
def updateUserScore(userscore,computer):
    score= userscore
    userLogValues = {}
    LogName = {}
    months={"jan":[0,0],"fev":[0,0],"mar":[0,0],"abr":[0,0],"mai":[0,0],"jun":[0,0]
            ,"jul":[0,0],"ago":[0,0],"set":[0,0],"out":[0,0],"nov":[0,0],"dez":[0,0]}
    month_with_Score = months
    month_with_Score[ALLMONTHS[CURRENTMONTH]] = [score,0]
    if (logValues == ""):
        #//logValues[currentYear][username][months][0 ou 1]
        LogName[computer]= month_with_Score
        userLogValues[CURRENTYEAR]= LogName
    
    else:
        #obj = { key: undefined };
        #print("key" in obj); 
        if(CURRENTYEAR in logValues):
            if(logValues[CURRENTYEAR][computer]) :
                newLogValues = logValues
                newLogValues[CURRENTYEAR][computer][ALLMONTHS[CURRENTMONTH]][0]+= score

            else:
                newLogValues = logValues
                newLogValues[CURRENTYEAR][computer]= month_with_Score

            
        else:
            newLogValues = logValues
            LogName[computer]= month_with_Score
            newLogValues[CURRENTYEAR]+= LogName
        
