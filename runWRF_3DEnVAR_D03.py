import os
import sys
import fnmatch
import datetime as dt
import numpy as np

#---------------------------------------------------------------------------------------------
# Runing WRF model
#---------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Script para correr el modelo WRF
#-------------------------------------------------------------------------------

def start():

    main('2018-12-05_12:00:00', '2018-12-06_12:00:00', str('201812050600'), '12')
    main('2018-12-09_12:00:00', '2018-12-10_12:00:00', str('201812090600'), '12')
    main('2018-12-10_00:00:00', '2018-12-11_00:00:00', str('201812091800'), '00')
    main('2018-12-10_12:00:00', '2018-12-11_12:00:00', str('201812100600'), '12')

##    main('2019-09-19_18:00:00', '2019-09-20_18:00:00', str('201909191200'), '12')
#    main('2019-10-24_00:00:00', '2019-10-25_00:00:00', str('201910231800'), '00')
#    main('2019-01-28_00:00:00', '2019-01-28_03:00:00', str('201901271800'), '00')




def main(sdates, edates, gfsdir, init):

    sYYYY = str(sdates[0:4])
    sMM   = str(sdates[5:7])
    sDD   = str(sdates[8:10])
    sHH   = str(sdates[11:13])

    eYYYY = str(edates[0:4])
    eMM   = str(edates[5:7])
    eDD   = str(edates[8:10])
    eHH   = str(edates[11:13])

    # Namelist del nucleo atmosferico del modelo
    fname_wrf = 'namelist.input'

    # Namelist del WPS del modelo WRF
    fname_wps = 'namelist.wps'

    # Definiendo directorios a usar
    WPSDIR   = '/home/adrian/WRF/WPS-4.1'
    WRFDIR   = '/home/adrian/WRF/WRF3.8.1'
    WRFDADIR    = '/home/adrian/WRF/WRF_4.3/WRFDA-CVCLOUD/WRF-4.3' # '/home/adrian/WRF/WRF_v3.8.1/WRFDA'
    DATA_GRB = '/media/adrian/hdd_glm/PHD_runs/GFS/'+gfsdir
    RDIR     = '/media/adrian/hdd_glm/PHD_runs/RUNS_3DEnVAR/D03'
    RUN_DIR  = RDIR+'/'+sYYYY+sMM+sDD+sHH

    RUN_DIR1  = '/media/adrian/hdd_glm/PHD_runs/RUNS_3DEnVAR/D01/'+sYYYY+sMM+sDD+sHH
    GEOG_dir  = '/home/adrian/WRF/WPS_GEOG/'

    DA_OPT = 'activado'   # 'activado' / 'desactivado'
    OBS_DATA = '/media/adrian/hdd_glm/PHD_runs/OBS/PREPBUFR'

    genbe = '/media/adrian/hdd_glm/PHD_runs/GenBE'
    ENS_DIR = '/media/adrian/hdd_glm/PHD_runs/RUNS_3DEnVAR/EnsData'

    # Namelist del wrfda
    fname_wrfda   = 'namelist.wrfda'

    # Namelist del update_bc
    fname_wrfdabc = 'parame.in'

    # Namelist del obsproc
    fname_obsproc = 'namelist.obsproc'


    # Parametros del namelist 1 (nwmelist.wps, namelist.input real.exe, ndown.exe)
    NDOM=2
    DX1=9000
    DX2=3000
    DX3=0
    DNX1=199
    DNY1=112
    DNX2=412
    DNY2=184
    DNX3=0
    DNY3=0
    PX21=30
    PY21=21
    PX32=0
    PY32=0

    # Parametros del namelist 2 (namelist.input wrf.exe)
    NNDOM=1
    NDX1=3000
    NDX2=0
    NDNX1=412
    NDNY1=184
    NDNX2=0
    NDNY2=0
    NPX21=0
    NPY21=0

    # Linkeando ficheros necesarios para el WPS

    cmd = 'mkdir -p ' + RUN_DIR
    os.system(cmd)
    cmd = 'mkdir -p ' + RUN_DIR + '/metgrid'
    os.system(cmd)
    cmd = 'mkdir -p ' + RUN_DIR + '/geogrid'
    os.system(cmd)
    cmd = 'mkdir -p ' + RUN_DIR + '/outputs'
    os.system(cmd)

    cmd = 'cp -u ' + WPSDIR + '/geogrid/GEOGRID.TBL ' + RUN_DIR + '/geogrid/'
    os.system(cmd)
    cmd = 'cp -u ' + WPSDIR + '/metgrid/METGRID.TBL ' + RUN_DIR + '/metgrid/'
    os.system(cmd)
