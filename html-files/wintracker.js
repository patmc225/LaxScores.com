function track(team1,team2,score1,score2,leaguename,competition,time)
{
    console.log('jhello')
    fetch('Display.csv')
    .then(response => response.text())
    .then(csvData => {        
        stuff = csvData.replace(/\n/g,',')
        stuff = stuff.split(',')
        console.log('got csv')
    let s = []
    let string = ''
    for (i=0; i<team1.length; i++) 
    {
        if(competition[i].includes('Finals:')) 
        {
            console.log(competition[i])
            competition[i] = 'Finals'
        }
        
        if(s.includes(team1[i]+'$'+leaguename[i]+'$'+competition[i])==false && score1[i]!='' && team1[i]!='TBD'&& team1[i]!='N/A' && !competition[i].includes('Placement Game') && !competition[i].includes('Out Of Conference Play') && (!leaguename[i].includes('NCAA') || competition[i].includes('Conference')) ) 
        {
            let t = team1[i]+'$'+leaguename[i]+'$'+competition[i]
           // let t2 = team2[i]+'$'+leaguename[i]+'$'+competition[i]
            s.push(t,0,0,0,0)
            if(leaguename[i].includes('NCAA')) s.push(0,0,0,0)
            //s.push(t2,0,0,0,0)
            //if(leaguename[i].includes('NCAA')) s.push(0,0,0,0)
        }
    }
    for (i=0; i<team1.length; i++) 
    {
       
        if((s.indexOf(team1[i]+'$'+leaguename[i]+'$'+competition[i])>-1 && score1[i]!='' && s.indexOf(team2[i]+'$'+leaguename[i]+'$'+competition[i])>-1) && score1[i]!=undefined && !time[i].includes('Live'))
        {
            let t1 = s.indexOf(team1[i]+'$'+leaguename[i]+'$'+competition[i])
            let t2 = s.indexOf(team2[i]+'$'+leaguename[i]+'$'+competition[i])
            if(t1>-1 && t2>-1)
            {
                if(parseInt(score1[i])>parseInt(score2[i]))
                { 
                    s[t1+1]+=1
                    s[t2+2]+=1
                }
                else if (parseInt(score1[i])<parseInt(score2[i]))
                {
                    s[t1+2]+=1
                    s[t2+1]+=1
                }
                s[t1+3]+=parseInt(score1[i])
                s[t1+4]+=parseInt(score2[i])
                s[t2+3]+=parseInt(score2[i])
                s[t2+4]+=parseInt(score1[i])
            }

        }
        else if(competition[i].includes('Out Of Conference Play')||(leaguename[i].includes('NCAA') && !competition[i].includes('Conference') ))
        {
            for(j=0;j<s.length;j++) if(typeof s[j] != 'number')  if(s[j].includes(team1[i]+ '$' +leaguename[i])) t1 = j  
         
            for(j=0;j<s.length;j++) if(typeof s[j] != 'number') if(s[j].includes(team2[i]+ '$' +leaguename[i])) t2 = j

            if(t1>-1 && t2>-1)
            {
                if(parseInt(score1[i])>parseInt(score2[i]))  
                {
                    s[t1+5]+=1
                    s[t2+6]+=1
                }       
                else if (parseInt(score1[i])<parseInt(score2[i]))   
                {
                    s[t1+6]+=1
                    s[t2+5]+=1
                }   
                s[t1+7] += parseInt(score1[i])
                s[t1+8] += parseInt(score2[i])  
                s[t2+7] += parseInt(score2[i])
                s[t2+8] += parseInt(score1[i])
            }
                
            t1 = -1
            t2 = -1
         }

     }
    

    for (i=0; i<s.length; i++)
    {
        
        if(s[i].includes('NLL') && s[i].includes('Regular'))
        { 
            index = stuff.indexOf( s[i].substring( 0, s[i].indexOf('$') ) )                    
            s[i] = s[i].substring(0,s[i].indexOf('NLL')) + 'NLL ' + stuff[index+4] + '$Regular Season'
            
        }
        string+=s[i]+'$'+s[i+1]+'$'+s[i+2]+'$'+s[i+3]+'$'+s[i+4]
        

        if(s[i].includes('NCAA'))
        {
            string+='$'+s[i+5]+'$'+s[i+6]+'$'+s[i+7]+'$'+s[i+8]
            i+=4
        }
        string+='#'
        i+=4
    }
    console.log('setting key')
    localStorage.setItem('key',string)
    console.log('set key')
    })}