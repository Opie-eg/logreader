from datetime import datetime
import json
CURRENTYEAR = str(datetime.now().year)
CURRENTMONTH = datetime.now().month - 1 
ALLMONTHS = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
"""

Falha no acesso à base de dados do web service! -> FalhaBD -> 0
Falha no acesso ao web service! -> FalhaWS -> 1
O leitor Impinj Ligou ->LeitorL -> 2
O leitor Impinj Desligou -> LeitorD -> 3 
Este codigo RFID não está autorizado a sair: -> RFIDSair -> 3
Sentido 1_2 -> Sentido1_2
Sentido 2_1 -> Sentido2_1 
Não foi possível adicionar a passagem ao webservice! -> NoPassagemWS
O serviço parou -> ServiceStop

"""
from pathlib import Path




def updateUserScore(userscore,computer,notitype):
       #userscore e o valor a adicionar aos contadores
       fle = Path('statistics.json')
       fle.touch(exist_ok=True)
       with open(fle, "r") as read_file:
              try:
                     logValues = json.loads(read_file.read())
                     print(logValues)
              except json.decoder.JSONDecodeError:
                     logValues = ""
                     print(logValues)
              score= userscore
              newTypeLogValues = {}
              LogName = {}
              months={"jan":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "fev":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "mar":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "abr":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "mai":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "jun":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "jul":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "ago":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "set":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "out":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "nov":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0},
              "dez":{"FalhaBD":0,"FalhaWS":0,"LeitorL":0,"LeitorD":0,"RFIDSair":0,
                     "Sentido1-2":0,"Sentido2-1":0,"NoPassagemWS":0,"ServiceStop":0}}
              month_with_Score = months
              month_with_Score[ALLMONTHS[CURRENTMONTH]][notitype] = score
              if (logValues == ""):
                     #//logValues[currentYear][username][months][0 ou 1]
                     LogName[computer]= month_with_Score
                     newTypeLogValues[CURRENTYEAR]= LogName
                     f = open("statistics.json", "w+", encoding= "utf-8")  # open file in write mode
                     #f.write(str(newLogValues))
                     f.write(json.dumps(newTypeLogValues, indent=4))
                     f.close()
              else:
                     #obj = { key: undefined };
                     #print("key" in obj); 
                     if(CURRENTYEAR in logValues):
                            if(computer in logValues[CURRENTYEAR]) :
                                   newLogValues = logValues
                                   newLogValues[CURRENTYEAR][computer]\
                                          [ALLMONTHS[CURRENTMONTH]][notitype]+= score
                            else:
                                   newLogValues = logValues
                                   newLogValues[CURRENTYEAR][computer]= month_with_Score
                     else:
                            newLogValues = logValues
                            LogName[computer]= month_with_Score
                            newLogValues[CURRENTYEAR]+= LogName
                     f = open("statistics.json", "w+", encoding= "utf-8")  # open file in write mode
                     #f.write(str(newLogValues))
                     f.write(json.dumps(newLogValues, indent=4))
                     f.close()

if __name__ == "__main__":
       updateUserScore(15,"Desktop-5B","FalhaBD")