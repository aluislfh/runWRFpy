import os
import sys
import datetime as dt

#-------------------------------------------------------------------------------
# Script para generar datos diarios
#-------------------------------------------------------------------------------


def start():

    wdir = '/home/adrian/WRF/run_erai/makeOBS/'
    datadir = '/home/adrian/NAS/Data/knudgin/'

    obs_upper = 'OBS:'           # OBS:2014010300
    obs_sfc   = 'SURFACE_OBS:'   # SURFACE_OBS:2010030912

    date = dt.datetime(2009,1,1,0)
    date2 = dt.datetime(2019,9,1,0)

    for i in range(31*12*10+31*8): # 10 anos y 8 meses 

        dates=str(date).split()
        dates=str(dates[0] + '_' + dates[1])
        
        YYYY0 = str(dates[0:4])
        MM0   = str(dates[5:7])
        DD0   = str(dates[8:10])
        HH0   = str(dates[11:13])

        daily_upper = []
        daily_upper.append(datadir+obs_upper+YYYY0+MM0+DD0+HH0)

        daily_sfc = []
        daily_sfc.append(datadir+obs_sfc+YYYY0+MM0+DD0+HH0)

        date1 = date

        for i in range(4): # 10 anos y 6 meses 

            date1 = date1 + dt.timedelta(hours=6)

            dates1=str(date1).split()
            dates1=str(dates1[0] + '_' + dates1[1])
            
            YYYY1 = str(dates1[0:4])
            MM1   = str(dates1[5:7])
            DD1   = str(dates1[8:10])
            HH1   = str(dates1[11:13])

            daily_upper.append(datadir+obs_upper+YYYY1+MM1+DD1+HH1)
            daily_sfc.append(datadir+obs_sfc+YYYY1+MM1+DD1+HH1)


        # Concatenando
        main(daily_upper,daily_sfc,wdir,datadir,YYYY0+MM0+DD0+HH0)

        date += dt.timedelta(hours=24)
        date1 = date + dt.timedelta(hours=24)


        if date == date2:
            break


def main(daily_upper,daily_sfc,wdir,datadir,fdate):

    print('load data from --> '+str(fdate))

    os.chdir(wdir)

    command = 'cat '
    for udata,sdata in zip(daily_upper,daily_sfc):
#        print(fdate,udata,sdata)

        command = command + udata + ' ' + sdata + ' '

    command = command + '> obs_data_'+fdate+'.ltr'


#    # concatenando
#    print(command)
    os.system(command)

#    # convirtiendo de little-r a formato nudging
    os.system('perl ./RT_fdda_reformat_obsnud.pl obs_data_'+fdate+'.ltr')



if __name__=='__main__':
    start()

