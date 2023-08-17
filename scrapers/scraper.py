import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as timee

league = 'WLA'

gender = 'women'
division = '3'

with open('real-games.json', 'r') as file:
                json_data = json.load(file)

if(league=='PLL'):    
    # Loading PLL Website
    pll = webdriver.Chrome()
    pll.get('https://premierlacrosseleague.com/schedule')


    bigstring = ""
    count = 0
    # Finding Buttons and Clicking Through Each
    b = pll.find_element(By.CLASS_NAME, 'swiper-wrapper')
    buttons = b.find_elements(By.CLASS_NAME, 'swiper-slide.swiperSlide')
    for button in buttons:
        button.click()

        # Finding Location
        try:
            l = pll.find_element(By.CLASS_NAME, 'gameInfo')
        except:
            break
        location = l.find_element(By.TAG_NAME, 'p').text
        location = location[(location.find("•")+2):(location.rfind("•"))]

        # Looping Through Each Sub-Schedule
        schedule = pll.find_elements(By.CLASS_NAME, 'css-pvnqtb') 
        for s in schedule: 

            # Looping Through Each Game
            games = s.find_elements(By.TAG_NAME,'tr')
            for game in games:
                count+=1

                # Finding Times
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
                time=date[2]

                # Finding Team Names
                try: 
                    teamsCon = game.find_elements(By.CLASS_NAME, 'results') [0]  
                    team1 = teamsCon.find_elements(By.TAG_NAME, 'a')[0].text
                    team2 = teamsCon.find_elements(By.TAG_NAME, 'a')[1].text 
                except:
                    team1 = ''
                    team2 = ''

                    

                event = ""
                if(count<21): event = "Regular Season"
                elif(count<23): event = "All Star Game"
                elif(count<43): event = "Regular Season"
                elif(count<46): event = "Quarterfinal"
                elif(count<48): event = "Semifinal"
                else: event = "Championship"

                try: link = game.find_element(By.CLASS_NAME, 'css-18irz2r').get_attribute('href')
                except: link = ''

                try:
                    t = game.find_element(By.CLASS_NAME, 'css-b6x483')     
                    channel = t.find_element(By.TAG_NAME, 'img').get_attribute('data-lazy')  

                    tv = channel[channel.index('Logos/')+6:channel.index('Logos/')+11]
                    if(tv == 'ESPN2'): tv = 'ESPN2'
                    elif(tv == 'ESPN%'): tv = 'ESPN+'
                    elif(tv == 'ESPN_'): tv= 'ESPN'
                    else: tv='ABC'
                except:
                    tv = 'ESPN+'

                # Finding Scores
                try: 
                    scores = game.find_elements(By.CLASS_NAME, 'resultItem')
                    score1 = scores[0].text
                    score2 = scores[1].text
                except:
                    score1 = ''
                    score2 = ''

                date = "2023-"
                if(month=='DECEMBER'): date="2022-01-"
                if(month=="JANUARY"): date+="01-"
                elif(month=="Feb" or month=="02" or month=="FEBRUARY"): date+="02-"
                elif(month=="03" or month=="MARCH"): date+="03-"
                elif(month=="04" or month=="APRIL"): date+="04-"
                elif(month=="05" or month=="MAY"): date+="05-"
                elif(month=="Jun" or month=="JUNE" or month=="June"): date+="06-"
                elif(month=="Jul" or month=="July"): date+="07-"
                elif(month=="Aug"): date+="08-"
                elif(month=="Sept"): date+="09-"
                if(len(day)<2): date+="0"+day
                else: date+=day

                new_game = date+team1+team2

                new_game = {
                    new_game: {
                    "date": date,
                    "time": time,
                    "team1": team1,
                    "team2": team2,
                    "location": location,
                    "competition": event,
                    "link": link,
                    "tv": tv,
                    "score1": score1,
                    "score2": score2
                    }
                }

                json_data[league].append(new_game)

    pll.quit()





