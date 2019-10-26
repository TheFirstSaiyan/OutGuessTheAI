import os;
import requests;
import csv
from bs4 import BeautifulSoup
import random

user_name = 'KamiVS'
main_link = 'https://paladins.guru/profile/13966361-'+user_name+'/matches?page='
match_summary_link = 'https://paladins.guru/match/'

def get_id(champion):
    if(champion=='ash'):
        return 2
    elif(champion=='barik'):
        return 3
    elif(champion=='fernando'):
        return 5
    elif(champion=='inara'):
        return 7
    elif(champion=='khan'):
        return 11
    elif(champion=='makoa'):
        return 13
    elif(champion=='ruckus'):
        return 17
    elif(champion=='terminus'):
        return 19
    elif(champion=='torvald'):
        return 23
    elif(champion=='bomb king'):
        return 29
    elif(champion=='cassie'):
        return 31
    elif(champion=='dredge'):
        return 37
    elif(champion=='drogoz'):
        return 41
    elif(champion=='imani'):
        return 43
    elif(champion=='kinessa'):
        return 47
    elif(champion=='lian'):
        return 53
    elif(champion=='sha lin'):
        return 59
    elif(champion=='strix'):
        return 61
    elif(champion=='tyra'):
        return 67
    elif(champion=='viktor'):
        return 71
    elif(champion=='vivian'):
        return 73
    elif(champion=='willo'):
        return 79
    elif(champion=='furia'):
        return 83
    elif(champion=='grohk'):
        return 89
    elif(champion=='grover'):
        return 97
    elif(champion=='jenos'):
        return 101
    elif(champion=='mal\'damba'):
        return 103
    elif(champion=='pip'):
        return 107
    elif(champion=='seris'):
        return 109
    elif(champion=='ying'):
        return 113
    elif(champion=='androxus'):
        return 127
    elif(champion=='buck'):
        return 131
    elif(champion=='evie'):
        return 137
    elif(champion=='koga'):
        return 139
    elif(champion=='lex'):
        return 149
    elif(champion=='maeve'):
        return 151
    elif(champion=='moji'):
        return 157
    elif(champion=='skye'):
        return 163
    elif(champion=='talus'):
        return 167
    elif(champion=='zhin'):
        return 173
    elif(champion=='atlas'):
        return 179
    elif(champion=='io'):
        return 181

def get_random_match():
    p = random.randint(1,30)
    link=main_link + str(p)
    contents = BeautifulSoup(requests.get(link).content,'html.parser').findAll('div',{'class':'d-flex'})
    csv_data = []
    for content in contents:
        id = content.find('a').get('href')
        match_link = 'https://paladins.guru/match/'+id[-9:]
        page = requests.get(match_link)
        
        row = []
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        team1_product=1
        team2_product=1
        
        pick = random.random()
        team1=[]
        team2=[]
        champs=[]
        dmges=[]
        shieldings=[]
        kdas=[] 
        ret_data={}
        
        if(pick > 0.5):
            
            # WINNING TEAM DATA

            win_div = soup.find('div',{'class':'match-table win'})
            match_body_rows = win_div.findAll('div',{'class':'row match-table__row'})
            for match_body_row in match_body_rows:
                champion_name = match_body_row.find('div',{'class':'row__player'}).find('img').get('alt')

                champs.append(champion_name)
                
                team1_product = team1_product * get_id(str(champion_name.lower()))

                data = match_body_row.findAll('div')
                kdas.append(data[4].string)
                dmges.append(data[7].string)
                shieldings.append(data[9].string)
                for i in range(4,10):
                    if i==4:
                            _kda = data[i].string.split('/')
                            kill = _kda[0]
                            death = _kda[1]
                            row.append(kill)
                            row.append(death)
                            continue
                    elif i!=5 and i!=6:
                        
                        row.append(data[i].string.replace(',',''))

            team1.append(champs) 
            team1.append(kdas)
            team1.append(dmges)
            team1.append(shieldings)
                    

            row.append(team1_product)
            # LOSING TEAM DATA

            champs=[]
            dmges=[]
            shieldings=[]
            kdas=[]

            lose_div = soup.find('div',{'class':'match-table loss'})
            match_body_rows = lose_div.findAll('div',{'class':'row match-table__row'})
            for match_body_row in match_body_rows:
                champion_name = match_body_row.find('div',{'class':'row__player'}).find('img').get('alt')

                champs.append(champion_name)

                team2_product = team2_product * get_id(str(champion_name.lower()))            
                data = match_body_row.findAll('div')

                kdas.append(data[4].string)
                dmges.append(data[7].string)
                shieldings.append(data[9].string)

                for i in range(4,10):
                    if i==4:
                            _kda = data[i].string.split('/')
                            kill = _kda[0]
                            death = _kda[1]
                            row.append(kill)
                            row.append(death)
                            continue
                    elif i!=5 and i!=6:
                            row.append(data[i].string.replace(',',''))

            team2.append(champs) 
            team2.append(kdas)
            team2.append(dmges)
            team2.append(shieldings)
                        

            row.append(team2_product)

            row.append(0)
            ret_data = {"team1":team1,"team2":team2,"win":0}
            
        elif(pick <=0.5):
            
            
            # LOSING TEAM DATA

            lose_div = soup.find('div',{'class':'match-table loss'})
            match_body_rows = lose_div.findAll('div',{'class':'row match-table__row'})
            for match_body_row in match_body_rows:
                champion_name = match_body_row.find('div',{'class':'row__player'}).find('img').get('alt')

                champs.append(champion_name)
                team2_product = team2_product * get_id(str(champion_name.lower()))            
                data = match_body_row.findAll('div')
                kdas.append(data[4].string)
                dmges.append(data[7].string)
                shieldings.append(data[9].string)
                for i in range(4,10):
                    if i==4:
                            _kda = data[i].string.split('/')
                            kill = _kda[0]
                            death = _kda[1]
                            row.append(kill)
                            row.append(death)
                            continue
                    if i!=5 and i!=6:
                        row.append(data[i].string.replace(',',''))

            team1.append(champs) 
            team1.append(kdas)
            team1.append(dmges)
            team1.append(shieldings)
            row.append(team2_product)
            # WINNING TEAM DATA
            champs=[]
            dmges=[]
            shieldings=[]
            kdas=[]

            win_div = soup.find('div',{'class':'match-table win'})
            match_body_rows = win_div.findAll('div',{'class':'row match-table__row'})
            for match_body_row in match_body_rows:
                champion_name = match_body_row.find('div',{'class':'row__player'}).find('img').get('alt')
                champs.append(champion_name)

                
                team1_product = team1_product * get_id(str(champion_name.lower()))

                data = match_body_row.findAll('div')
                kdas.append(data[4].string)
                dmges.append(data[7].string)
                shieldings.append(data[9].string)

                for i in range(4,10):
                    if i==4:
                            _kda = data[i].string.split('/')
                            kill = _kda[0]
                            death = _kda[1]
                            row.append(kill)
                            row.append(death)
                            continue
                    if i!=5 and i!=6:
                        row.append(data[i].string.replace(',',''))
            team2.append(champs) 
            team2.append(kdas)
            team2.append(dmges)
            team2.append(shieldings)

            row.append(team1_product)

            row.append(1)
            ret_data = {"team1":team1,"team2":team2,"win":1}

       # print(row)
        return (row, ret_data, )

        break;



    