#            cmd = 'cp -f ' + WPSDIR + '/ungrib/Variable_Tables/Vtable.GFS '+ RUN_DIR + '/Vtable'
    cmd = 'cp -f '+RDIR+'/Vtable.GFS '+ RUN_DIR + '/Vtable'  # Vtable viejo para 2014
    os.system(cmd)
    cmd = 'cp -u ' + WPSDIR + '/link_grib.csh ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WPSDIR + '/geogrid/src/geogrid.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WPSDIR + '/ungrib/src/ungrib.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WPSDIR + '/metgrid/src/metgrid.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WPSDIR + '/util/src/mod_levs.exe ' + RUN_DIR
    os.system(cmd)

    # Linkeando ficheros necesarios para el WRF
    cmd = 'ln -sf ' + WRFDIR + '/main/wrf.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/main/real.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/main/ndown.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/GENPARM.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/grib2map.tbl ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/LANDUSE.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/MPTABLE.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/SOILPARM.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/URBPARM.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/URBPARM_UZE.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/VEGPARM.TBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/RRTM_DATA ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/RRTM_DATA_DBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/RRTMG_LW_DATA ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/RRTMG_LW_DATA_DBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/RRTMG_SW_DATA ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/RRTMG_SW_DATA_DBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/tr49t67 ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/tr49t85 ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/tr67t85 ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/CAM_ABS_DATA ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/CAM_AEROPT_DATA ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA_DBL ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/co2_trans ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA.expanded_rain ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA.expanded_rain_DBL ' + RUN_DIR
    os.system(cmd)


    # Linkeando ficheros necesarios para el WRFDA

    cmd = 'ln -sf ' + WRFDADIR + '/run/LANDUSE.TBL ' + RUN_DIR

    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/run/radiance_info ' + RUN_DIR + '/.'
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/run/crtm_coeffs ' + RUN_DIR + '/.'
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/run/be.dat.cv3 ' + RUN_DIR + '/be.dat'
#            os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/obsproc/obserr.txt ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/run/VARBC.in ' + RUN_DIR
    os.system(cmd)

    cmd = 'ln -sf ' + WRFDADIR + '/var/build/da_wrfvar.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/build/da_update_bc.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/build/gen_be_stage0_wrf.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/build/da_advance_time.exe ' + RUN_DIR
    os.system(cmd)

    cmd = 'ln -sf ' + WRFDADIR + '/var/obsproc/src/obsproc.exe ' + RUN_DIR
    os.system(cmd)


    cmd = 'ln -sf ' + WRFDADIR + '/var/build/gen_be_ensmean.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/build/gen_be_ep2.exe ' + RUN_DIR
    os.system(cmd)
    cmd = 'ln -sf ' + WRFDADIR + '/var/build/gen_be_vertloc.exe ' + RUN_DIR
    os.system(cmd)


    # Ubicandonos en el directorio de corridas
    cmd = 'mkdir -p ' + RUN_DIR
    os.system(cmd)
    os.chdir(RUN_DIR)


    #-----------------------------------------------------------------------------
    # Corriendo por todos los elementos del array 'sdates'
    # Este array es util para lanzar mas de una corrida
    #-----------------------------------------------------------------------------

    #----------------------
    # runing WPS from WRF model
    #----------------------

    #eliminando namelist viejos
    cmd = 'rm -f namelist.wps'
    os.system(cmd)

    #write wps namelist    
    f = open(fname_wps,'w')
    s = namelist_wps(sdates, edates, NDOM, GEOG_dir, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, RDIR)
    f.write(s)
    f.close()

    #borrando ficheros viejos
    cmd = 'rm -f WPS:* GRIBFILE* PFILE*'
    os.system(cmd)


    #----------------------
    # runing WPS GFS LINKS
    #----------------------

    try:
        grbfile1  = 'gfs.t*z.pgrb2full.0p50.f*'
    except:
        grbfile1  = 'gfs.t*z.pgrb2.0p25.f*'


    os.system("ln -sf " + DATA_GRB + '/' + grbfile1 + " " + RUN_DIR)


    # Linkeando ficheros
    cmd = 'csh ' + RUN_DIR + '/link_grib.csh ' + RUN_DIR + '/' + grbfile1
    os.system(cmd)


    #----------------------
    # runing WPS UNGRID
    #----------------------

    cmd = './ungrib.exe'
    os.system(cmd)

    #----------------------
    # runing WPS GEOGRID
    #----------------------

    #generate initial data with ungrib.exe
    if not os.path.exists(RDIR+'/geo_em.d01.nc'):
        cmd = 'mpirun -np 8 ./geogrid.exe'
        os.system(cmd)

    #----------------------
    # runing WPS METGRID
    #----------------------
    
    #generate initial data with metgrid.exe
    cmd = 'mpirun -np 8 ./metgrid.exe'
    os.system(cmd)

    #----------------------
    # runing WRF model
    #----------------------

    # Eliminando namelist viejos
    cmd = 'rm -f namelist.input'
    os.system(cmd)

    #---------------------------
    # Run real.exe
    #---------------------------

    #write init namelist    
    f = open(fname_wrf,'w')
    s = namelist_wrf(sdates, edates, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, 10800)
    f.write(s)
    f.close()

    cmd = 'mpirun -np 8 ./real.exe'
    os.system(cmd)

    cmd = 'mv rsl.error.0000 real.rsl.error.0000'
    os.system(cmd)
    cmd = 'mv rsl.out.0000 real.rsl.out.0000'
    os.system(cmd)
    cmd = 'mv -f wrfinput_d02 wrfndi_d02'
    os.system(cmd)


    #----------------------
    # run NDOWN.EXE
    #----------------------

    #write init namelist    (ndown.exe)
    f = open(fname_wrf,'w')
    s = namelist_wrf(sdates, edates, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, 10800)
    f.write(s)
    f.close()

    cmd = 'ln -sf ' + RUN_DIR1 + '/wrfout_d02_* ' + RUN_DIR + '/.'
    os.system(cmd)

    #renombrador d ficheros
    wrfouts=[]
    for files in os.listdir('./'):
        if fnmatch.fnmatch(files,'wrfout_d02_*'):
            wrfouts.append(files)
    for wf in wrfouts:
        wfsp=wf.split('_')
        print(wf + ' ' + wfsp[0] + '_d01_' + wfsp[2] + '_' + wfsp[3])
        cmd='mv ' + wf + ' ' + wfsp[0] + '_d01_' + wfsp[2] + '_' + wfsp[3]
        os.system(cmd)

    cmd = 'mpirun -np 8 ./ndown.exe'
    os.system(cmd)

    cmd = 'mv rsl.error.0000 ndown.rsl.error.0000'
    os.system(cmd)
    cmd = 'mv rsl.out.0000 ndown.rsl.out.0000'
    os.system(cmd)

    cmd = 'rm -f wrfbdy_d01'
    os.system(cmd)
    cmd = 'rm -f wrfinput_d01'
    os.system(cmd)
    cmd = 'mv -f wrfbdy_d02 wrfbdy_d01'
    os.system(cmd)
    cmd = 'mv -f wrfinput_d02 wrfinput_d01'
    os.system(cmd)
    #cmd = 'mv -f wrfinput_d03 wrfinput_d02'
    #os.system(cmd)

    cmd = 'rm -f wrfout*'
    os.system(cmd)

    cmd = 'rm -f wrfndi_d02'
    os.system(cmd)

    # Eliminando namelist viejos
    cmd = 'mv namelist.input namelist.input.1'
    os.system(cmd)

    #write init namelist    (wrf.exe)
    f = open(fname_wrf,'w')
    s = namelist_wrf(sdates, edates, NNDOM, NDX1, NDX2, NDX2, NDNX1, NDNY1, NDNX2, NDNY2, NDNX2, NDNY2, NPX21, NPY21, NPX21, NPY21, 10800)
    f.write(s)
    f.close()

    #---------------------------
    # Run WRFDA
    #---------------------------

    if DA_OPT == 'activado':
        print('Ejecutando WRFDA ... ')


        # Linkeando ficheros de observaciones

        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.1bamua.tm00.bufr_d ./amsua.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.1bhrs4.tm00.bufr_d ./hirs4.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.1bmhs.tm00.bufr_d  ./mhs.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.airsev.tm00.bufr_d ./airs.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.mtiasi.tm00.bufr_d ./iasi.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.atms.tm00.bufr_d ./atms.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.sevcsr.tm00.bufr_d ./seviri.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.ssmisu.tm00.bufr_d ./ssmis.bufr'
        os.system(cmd)

        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.prepbufr.nr ./ob.bufr '
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/gdas.t'+sHH+'z.gpsro.tm00.bufr_d ./gpsro.bufr'
        os.system(cmd)
        cmd = 'ln -sf '+OBS_DATA+'/'+sYYYY+sMM+sDD+'/'+sYYYY[2:]+sMM+sDD+sHH+'_multi_ob.radar ./ob.radar'
        os.system(cmd)

        cmd = 'mv namelist.input namelist.wrf'
        os.system(cmd)

        # runing wrfvar for domain 1


        EnsDates = np.loadtxt(ENS_DIR+'/table.txt',dtype='str',skiprows=1)

        fdates = []
        bedat = ''
        for dd in range(len(EnsDates[:,0])):
            if EnsDates[dd,0] == sYYYY+sMM+sDD+sHH:
                fdates.append(EnsDates[dd,1])
                fdates.append(EnsDates[dd,2])
                fdates.append(EnsDates[dd,3])
                fdates.append(EnsDates[dd,4])
                bedat = EnsDates[dd,5]

        os.system('ln -sf '+ENS_DIR+'/'+sYYYY+sMM+sDD+sHH+'/'+fdates[0]+'/wrfout_d03_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00 '+RUN_DIR+'/wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00.e001')
        os.system('ln -sf '+ENS_DIR+'/'+sYYYY+sMM+sDD+sHH+'/'+fdates[1]+'/wrfout_d03_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00 '+RUN_DIR+'/wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00.e002')
        os.system('ln -sf '+ENS_DIR+'/'+sYYYY+sMM+sDD+sHH+'/'+fdates[2]+'/wrfout_d03_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00 '+RUN_DIR+'/wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00.e003')
        os.system('ln -sf '+ENS_DIR+'/'+sYYYY+sMM+sDD+sHH+'/'+fdates[3]+'/wrfout_d03_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00 '+RUN_DIR+'/wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00.e004')

        os.system('cp -vf '+ENS_DIR+'/'+sYYYY+sMM+sDD+sHH+'/'+fdates[3]+'/wrfout_d03_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00 '+RUN_DIR+'/wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00.mean')
        os.system('cp -vf '+ENS_DIR+'/'+sYYYY+sMM+sDD+sHH+'/'+fdates[3]+'/wrfout_d03_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00 '+RUN_DIR+'/wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00.vari')

        f = open('gen_be_ensmean_nl.nl','w')
        s = ensmean_nl(RUN_DIR, 'wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00')
        f.write(s)
        f.close()

        os.system('./gen_be_ensmean.exe')

        os.system('mkdir -p '+RUN_DIR+'/ep')
        os.system('cp -f '+RUN_DIR+'/gen_be_ep2.exe '+RUN_DIR+'/ep')

        os.chdir(RUN_DIR+'/ep')
        os.system('./gen_be_ep2.exe '+sYYYY+sMM+sDD+sHH+' 4 . ../wrfout_d01_'+sYYYY+'-'+sMM+'-'+sDD+'_'+sHH+':00:00')
        os.chdir(RUN_DIR)

        os.system('./gen_be_vertloc.exe 28')





        cmd = 'rm -f namelist.wrfda'
        os.system(cmd)

        e_we=412
        e_sn=184
        e_vert=28 #30
        dx=3000
        dy=3000
        radio='60.0'

        cmd = 'cp -vf '+genbe+'/'+bedat+'_d03 '+ RUN_DIR + '/be.dat'
        os.system(cmd)

        f = open(fname_wrfda,'w')
        s = namelist_wrfda(e_we, e_sn, e_vert, dx, dy, radio, sdates, edates)
        f.write(s)
        f.close()

        cmd = 'ln -sf namelist.wrfda namelist.input'
        os.system(cmd)
        cmd = 'ln -sf wrfinput_d01 fg'
        os.system(cmd)

        #--------
        cmd = './da_wrfvar.exe'
        os.system(cmd)

        cmd = 'mv rsl.out.0000 wfrvar1_rsl.out.0000'
        os.system(cmd)
        cmd = 'mv wrfinput_d01 wrfinput_d01.old' 
        os.system(cmd)
        cmd = 'mv wrfvar_output wrfinput_d01'
        os.system(cmd)
        #--------

        # runing update_bc

        cmd = 'rm -f parame.in'
        os.system(cmd)

        f = open(fname_wrfdabc,'w')
        s = namelist_wrfdabc()
        f.write(s)
        f.close()

        #--------
        cmd = './da_update_bc.exe'
        os.system(cmd)
        #--------

        # Restableciendo el namelist del WRF
        cmd = 'rm -f namelist.input'
        os.system(cmd)
        cmd = 'mv namelist.wrf namelist.input'
        os.system(cmd)

    #---------------------------
    # Run wrf.exe
    #---------------------------

    # Parallel
    cmd = 'mpirun -np 8 ./wrf.exe'
    os.system(cmd)

    # Eliminando ficheros viejos
    cmd = 'rm -f met_em* PFILE* FILE*'
