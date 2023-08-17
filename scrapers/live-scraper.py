from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as timee
import paramiko
import pysftp



gender = 'women'
division = '3'


print('1')
ssh_client = paramiko.SSHClient()
print('2')
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('3')
ssh_client.connect('laxscores.com', 22, 'patmc225', 'mcrick24')
print('4.5')
# Read the current JSON data from the remote file
stdin, stdout, stderr = ssh_client.exec_command(f'cat {"/home/patmc225/laxscores.com/games.json"} ')
print('5')
json_data = json.loads(stdout.read().decode())
print('6')
sftp_client = ssh_client.open_sftp()
print('4') 

#with open('testjawn.json', 'r') as file:
                #json_data = json.load(file)


league = 'MSL'

while(league=='PLLs'):  
    try:
        pll.refresh()  
    except:
        continue
    print('new loop')
    # Loading PLL Website
    


    bigstring = ""
    count = 34

    # Looping Through Each Sub-Schedule
    try:
        schedule = pll.find_elements(By.CLASS_NAME, 'css-pvnqtb') 
    except:
        schedule =[]
        print('failed schedule')

    for s in schedule: 
        # Looping Through Each Game
        try:
            games = s.find_elements(By.TAG_NAME,'tr')
        except:
            games = []
            print('failed games')

        for game in games:
            count+=1
            print(count)
            # Finding Times
            
            try:
                date = game.find_element(By.TAG_NAME, 'td').text

                if(date[4]==(" ")): date = date[5:len(date)]
                else: date = date[7:len(date)]
                date = date.replace("• ", "")
                date = date.split(' ')
                date.append('')
                date.append('')
                date.append('')
                month = date[0]
                day = date[1]
                
                time = date[2]
            except:
                time = ''
                print('failed time')

            # Finding Team Names
            try: 
                teamsCon = game.find_elements(By.CLASS_NAME, 'results') [0]  
                team1 = teamsCon.find_elements(By.TAG_NAME, 'a')[0].text
                team2 = teamsCon.find_elements(By.TAG_NAME, 'a')[1].text 
            except:
                team1 = ''
                team2 = ''
                print('failed teams')

            # Finding Scores
            try: 
                scores = game.find_elements(By.CLASS_NAME, 'resultItem')
                score1 = scores[0].text
                score2 = scores[1].text
            except:
                score1 = ''
                score2 = ''
                print('failed scores')

            date = "2023-"
            if(month=="Jul" or month=="July"): date+="07-"
            elif(month=="Aug"): date+="08-"
            elif(month=="Sept"): date+="09-"
            if(len(day)<2): date+="0"+day
            else: date+=day

            new_game = date+team1+team2
            print('adding new data') 
            if(date!='' and team1!='' and team2!=''):
                json_data[league][count][date+team1+team2]["score1"] = score1
                json_data[league][count][date+team1+team2]["score2"] = score2
                if(len(game.find_elements(By.CLASS_NAME,'live'))>0):json_data[league][count][date+team1+team2]["time"] = 'Live'
                else: json_data[league][count][date+team1+team2]["time"] = time
            print('added new data') 
    print('ended launch') 

    print('saving data')
    modified_json_str = json.dumps(json_data)
    print('dumped')
        

    print('got sftp')
    with sftp_client.open('/home/patmc225/laxscores.com/games.json', "w") as remote_file:
        remote_file.write(modified_json_str)

    print('saved data')
