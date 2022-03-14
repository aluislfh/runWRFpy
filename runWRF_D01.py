import os
import sys
import datetime as dt

#-------------------------------------------------------------------------------
# Script para correr el modelo WRF
#-------------------------------------------------------------------------------


# Esta funcion crea los namelist y lanza las corridas
def start():
    

    date = dt.datetime(2014,1,1,0)
    date1 = date + dt.timedelta(hours=24)
    date2 = dt.datetime(2014,2,1,0)

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

        main(YYYY0+'-'+MM0+'-'+DD0+'_'+HH0+':00:00', YYYY1+'-'+MM1+'-'+DD1+'_'+HH1+':00:00')

        date += dt.timedelta(hours=24)
        date1 = date + dt.timedelta(hours=24)

        if date == date2:
            break


    date = dt.datetime(2014,7,1,0)
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

        main(YYYY0+'-'+MM0+'-'+DD0+'_'+HH0+':00:00', YYYY1+'-'+MM1+'-'+DD1+'_'+HH1+':00:00')

        date += dt.timedelta(hours=24)
        date1 = date + dt.timedelta(hours=24)

        if date == date2:
            break


def main(sdates, edates):

    fisicas = ['4']
    lightnings = ['0']

    for li in lightnings:
        for mp in fisicas:
            
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
            WPSDIR   = '/opt/NWP/v4.1/WPS'
            WRFDIR   = '/opt/NWP/v4.1/WRF'
            DATA_GRB = '/home/cluster/DATA/Roque'
            RUN_DIR  = '/home/cluster/hdd1/DATA/D01/run_mp'+mp+'_l'+li+"_"+sYYYY+sMM+sDD+sHH
            GEOG_dir = '/opt/NWP/GEOG/geog_complete/'
        
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
            s = namelist_wps(sdates, edates, GEOG_dir)
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

#            sys.exit()
        
        #****************************************************************************************

            if not os.path.exists('/home/cluster/hdd1/DATA/D01/geo_em.d01.nc'):
            #generate initial data with ungrib.exe
#                cmd = 'mpirun -np 12 ./geogrid.exe'
                cmd = './geogrid.exe'
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
            s = namelist_wrf(sdates, edates, mp, li)
            f.write(s)
            f.close()
        
            cmd = 'mpirun -np 12 ./real.exe'
            os.system(cmd)
        
            cmd = 'mv rsl.error.0000 real.rsl.error.0000'
            os.system(cmd)
            cmd = 'mv rsl.out.0000 real.rsl.out.0000'
            os.system(cmd)
        
            #---------------------------
            # Run wrf.exe
            #---------------------------
        
            # Parallel
            cmd = 'mpirun -np 12 ./wrf.exe'
            os.system(cmd)
        
            # Eliminando ficheros viejos
            cmd = 'rm -f met_em* PFILE* FILE*'
#            os.system(cmd)

#            sys.exit()




# REAL & WRF

def namelist_wrf(startTime, endTime, mp, li):

  YYYY0 = str(startTime[0:4])
  MM0   = str(startTime[5:7])
  DD0   = str(startTime[8:10])
  HH0   = str(startTime[11:13])

  YYYY1 = str(endTime[0:4])
  MM1   = str(endTime[5:7])
  DD1   = str(endTime[8:10])
  HH1   = str(endTime[11:13])

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
 input_from_file                     = .true.,.true.,
 history_interval                    = 180,  180,  180,  60, 60,   
 frames_per_outfile                  = 1, 1, 1, 1000, 1000,
 restart                             = .false.,
 restart_interval                    = 5000,
 io_form_history                     = 2
 io_form_restart                     = 2
 io_form_input                       = 2
 io_form_boundary                    = 2
 debug_level                         = 0
 /

 &domains
time_step                = 150,
time_step_fract_num      = 0,
time_step_fract_den      = 1,
 max_dom                             = 2, 
 i_parent_start                      =  1,   43,   18,  60,  35,
 j_parent_start                      =  1,   17,   12,  64,  40,
 e_we                                = 140,  199,  472, 994, 3701,
 e_sn                                =  78,  112,   190, 508, 1701,
 e_vert                              = 30,  30,  30,  
 p_top_requested                     = 10000, 
 num_metgrid_levels                  = 27, 
 num_metgrid_soil_levels             = 4, 
 dx                                  = 27000,  9000,  3000
 dy                                  = 27000,  9000,  3000
 grid_id                             = 1,     2,     3,
 parent_id                           = 1,     1,     2,
 parent_grid_ratio                   = 1,     3,     3,
 parent_time_step_ratio              = 1,     3,     3,
 feedback                            = 1,     
 smooth_option                       = 0,     
 /


 &physics
 mp_physics                          = {8},     {8},    {8},
 ra_lw_physics                       = 1,     1,    1,
 ra_sw_physics                       = 1,     1,    1,
 radt                                = 81,    81,   81,
 sf_sfclay_physics                   = 2,     2,     2,
 sf_surface_physics                  = 2,     2,     2,
 bl_pbl_physics                      = 5,     5,     5,
 bldt                                = 0,     0,     0,
 cu_physics                          = 3,     3,     3,
 cudt                                = 0,     0,     0,
 isfflx                              = 1,
 ifsnow                              = 0,
 icloud                              = 1,
 surface_input_source                = 1,
 num_soil_layers                     = 4,
 sf_urban_physics                    = 0,
 maxiens                             = 1,
 maxens                              = 3,
 maxens2                             = 3,
 maxens3                             = 16,
 ensdim                              = 144,
 do_radar_ref = 1,
 lightning_option = {9}, {9}, {9},
 lightning_dt = 150, 150, 150,
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
 kvdif                               = 0,      0,      0,60,  60,  60
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

'''.format(YYYY0, MM0, DD0, HH0, YYYY1, MM1, DD1, HH1, mp, li)
  return s

# WPS
def namelist_wps(startTime, endTime, GEOG_dir):
  s = '''&share
 wrf_core = 'ARW',
 max_dom = 2,
 start_date = '{0}','{0}','{0}',
 end_date   = '{1}','{1}','{1}',
 interval_seconds = 10800,
 io_form_geogrid = 2,
 opt_output_from_geogrid_path = '/home/cluster/hdd1/DATA/D01/'
 debug_level = 1000
/

&geogrid
 parent_id         = 1,1,
 parent_grid_ratio = 1,3,
 i_parent_start    = 1,43,
 j_parent_start    = 1,17,
 e_we          = 140,199,
 e_sn          = 78,112,
 geog_data_res = '30s','30s','30s',
 dx = 27000,
 dy = 27000,
 map_proj =  'mercator',
 ref_lat   = 23.162,
 ref_lon   = -81.054,
 truelat1  = 23.162,
 truelat2  = 0,
 stand_lon = -82.054,
 geog_data_path = '{2}'
/

&ungrib
 out_format = 'WPS',
 prefix = 'FILE',
/

&metgrid
 fg_name = 'FILE'
 io_form_metgrid = 2,
/
'''.format(startTime, endTime, GEOG_dir)
  return s




if __name__=='__main__':
    start()