#    os.system(cmd)



# REAL & WRF


def ensmean_nl(rundir,wfile):

  s='''  &gen_be_ensmean_nl
    directory = '{0}'
    filename = '{1}'
    num_members = 4,
    nv = 7
    cv = 'U', 'V', 'W', 'PH', 'T', 'MU', 'QVAPOR' /
'''.format(rundir,wfile)

  return s


def namelist_wrf(startTime, endTime, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, NINT):

  YYYY0 = str(startTime[0:4])
  MM0   = str(startTime[5:7])
  DD0   = str(startTime[8:10])
  HH0   = str(startTime[11:13])

  YYYY1 = str(endTime[0:4])
  MM1   = str(endTime[5:7])
  DD1   = str(endTime[8:10])
  HH1   = str(endTime[11:13])

# auxinput4_inname = "wrflowinp_d<domain>",
# auxinput4_interval = 360,
# io_form_auxinput4 = 2

  s = '''&time_control
 run_days                            = 0,
 run_hours                           = 24,
 run_minutes                         = 0,
 run_seconds                         = 0,
 start_year                          = {0}, {0}, {0},
 start_month                         = {1}, {1}, {1},
 start_day                           = {2}, {2}, {2},
 start_hour                          = {3}, {3}, {3},
 start_minute                        = 00,   00,   00,
 start_second                        = 00,   00,   00,
 end_year                            = {4}, {4}, {4},
 end_month                           = {5}, {5}, {5},
 end_day                             = {6}, {6}, {6},
 end_hour                            = {7}, {7}, {7},
 end_minute                          = 00,   00,   00,
 end_second                          = 00,   00,   00, 
 interval_seconds                    = 10800,
 input_from_file                     = .true.,.true.,.true.,
 history_interval                    = 60,  60,  60,  60, 60,
 frames_per_outfile                  = 1, 1, 1, 1, 1,
 restart                             = .false.,
 restart_interval                    = 10800,
 io_form_history                     = 2,
 io_form_restart                     = 2,
 io_form_input                       = 2,
 io_form_boundary                    = 2,
 io_form_auxinput2                   = 2,
 debug_level                         = 0,
! force_use_old_data                  = .true.,
 /

 &domains
 time_step                           = 18,
 time_step_fract_num                 = 0,
 time_step_fract_den                 = 1,
 use_adaptive_time_step              = .true.
 step_to_output_time                 = .true.
 starting_time_step                  = 18,
 max_time_step                       = 36,
max_dom                  = {8},
e_we                     = {12},  {14}, {16},
e_sn                     = {13},  {15}, {17},
 e_vert                              = 28,  28,  28,
! e_vert                              =  30,  30,  30,  
 p_top_requested                     = 10000, 
 num_metgrid_levels                  = 48,
 num_metgrid_soil_levels  = 4,
dx                       = {9}, {10}, {11},
dy                       = {9}, {10}, {11},
grid_id                  = 1,       2,   3,
parent_id                = 1,       1,   2,
i_parent_start           = 1,     {18},  {20},
j_parent_start           = 1,     {19},  {21},
parent_grid_ratio        = 1,       3,    3,
parent_time_step_ratio   = 1,       3,    3,
 feedback                 = 1,
 smooth_option            = 0,
 /

 &physics
 mp_physics                          = 10,   10,   10,
 ra_lw_physics                       = 1,     1,     1,
 ra_sw_physics                       = 2,     2,     2,
 radt                                = 3,     3,     3,
 sf_sfclay_physics                   = 2,     2,     2,
 sf_surface_physics                  = 2,     2,     2,
 bl_pbl_physics                      = 5,     5,     5,
 bldt                                = 0,     0,     0,
 cu_physics                          = 0,     0,     0,
 cudt                                = 0,     0,     0,
 isfflx                              = 1,
 ifsnow                              = 0,
 icloud                              = 1,
 surface_input_source                = 1,
 num_soil_layers                     = 4,
 sf_urban_physics                    = 0,     0,     0,
 sst_update                          = 0,
 tmn_update                          = 0,
 sst_skin                            = 0,
 maxiens                             = 1,
 maxens                              = 3,
 maxens2                             = 3,
 maxens3                             = 16,
 ensdim                              = 144,
 do_radar_ref = 1,
 /

 &fdda
 /

 &dynamics
 w_damping                           = 1,
 diff_opt                            = 1,
 km_opt                              = 4,
 diff_6th_opt                        = 0,      0,      0,
 diff_6th_factor                     = 0.12,   0.12,   0.12,
 base_temp                           = 290.
 damp_opt                            = 3,
 zdamp                               = 5000.,  5000.,  5000.,
 dampcoef                            = 0.2,    0.2,    0.2
 khdif                               = 0,      0,      0,
 kvdif                               = 0,      0,      0,
 non_hydrostatic                     = .true., .true., .true.,
 moist_adv_opt                       = 1,      1,      1,     
 scalar_adv_opt                      = 1,      1,      1,     
! etac                                = 0.100000001
 /

 &bdy_control
 spec_bdy_width                      = 5,
 spec_zone                           = 1,
 relax_zone                          = 4,
 specified                           = .true., .false.,.false.,
 nested                              = .false., .true., .true.,
 /

 &grib2
 /

 &namelist_quilt
 nio_tasks_per_group = 0,
 nio_groups = 1,
 /

'''.format(YYYY0, MM0, DD0, HH0, YYYY1, MM1, DD1, HH1, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, NINT)