if(league=='PLL'):
    try:
        pll = webdriver.Chrome()
        pll.get('https://stats.premierlacrosseleague.com/games/2023/game-33-2023-08-11?_ga=2.20305534.73563531.1691809013-1860596051.1685815842')
    except:
        print('failed launch')
    timee.sleep(10)

    date='2023-08-12'
    # Finding Team Names
    try: 
        teamsCon = pll.find_elements(By.CLASS_NAME, 'teamName')  
        team1 = teamsCon[0].text
        team2 = teamsCon[1].text 
    except:
        team1 = ''
        team2 = ''
        print('failed teams')
    count = 41
    print(json_data[league][count])
    time=''
    while(time!='Final'):
        print('')
        print('')
        print('')
        print('new loop')
        timee.sleep(10)
        # Finding Scores
        try: 
            scores = pll.find_elements(By.CLASS_NAME, 'css-1ah3t3c')
            score1 = scores[0].text
            score2 = scores[2].text
        except:
            score1 = ''
            score2 = ''
            print('failed scores')
        try:
            time = pll.find_elements(By.CLASS_NAME,'css-j82ltk')[0].text
        except: time = ''

        new_game = date+team1+team2
        print('adding new data') 
        if(date!='' and team1!='' and team2!=''):
            json_data[league][count][date+team1+team2]["score1"] = score1
            json_data[league][count][date+team1+team2]["score2"] = score2
            if(time!='Final'):json_data[league][count][date+team1+team2]["time"] = 'Live: ' + time
            else: json_data[league][count][date+team1+team2]["time"] = ''
        print('added new data') 
        print('ended launch') 

        print('saving data')
        modified_json_str = json.dumps(json_data)
        print('dumped')
            

        print('got sftp')
        with sftp_client.open('/home/patmc225/laxscores.com/games.json', "w") as remote_file:
            remote_file.write(modified_json_str)

        print('saved data')
    pll.quit()
if(league=='WLA'):
    print(json_data[league][61])
    wla = webdriver.Chrome()
    wla.get("https://www.wlalacrosse.com/schedule")
    timee.sleep(10)
    counter = 0
    count=61
    

    things = wla.find_element(By.CLASS_NAME,'table-scroll').find_element(By.TAG_NAME,'tbody').find_elements(By.CSS_SELECTOR, 'tr.ng-scope')
    for thing in things:
        counter+=1
        if(counter>4):
            try: date = thing.find_elements(By.CLASS_NAME, 'center.ng-binding')[1].text
            except: continue

            date = date.split(' ')
            month = date[1]
            day = date[2]

            teams = thing.find_elements(By.CLASS_NAME,'d.t.ng-binding')
            team1 = teams[0].text 
            team2 = teams[1].text
            print(team1+' vs ' +team2)
            
            link = thing.find_element(By.CLASS_NAME,'center.actions').find_element(By.TAG_NAME,'a').get_attribute('href')                   
            
            #score1 = thing.find_elements(By.CLASS_NAME,'center')[2].find_elements(By.TAG_NAME,'span')[0].find_elements(By.TAG_NAME,'span')[0].text
            #score2 = thing.find_elements(By.CLASS_NAME,'center')[2].find_elements(By.TAG_NAME,'span')[0].find_elements(By.TAG_NAME,'span')[1].text

            time = thing.find_elements(By.CLASS_NAME, 'center.ng-binding')[2].text




            date = "2023-"
            if(month=='DECEMBER'): date="2022-01-"
            if(month=="JANUARY"): date+="01-"
            elif(month=="Feb" or month=="02" or month=="FEBRUARY"): date+="02-"
            elif(month=="03" or month=="MARCH"): date+="03-"
            elif(month=="04" or month=="APRIL"): date+="04-"
            elif(month=="05" or month=="MAY" or month=="May"): date+="05-"
            elif(month=="Jun" or month=="JUNE" or month=="June"): date+="06-"
            elif(month=="Jul" or month=="July"): date+="07-"
            elif(month=="Aug"): date+="08-"
            elif(month=="Sept"): date+="09-"
            if(len(day)<2): date+="0"+day
            else: date+=day
            date = date.replace(',','')

            new_game = date+team1+team2

            new_game = {
                new_game: {
                "date": date,
                "time": time,
                "team1": team1,
                "team2": team2,
                "location": team2,
                "competition": 'WLA Finals: Game ',
                "link": link,
                "tv": '',
                "score1": '',
                "score2": ''
                }
            }
            #print(json_data[league][count])
            #print(json_data[league][count][date+team1+team2])
            json_data[league].append(new_game)
            #count-=1

    wla.quit()

    modified_json_str = json.dumps(json_data)
    with sftp_client.open('/home/patmc225/laxscores.com/games.json', "w") as remote_file:
        remote_file.write(modified_json_str)
