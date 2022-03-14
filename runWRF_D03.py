import os
import sys
import fnmatch
import datetime as dt

#---------------------------------------------------------------------------------------------
# Runing WRF model
#---------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Script para correr el modelo WRF
#-------------------------------------------------------------------------------

# Esta funcion crea los namelist y lanza las corridas
def start():

    date = dt.datetime(2014,7,12,0)
    date1 = date + dt.timedelta(hours=24)
    date2 = dt.datetime(2014,8,1,0)

    for i in range(31*4+1): # cada 12 horas

        dates=str(date).split()
        dates=str(dates[0] + '_' + dates[1])
        
        YYYY0 = str(dates[0:4])
        MM0   = str(dates[5:7])
        DD0   = str(dates[8:10])
        HH0   = str(dates[11:13])

        dates=str(date1).split()
        dates=str(dates[0] + '_' + dates[1])

        YYYY1 = str(dates[0:4])
        MM1   = str(dates[5:7])
        DD1   = str(dates[8:10])
        HH1   = str(dates[11:13])

        main(YYYY0+MM0+DD0+HH0, YYYY1+MM1+DD1+HH1)

        date += dt.timedelta(hours=24)
        date1 = date + dt.timedelta(hours=24)

        if date == date2:
            break


# Esta funcion crea los namelist y lanza las corridas

def main(sdates, edates):

    fisicas = ['10']
    lightnings = ['0']

    for li in lightnings:
        for mp in fisicas:

            sYYYY = str(sdates[0:4])
            sMM   = str(sdates[4:6])
            sDD   = str(sdates[6:8])
            sHH   = str(sdates[8:10])

            eYYYY = str(edates[0:4])
            eMM   = str(edates[4:6])
            eDD   = str(edates[6:8])
            eHH   = str(edates[8:10])

            # Namelist del nucleo atmosferico del modelo
            fname_wrf = 'namelist.input'

            # Namelist del WPS del modelo WRF
            fname_wps = 'namelist.wps'

            # Definiendo directorios a usar
            WPSDIR   = '/opt/NWP/v4.1/WPS'
            WRFDIR   = '/opt/NWP/v4.1/WRF'
            DATA_GRB = '/home/cluster/DATA/Roque'
            RUN_DIR  = '/home/cluster/hdd2/DATA/D03/run_mp'+mp+'_l'+li+"_"+sYYYY+sMM+sDD+sHH
            RUN_DIR1  = '/home/cluster/hdd1/DATA/D01/run_mp'+'4'+'_l'+li+"_"+sYYYY+sMM+sDD+sHH
            GEOG_dir = '/opt/NWP/GEOG/geog_complete/'

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
            cmd = 'cp -f /home/cluster/hdd1/DATA/D01/Vtable.GFS '+ RUN_DIR + '/Vtable'  # Vtable viejo para 2014
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
            s = namelist_wps(sdates, edates, NDOM, GEOG_dir, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32)
            f.write(s)
            f.close()

            #borrando ficheros viejos
            cmd = 'rm -f WPS:* GRIBFILE* PFILE*'
            os.system(cmd)


        #****************************************************************************************

            grbfile1  = "gfsanl_4_"+sYYYY+sMM+sDD+"_*.grb2"
            grbfile2  = "gfsanl_4_"+eYYYY+eMM+eDD+"_"+eHH+"*.grb2"

            os.system("ln -sf " + DATA_GRB + '/' + grbfile1 + " " + RUN_DIR)
            os.system("ln -sf " + DATA_GRB + '/' + grbfile2 + " " + RUN_DIR)
        
            # Linkeando ficheros
            cmd = 'csh ' + RUN_DIR + '/link_grib.csh ' + RUN_DIR + '/' + "gfsanl_4_*.grb2"
            os.system(cmd)
        
            #generate initial data with ungrib.exe
            cmd = './ungrib.exe'
            os.system(cmd)

        #****************************************************************************************

            #generate initial data with ungrib.exe
            if not os.path.exists('/home/cluster/hdd1/DATA/D03/geo_em.d01.nc'):
                cmd = 'mpirun -np 12 ./geogrid.exe'
                os.system(cmd)

            #generate initial data with metgrid.exe
            cmd = 'mpirun -np 12 ./metgrid.exe'
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
            s = namelist_wrf(sdates, edates, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, 10800, mp, li)
            f.write(s)
            f.close()

            cmd = 'mpirun -np 12 ./real.exe'
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
            s = namelist_wrf(sdates, edates, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, 10800, mp, li)
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
                print  wf + ' ' + wfsp[0] + '_d01_' + wfsp[2] + '_' + wfsp[3]
                cmd='mv ' + wf + ' ' + wfsp[0] + '_d01_' + wfsp[2] + '_' + wfsp[3]
                os.system(cmd)

            cmd = 'mpirun -np 12 ./ndown.exe'
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
        #    cmd = 'mv -f wrfinput_d03 wrfinput_d02'
        #    os.system(cmd)

            cmd = 'rm -f wrfout*'
            os.system(cmd)

            cmd = 'rm -f wrfndi_d02'
            os.system(cmd)

            # Eliminando namelist viejos
            cmd = 'mv namelist.input namelist.input.1'
            os.system(cmd)

            #write init namelist    (wrf.exe)
            f = open(fname_wrf,'w')
            s = namelist_wrf(sdates, edates, NNDOM, NDX1, NDX2, NDX2, NDNX1, NDNY1, NDNX2, NDNY2, NDNX2, NDNY2, NPX21, NPY21, NPX21, NPY21, 10800, mp, li)
            f.write(s)
            f.close()

            #---------------------------
            # Run wrf.exe
            #---------------------------

            # Parallel
            cmd = 'mpirun -np 12 ./wrf.exe'
            os.system(cmd)

            # Eliminando ficheros viejos
            cmd = 'rm -f met_em* PFILE* FILE*'
        #    os.system(cmd)