# do_radar_ref = 1,
# lightning_option = {24}, {24}, {24},
# lightning_dt = 45, 45, 45,
# lightning_start_seconds = 600, 600, 600,
# flashrate_factor = 1.0, 1.0, 1.0,
# cellcount_method = 0, 0, 0,
# iccg_method = 3, 3, 3,
# iccg_prescribed_num = 0.,
# iccg_prescribed_den = 1.,
# NUM_LAND_CAT = 21,

# w_damping                           = 0,
# damp_opt                            = 0,

  return s



# WPS
def namelist_wps(startTime, endTime, NDOM, GEOG_dir, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, RDIR):

  s = '''&share
 wrf_core = 'ARW',
 max_dom = {2},
 start_date = '{0}','{0}','{0}',
 end_date   = '{1}','{1}','{1}',
 interval_seconds = 10800,
 opt_output_from_geogrid_path = '{17}'
 io_form_geogrid = 2,
 debug_level = 1000,
/

&geogrid
 parent_id         = 1, 1, 2,
 parent_grid_ratio = 1, 3, 3,
 i_parent_start    = 1, {13}, {15},
 j_parent_start    = 1, {14}, {16},
 e_we          = {7}, {9}, {11},
 e_sn          = {8}, {10}, {12},
 geog_data_res = '30s','30s','30s',
 dx = {4},
 dy = {4},
 map_proj =  'mercator',
 ref_lat   = 22.229,
 ref_lon   = -79.61004,
 truelat1  = 22.229,
 truelat2  = 0,
 stand_lon = -79.61004, 
 geog_data_path = '{3}',
/

&ungrib
 out_format = 'WPS',
 prefix = 'FILE',
/

&metgrid
 fg_name = 'FILE'
 io_form_metgrid = 2, 
/

'''.format(startTime, endTime, NDOM, GEOG_dir, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, RDIR)


  return s