if(league.__contains__('NCAA')):

    ncaa = webdriver.Chrome()
    ncaa.implicitly_wait(2)
    ncaa.get('https://www.ncaa.com/scoreboard/lacrosse-'+gender+'/d'+division+'/2023/02/01/all-conf')
    for m in range(2,6): 
        if(m != 2): 
            ncaa.find_element(By.CLASS_NAME, 'next').click()
            timee.sleep(2)
        buttons = ncaa.find_elements(By.CLASS_NAME, 'scoreboardDateNav-date.hasGames')
        for button in buttons:
            try:
                button.click()
            except:
                buttons = ncaa.find_elements(By.CLASS_NAME, 'scoreboardDateNav-date.hasGames')
                button.click()

            try: 
                g = ncaa.find_element(By.CLASS_NAME, 'gamePod_content')
                games = g.find_elements(By.CLASS_NAME, 'gamePod.gamePod-type-game.status-final')
            except: 
                break

            for game in games:
                teams = game.find_elements(By.CLASS_NAME,'gamePod-game-team-name' )
                scores = game.find_elements(By.CLASS_NAME, 'gamePod-game-team-score')
                day = ncaa.find_element(By.CLASS_NAME, 'scoreboardDateNav-date.hasGames.selected').find_element(By.CLASS_NAME, 'scoreboardDateNav-dayNumber').text

                try:
                    link = game.find_element(By.CLASS_NAME,'gamePod-link').get_attribute('href')
                except selenium.common.exceptions.StaleElementReferenceException:
                    link = ''
    
                round = ''
                
                if(int(m)>=5 and int(day)>=6):
                    try:
                        round = game.find_element(By.CLASS_NAME,'game-round').text     
                    except selenium.common.exceptions.NoSuchElementException:
                        round = ''



                month = "0" + str(m) 
                day = day      

                if ' ' in teams[0].text:    team1 = teams[0].text.replace(" ","-")
                else:                       team1 = teams[0].text     
                
                if ' ' in teams[2].text:    team2 = teams[2].text.replace(' ','-')
                else:                       team2 = teams[2].text

                competition = round                     # game type
                score1  = scores[0].text            # score 1
                score2 = scores[1].text          # score 2


                date = "2023-"
                if(month=='DECEMBER'): date="2022-01-"
                if(month=="JANUARY"): date+="01-"
                elif(month=="Feb" or month=="02" or month=="FEBRUARY"): date+="02-"
                elif(month=="03" or month=="MARCH"): date+="03-"
                elif(month=="04" or month=="APRIL"): date+="04-"
                elif(month=="05" or month=="MAY"): date+="05-"
                elif(month=="Jun" or month=="JUNE" or month=="June"): date+="06-"
                elif(month=="Jul" or month=="July"): date+="07-"
                elif(month=="Aug"): date+="08-"
                elif(month=="Sept"): date+="09-"
                if(len(day)<2): date+="0"+day
                else: date+=day

                new_game = date+team1+team2

                new_game = {
                    new_game: {
                    "date": date,
                    "time": '',
                    "team1": team1,
                    "team2": team2,
                    "location": '',
                    "competition": competition,
                    "link": link,
                    "tv": '',
                    "score1": score1,
                    "score2": score2
                    }
                }

                json_data[league].append(new_game)

    ncaa.quit()

if(league=='World Lacrosse'):
    world = webdriver.Chrome()
    world.get("https://www.worldlax2023.com/sports/mlax/2023-24/schedule")

    date = ''
    count = 0
    things = world.find_elements(By.CLASS_NAME, 'card.event-group.my-3')
    for thing in things:

        date = thing.find_element(By.CLASS_NAME, 'card-header.h5.text-white.bg-primary').text
        date = date[date.index(',')+1:date.index('202')-2]
        date = date.split(' ')
        month = date[1]
        day = date[2]

        bugs = thing.find_elements(By.CLASS_NAME, 'card-body')
        for bug in bugs:

            teams = bug.find_elements(By.CLASS_NAME,'text-uppercase')     
            team1 = teams[1].text.replace(' *','').replace(' ^','').replace(' ','-')
            team2 = teams[2].text.replace(' *','').replace(' ^','').replace(' ','-') 


            competition = bug.find_elements(By.CLASS_NAME,'text-muted.small')[1].text

            if(competition=='' or competition[0:]=='@'): competition = ''
            else:
                index = competition.index('@')
                competition = competition[0:index]
            if(competition.find('Game')>-1): competition = competition[0:competition.index('Game')+4]
            if(competition.find('GAME')>-1): competition = competition[0:competition.index('GAME')+4]

        
            try: link = bug.find_element(By.CLASS_NAME,'link').get_attribute('href')
            except: link = ""

            scores = bug.find_elements(By.CLASS_NAME,'col-auto')                                        
            score1 = scores[1].text.replace(' ','') 
            score2 = scores[3].text.replace(' ','')


            date = "2023-"
            if(month=='DECEMBER'): date="2022-01-"
            elif(month=="JANUARY"): date+="01-"
            elif(month=="Feb" or month=="02" or month=="FEBRUARY"): date+="02-"
            elif(month=="03" or month=="MARCH"): date+="03-"
            elif(month=="04" or month=="APRIL"): date+="04-"
            elif(month=="05" or month=="MAY"): date+="05-"
            elif(month=="Jun" or month=="JUNE" or month=="June"): date+="06-"
            elif(month=="Jul" or month=="July"): date+="07-"
            elif(month=="Aug"): date+="08-"
            elif(month=="Sept"): date+="09-"

            if(len(day)<2): date+="0"+day
            else: date+=day

            new_game = date+team1+team2

            new_game = {
                new_game: {
                "date": date,
                "time": '',
                "team1": team1,
                "team2": team2,
                "location": 'San Diego, CA',
                "competition": competition,
                "link": link,
                "tv": 'ESPN+',
                "score1": score1,
                "score2": score2
                }
            }

            json_data[league].append(new_game)

        
    world.quit()