if(league=='MSL'):
    loopcounter = 0
    count = 49
    date='2023-08-15'
    team1 = 'Peterborough Lakers'
    team2 = 'Six Nations Chiefs'
    print(json_data[league][count])
    time=''
    
    try:
        msl = webdriver.Chrome()
        msl.get('https://gamesheetstats.com/seasons/3246/games/1446443')
    except:
        print('failed launch')
    timee.sleep(10)

    while(time!='Final'):
        print('')
        print('')      
        print('new loop: ')
        print(loopcounter)
        timee.sleep(10)

        # Finding Scores
        try: 
            scores = msl.find_elements(By.CLASS_NAME, 'final-score')
            score1 = scores[0].text
            score2 = scores[1].text
        except:
            score1 = ''
            score2 = ''
            print('failed scores')
        print(score1+' '+score2)

        try:
            thing = msl.find_element(By.CLASS_NAME,'sc-ipEyDJ.bisAuX.undefined.title-bar2.undefined')
            print('got fitst')
            time = thing.find_element(By.TAG_NAME, 'span').text
        except: 
            time = 'Live'
            print('failed time')
        if(time=='IN PROGRESS (LIVE)'): time = 'Live'
        print(time)

        print('adding new data') 
        if(date!='' and team1!='' and team2!=''):
            json_data[league][count][date+team1+team2]["score1"] = score1
            json_data[league][count][date+team1+team2]["score2"] = score2
            if(time!='SCHEDULED' and time!='FINAL'):json_data[league][count][date+team1+team2]["time"] = 'Live: ' + time
            elif(time=='SCHEDULED'): time = time
            else: json_data[league][count][date+team1+team2]["time"] = ''
        print('added new data') 

        print('saving data')
        modified_json_str = json.dumps(json_data)
        print('dumped')
        with sftp_client.open('/home/patmc225/laxscores.com/games.json', "w") as remote_file:
            remote_file.write(modified_json_str)
        print('saved data')
        msl.refresh()
        loopcounter +=1

    msl.quit()


if(league=='MLSS'):

    msl = webdriver.Chrome()
    msl.get("https://gamesheetstats.com/seasons/3246/schedule")
    timee.sleep(60)

    d = ''

   
    #things = msl.find_elements(By.CLASS_NAME, 'ScoreBoxstyles__StyledScoreBox-sc-7hv0ta-0.dpLruS')
    things = msl.find_elements(By.CLASS_NAME, 'box')
    for thing in things:
        #date = thing.find_elements(By.CLASS_NAME, 'game-date')[0].text
        date = thing.find_elements(By.CLASS_NAME, 'date')[0].text
        date = date.split(' ')
        month = date[0]
        day = date[1]

        teams = thing.find_elements(By.CLASS_NAME,'team-name')
        team1 = teams[0].text 
        team2 = teams[1].text
        

        link = thing.find_element(By.CLASS_NAME,'button-container').find_element(By.TAG_NAME,'a').get_attribute('href')                   
        
       # score1 = thing.find_element(By.CLASS_NAME,'final-score.final-score-visitor').text
       # score2 = thing.find_element(By.CLASS_NAME,'final-score.final-score-home').text

        time = thing.find_element(By.CLASS_NAME,'time').text


        date = "2023-"
        if(month=="Aug"): date+="08-"
        elif(month=="Sept"): date+="09-"
        if(len(day)<3): date+="0"+day
        else: date+=day
        date = date.replace(',','')

        new_game = date+team1+team2

        new_game = {new_game:{"date": date,"time": time,"team1": team1,"team2": team2,"location": team2,"competition": 'Semifinal: Game ',"link": link,"tv": '',"score1": '',"score2": ''}}

        json_data[league].append(new_game)

        modified_json_str = json.dumps(json_data)
    
        sftp_client = ssh_client.open_sftp()
        with sftp_client.open('/home/patmc225/laxscores.com/games.json', "w") as remote_file:
            remote_file.write(modified_json_str)

    msl.quit()


sftp_client.close()

ssh_client.close()