def namelist_wrfdabc():

  s = '''&control_param
da_file            = './wrfinput_d01'
wrf_bdy_file       = './wrfbdy_d01'
domain_id          = 1
debug              = .true.
update_lateral_bdy = .true.
update_low_bdy     = .false.
update_lsm         = .false.
iswater            = 16
var4d_lbc          = .false.
/
'''

  return s


def namelist_wrfda(e_we, e_sn, e_vert, dx, dy, radio,sdates, edates):

    YYYY0 = str(sdates[0:4])
    MM0   = str(sdates[5:7])
    DD0   = str(sdates[8:10])
    HH0   = str(sdates[11:13])

    YYYY1 = str(edates[0:4])
    MM1   = str(edates[5:7])
    DD1   = str(edates[8:10])
    HH1   = str(edates[11:13])


    date = dt.datetime(int(YYYY0),int(MM0),int(DD0),int(HH0))
    date2 = date - dt.timedelta(hours=1)
    date3 = date + dt.timedelta(hours=1)

    dates=str(date2).split()
    dates=str(dates[0] + '_' + dates[1]) # hora inicial
    DHH2   = str(dates[0:13])

    dates=str(date3).split()
    dates=str(dates[0] + '_' + dates[1]) # hora inicial
    DHH3   = str(dates[0:13])