if(league=='NLL'):

    nll = webdriver.Chrome()
    nll.get("https://www.nll.com/schedule/scores/")
    nll.implicitly_wait(20)

    d = ''

    count = 100
    things = nll.find_elements(By.CSS_SELECTOR, '.game_card.bg_light, .h3.month')
    for thing in things:
        if(thing.get_attribute('class')=='game_card bg_light'):

            teams = thing.find_elements(By.CLASS_NAME,'team_status.bold')
            team1 = teams[0].text 
            team2 = teams[1].text
            
            if(count>99):competition='Regular Season'
            elif(count==0 or count ==2): competition = "Eastern Conference Semifinal"  
            elif(count==1 or count == 3): competition = "Western Conference Semifinal"
            elif(count==4): competition = "Western Conference Final: Game 1"
            elif(count==5): competition = "Eastern Conference Final: Game 1"
            elif(count==6): competition = "Eastern Conference Final: Game 2"
            elif(count==7): competition = "Western Conference Final: Game 2"
            elif(count==8): competition = "Western Conference Final: Game 3"
            elif(count==9): competition = "Final: Game 1"
            elif(count==10): competition = "Final: Game 2"
            else: competition = "Final: Game 3"
            

            link= thing.find_element(By.CLASS_NAME,'button').get_attribute('href')                   
            scores = thing.find_element(By.TAG_NAME,'h2').text.replace('- ','')
            scores = scores.split(' ')
            score1 = scores[0]
            score2 = scores[1]
            
            count+=1       



            date = "2023-"
            if(month=='DECEMBER'): date="2022-01-"
            if(month=="JANUARY"): date+="01-"
            elif(month=="Feb" or month=="02" or month=="FEBRUARY"): date+="02-"
            elif(month=="03" or month=="MARCH"): date+="03-"
            elif(month=="04" or month=="APRIL"): date+="04-"
            elif(month=="05" or month=="MAY"): date+="05-"
            elif(month=="Jun" or month=="JUNE" or month=="June"): date+="06-"
            elif(month=="Jul" or month=="July"): date+="07-"
            elif(month=="Aug"): date+="08-"
            elif(month=="Sept"): date+="09-"
            if(len(day)<2): date+="0"+day
            else: date+=day

            new_game = date+team1+team2

            new_game = {
                new_game: {
                "date": date,
                "time": '',
                "team1": team1,
                "team2": team2,
                "location": team2,
                "competition": competition,
                "link": link,
                "tv": '',
                "score1": score1,
                "score2": score2
                }
            }

            json_data[league].append(new_game)

        else:
            fulldate = thing.text
            if(d != fulldate): d = fulldate[fulldate.index(',')+1:fulldate.index('202')-3]
            date = d.split(' ')
            month = date[1]
            day = date[2]

    nll.quit()





if(league=='MSL'):

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
        if(month=='DECEMBER'): date="2022-01-"
        if(month=="JANUARY"): date+="01-"
        elif(month=="Feb" or month=="02" or month=="FEBRUARY"): date+="02-"
        elif(month=="03" or month=="MARCH"): date+="03-"
        elif(month=="04" or month=="APRIL"): date+="04-"
        elif(month=="05" or month=="MAY"): date+="05-"
        elif(month=="Jun" or month=="JUNE" or month=="June"): date+="06-"
        elif(month=="Jul" or month=="July"): date+="07-"
        elif(month=="Aug"): date+="08-"
        elif(month=="Sept"): date+="09-"
        if(len(day)<3): date+="0"+day
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
            "competition": 'Regular Season',
            "link": link,
            "tv": '',
            "score1": '',
            "score2": ''
            }
        }

        json_data[league].append(new_game)

    msl.quit()
    







if(league=='WLA'):
    wla = webdriver.Chrome()
    wla.get("https://www.wlalacrosse.com/stats#/62/schedule?division_id=22538")
    timee.sleep(30)
    count = 0

    things = wla.find_element(By.CLASS_NAME,'table-scroll').find_element(By.TAG_NAME,'tbody').find_elements(By.CSS_SELECTOR, 'tr.ng-scope')
    for thing in things:
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
            "competition": 'Regular Season',
            "link": link,
            "tv": '',
            "score1": '',
            "score2": ''
            }
        }

        json_data[league].append(new_game)

    wla.quit()


with open('real-games.json', 'w') as file:
    json.dump(json_data, file, indent=4)