# REAL & WRF

# REAL & WRF

def namelist_wrf(startTime, endTime, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, NINT, mp, li):

  YYYY0 = str(startTime[0:4])
  MM0   = str(startTime[4:6])
  DD0   = str(startTime[6:8])
  HH0   = str(startTime[8:10])

  YYYY1 = str(endTime[0:4])
  MM1   = str(endTime[4:6])
  DD1   = str(endTime[6:8])
  HH1   = str(endTime[8:10])
    
# auxinput4_inname = "wrflowinp_d<domain>",
# auxinput4_interval = 360,
# io_form_auxinput4 = 2

  s = '''&time_control
 run_days                            = 0,
 run_hours                           = 36,
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
 frames_per_outfile                  = 1, 1, 1, 1000, 1000,
 restart                             = .false.,
 restart_interval                    = 10800,
 io_form_history                     = 2,
 io_form_restart                     = 2,
 io_form_input                       = 2,
 io_form_boundary                    = 2,
 io_form_auxinput2                   = 2,
 debug_level                         = 0,
 /

 &domains
 time_step                = 45,
 time_step_fract_num      = 0,
 time_step_fract_den      = 1,
max_dom                  = {8},
e_we                     = {12},  {14}, {16},
e_sn                     = {13},  {15}, {17},
 e_vert                              = 30,  30,  30,  
 p_top_requested                     = 10000, 
 num_metgrid_levels                  = 27,
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
 mp_physics                          = {23},   {23},   {23},
 ra_lw_physics                       = 1,     1,     1,
 ra_sw_physics                       = 2,     2,     2,
 radt                                = 81,    81,   81,
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
 lightning_option = {24}, {24}, {24},
 lightning_dt = 45, 45, 45,
 lightning_start_seconds = 600, 600, 600,
 flashrate_factor = 1.0, 1.0, 1.0,
 cellcount_method = 0, 0, 0,
 iccg_method = 3, 3, 3,
 iccg_prescribed_num = 0.,
 iccg_prescribed_den = 1.,
 NUM_LAND_CAT = 21,
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

'''.format(YYYY0, MM0, DD0, HH0, YYYY1, MM1, DD1, HH1, NDOM, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32, NINT, mp, li)

# w_damping                           = 0,
# damp_opt                            = 0,

  return s



# WPS
def namelist_wps(startTime, endTime, NDOM, GEOG_dir, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32):

  YYYY0 = str(startTime[0:4])
  MM0   = str(startTime[4:6])
  DD0   = str(startTime[6:8])
  HH0   = str(startTime[8:10])

  YYYY1 = str(endTime[0:4])
  MM1   = str(endTime[4:6])
  DD1   = str(endTime[6:8])
  HH1   = str(endTime[8:10])

  startTime, endTime = (YYYY0+'-'+MM0+'-'+DD0+'_'+HH0+':00:00', YYYY1+'-'+MM1+'-'+DD1+'_'+HH1+':00:00')

  s = '''&share
 wrf_core = 'ARW',
 max_dom = {2},
 start_date = '{0}','{0}','{0}',
 end_date   = '{1}','{1}','{1}',
 interval_seconds = 10800,
 opt_output_from_geogrid_path = '/home/cluster/hdd1/DATA/D03/'
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

'''.format(startTime, endTime, NDOM, GEOG_dir, DX1, DX2, DX3, DNX1, DNY1, DNX2, DNY2, DNX3, DNY3, PX21, PY21, PX32, PY32)


  return s




if __name__=='__main__':

    start()