# 
# update_sfc_diags=true,
#
    s = '''&wrfvar1
UPDATE_SFCDIAGS=true,
/
&wrfvar2
calc_w_increment=true, 
/
&wrfvar3
num_fgat_time = 1,
ob_format=1,
ob_format_gpsro=1,
/
&wrfvar4
use_radarobs = .true.,
use_radar_rv = .true.,
use_radar_rf = .false.,
use_radar_rhv = .true.,
use_radar_rqv = .true.,
use_amsuaobs = .true.,
use_atmsobs  = .true.,
use_mhsobs   = .true.,
!use_hirs4obs = .false.,
use_ssmisobs = .true.,
!use_airsobs  = .true.,
!use_iasiobs = .true.,
!use_seviriobs = .true.,
/
&wrfvar5
check_max_iv=true,
max_omb_spd=14.0,
max_omb_dir=135.0,
max_error_spd=5.0,
max_error_dir=5.0,
/
&wrfvar6
max_ext_its=3,
ntmax=200,
eps=0.001,
orthonorm_gradient=true,
/
&wrfvar7
cv_options=7,
cloud_cv_options=2,
use_cv_w = true,
var_scaling1 = 1.0, 0.5, 0.25,
var_scaling2 = 1.0, 0.5, 0.25,
var_scaling3 = 1.0, 0.5, 0.25,
var_scaling4 = 1.0, 0.5, 0.25,
var_scaling5 = 1.0, 0.5, 0.25,
var_scaling6 = 1.0, 0.5, 0.25,
var_scaling7 = 1.0, 0.5, 0.25,
var_scaling8 = 1.0, 0.5, 0.25,
var_scaling9 = 1.0, 0.5, 0.25,
var_scaling10 = 1.0, 0.5, 0.25,
var_scaling11 = 1.0, 0.5, 0.25,
len_scaling1 = 1.0, 0.5, 0.2,
len_scaling2 = 1.0, 0.5, 0.2,
len_scaling3 = 1.0, 0.5, 0.2,
len_scaling4 = 1.0, 0.5, 0.2,
len_scaling5 = 1.0, 0.5, 0.2,
len_scaling6 = 1.0, 0.5, 0.2,
len_scaling7 = 1.0, 0.5, 0.2,
len_scaling8 = 1.0, 0.5, 0.2,
len_scaling9 = 1.0, 0.5, 0.2,
len_scaling10 = 1.0, 0.5, 0.2,
len_scaling11 = 1.0, 0.5, 0.2,
je_factor=1.33,
/
&wrfvar8
/
&wrfvar9
trace_use=false
/
&wrfvar10
test_transforms=false,
test_gradient=false,
/
&wrfvar11
cv_options_hum=1
check_rh=1
sfc_assi_options=1
!psfc_from_slp = .false.
calculate_cg_cost_fn=.true.
/
&wrfvar12
/
&wrfvar13
/
&wrfvar14
rtminit_nsensor=8,
rtminit_platform=1,1,1,1,17,1,1,2,
rtminit_satid=15,16,18,19,0,18,19,16,
rtminit_sensor=3,3,3,3,19,15,15,10,
thinning_mesh=20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,
thinning=true,
qc_rad=true,
write_iv_rad_ascii=true,
write_oa_rad_ascii=true,
rtm_option=2,
only_sea_rad=false,
crtm_coef_path="/home/adrian/WRF/crtm_coeffs_2.3.0"
/
&wrfvar15
/
&wrfvar16
ensdim_alpha = 4
alphacv_method = 2
alpha_corr_type= 3
alpha_corr_scale = 500.0
!alpha_std_dev=1.000
!alpha_vertloc = .true.
/
&wrfvar17
/
&wrfvar18
 analysis_date="{6}-{7}-{8}_{9}:00:00.0000",
/
&wrfvar19
/
&wrfvar20
/
&wrfvar21
 time_window_min="{10}:00:00.0000",
/
&wrfvar22
 time_window_max="{11}:00:00.0000",
/
&wrfvar23
/
&time_control
 start_year={6},
 start_month={7},
 start_day={8},
 start_hour={9},
 end_year={12},
 end_month={13},
 end_day={14},
 end_hour={9},
 force_use_old_data=.true.,
/
&fdda
/
&domains
 e_we={0},
 e_sn={1},
 e_vert={2},
 dx={3},
 dy={4},
 auto_levels_opt = 1,
/
&dfi_control
/
&tc
/
&physics
 mp_physics=10,
 ra_lw_physics=1,
 ra_sw_physics=2,
 radt=3,
 sf_sfclay_physics=2,
 sf_surface_physics=2,
 bl_pbl_physics=5,
 cu_physics=0,
 cudt=0,
 num_soil_layers=4,
 mp_zero_out=2,
 co2tf=0,
/
&scm
/
&dynamics
 hybrid_opt  = 0,
 use_theta_m = 0,
 w_damping                           = 1,
 diff_opt                            = 1,
 km_opt                              = 4,
 diff_6th_opt                        = 0,      0,      0,
 diff_6th_factor                     = 0.12,   0.12,   0.12,
 base_temp                           = 290.
 damp_opt                            = 3,
 zdamp                               = 5000.,  5000.,  5000.,
 dampcoef                            = 0.2,    0.2,    0.2
 khdif                               = 0,      0,      0,
 kvdif                               = 0,      0,      0,
 non_hydrostatic                     = .true., .true., .true.,
 moist_adv_opt                       = 1,      1,      1,     
 scalar_adv_opt                      = 1,      1,      1,     
! etac                                = 0.100000001
/
&bdy_control
/
&grib2
/
&fire
/
&namelist_quilt
/
&perturbation
/
&logging
/
'''.format(e_we, e_sn, e_vert, dx, dy, radio,YYYY0, MM0, DD0, HH0, DHH2, DHH3, YYYY1, MM1, DD1)

    return s



if __name__=='__main__':

    start()
