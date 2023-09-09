import os
import sys
import datetime as dt

#-------------------------------------------------------------------------------
# Starting dates of wrf runs
#-------------------------------------------------------------------------------
# https://dreambooker.site/2017/12/20/Initializing-the-WRF-model-with-ECMWF-ERA-Interim-reanalysis/
# http://climate-cms.wikis.unsw.edu.au/How_to_run_WRF_with_ERA-Interim_data



def start():

    date = dt.datetime(2014,12,6,0)
    date1 = date + dt.timedelta(hours=24)
    date2 = dt.datetime(2019,8,1,0)

    for i in range(31*12*11): # cada 12 horas

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

        main(YYYY0+'-'+MM0+'-'+DD0+'_'+HH0+':00:00', YYYY1+'-'+MM1+'-'+DD1+'_'+HH1+':00:00',YYYY0+MM0+DD0+HH0+'00', HH0)

        date += dt.timedelta(hours=24)
        date1 = date + dt.timedelta(hours=24)

        if date == date2:
            break


#    main('2009-01-01_00:00:00', '2019-08-01_00:00:00', str('200901010000'), '00')


def main(sdates, edates, gfsdir, init):

    # Start and End date

    sYYYY = str(sdates[0:4])
    sMM   = str(sdates[5:7])
    sDD   = str(sdates[8:10])
    sHH   = str(sdates[11:13])

    eYYYY = str(edates[0:4])
    eMM   = str(edates[5:7])
    eDD   = str(edates[8:10])
    eHH   = str(edates[11:13])

    #------------------------------------------------------
    # Parametros a editar
    #------------------------------------------------------

    # Definiendo directorios a usar

    WPSDIR   = '/home/adrian/WRF/WPS-4.1'
    WRFDIR   = '/home/adrian/WRF/WRF-4.1.2'
    DATA_GRB = '/home/adrian/NAS/Data/era-interim'
    GEOG_dir = '/home/adrian/WRF/WPS_GEOG/'

    # Directorio de salidas

    RDIR     = '/home/adrian/WRF/Runs'
    RUN_DIR  = RDIR+'/d01_lin_bmj'

    obsdir = '/home/adrian/NAS/Data/makeOBS'

    # Numero de procesadores
    NCPU = 32

    #------------------------------------------------------

    # Namelist del nucleo atmosferico del modelo
    fname_wrf = 'namelist.input'

    # Namelist del WPS del modelo WRF
    fname_wps = 'namelist.wps'


    # Linkeando ficheros necesarios para el WPS

    os.system('mkdir -p ' + RUN_DIR)
    os.system('mkdir -p ' + RUN_DIR + '/metgrid')
    os.system('mkdir -p ' + RUN_DIR + '/geogrid')
    os.system('mkdir -p ' + RUN_DIR + '/outputs')

    os.system('ln -sf '+obsdir+'/obs_data_'+sYYYY+sMM+sDD+'00.ltr.obsnud '+RUN_DIR+'/OBS_DOMAIN101')

    os.system('cp -u ' + WPSDIR + '/geogrid/GEOGRID.TBL ' + RUN_DIR + '/geogrid/')
    os.system('cp -u ' + WPSDIR + '/metgrid/METGRID.TBL ' + RUN_DIR + '/metgrid/METGRID.TBL')   # .ECMWF
    os.system('cp -f ' + WPSDIR + '/ungrib/Variable_Tables/Vtable.ECMWF '+ RUN_DIR + '/Vtable')
    os.system('cp -u ' + WPSDIR + '/link_grib.csh ' + RUN_DIR)
    os.system('ln -sf ' + WPSDIR + '/geogrid/src/geogrid.exe ' + RUN_DIR)
    os.system('ln -sf ' + WPSDIR + '/ungrib/src/ungrib.exe ' + RUN_DIR)
    os.system('ln -sf ' + WPSDIR + '/metgrid/src/metgrid.exe ' + RUN_DIR)
    os.system('ln -sf ' + WPSDIR + '/util/src/mod_levs.exe ' + RUN_DIR)

    # Linkeando ficheros necesarios para el WRF
    os.system('ln -sf ' + WRFDIR + '/main/wrf.exe ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/main/real.exe ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/main/ndown.exe ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/GENPARM.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/grib2map.tbl ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/LANDUSE.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/MPTABLE.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/SOILPARM.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/URBPARM.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/URBPARM_UZE.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/VEGPARM.TBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/RRTM_DATA ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/*CAM* ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/RRTM_DATA_DBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/RRTMG_LW_DATA ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/RRTMG_LW_DATA_DBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/RRTMG_SW_DATA ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/RRTMG_SW_DATA_DBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/tr49t67 ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/tr49t85 ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/tr67t85 ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/CAM_ABS_DATA ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/CAM_AEROPT_DATA ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA_DBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/co2_trans ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA.expanded_rain ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/ETAMPNEW_DATA.expanded_rain_DBL ' + RUN_DIR)
    os.system('ln -sf ' + WRFDIR + '/run/ozone* ' + RUN_DIR)

    os.chdir(RUN_DIR)

    #-----------------------------------------------------------------------------
    # Corriendo por todos los elementos del array 'sdates'
    # Este array es util para lanzar mas de una corrida
    #-----------------------------------------------------------------------------

    #----------------------
    # runing WPS from WRF model
    #----------------------

    #***********************
    # Niveles de presion

    # eliminando namelist viejos
    os.system('rm -f namelist.wps')

    # write wps namelist
    f = open(fname_wps,'w')
    s = namelist_wps(sdates, edates, GEOG_dir, RUN_DIR, 'PL')
    f.write(s)
    f.close()

    #borrando ficheros viejos
    os.system('rm -f WPS:* GRIBFILE* PFILE*')

    #----------------------
    # runing WPS GFS LINKS
    #----------------------

    grbfile1  = "an_pl_"+sYYYY+sMM+"*.grb"

    os.system("ln -sf " + DATA_GRB + '/' + grbfile1 + " " + RUN_DIR)

    #----------------------
    # runing WPS UNGRID
    #----------------------

    # Linkeando ficheros
    os.system('csh ' + RUN_DIR + '/link_grib.csh ' + RUN_DIR + '/' + grbfile1)

    os.system('./ungrib.exe')


    #***********************
    # Nivel de superficie

    # eliminando namelist viejos
    os.system('rm -f namelist.wps')

    # write wps namelist
    f = open(fname_wps,'w')
    s = namelist_wps(sdates, edates, GEOG_dir, RUN_DIR, 'SFC')
    f.write(s)
    f.close()

    #borrando ficheros viejos
    os.system('rm -f WPS:* GRIBFILE* PFILE*')

    #----------------------
    # runing WPS GFS LINKS
    #----------------------

    grbfile2  = "an_sfc_"+sYYYY+sMM+"*.grb"

    os.system("ln -sf " + DATA_GRB + '/' + grbfile2 + " " + RUN_DIR)

    #----------------------
    # runing WPS UNGRID
    #----------------------

    # Linkeando ficheros
    os.system('csh ' + RUN_DIR + '/link_grib.csh ' + RUN_DIR + '/' + grbfile2)

    os.system('./ungrib.exe')



    #***********************
    # ficheros invariantes

    # eliminando namelist viejos
    os.system('rm -f namelist.wps')

    # write wps namelist
    f = open(fname_wps,'w')
    s = namelist_wps('1989-01-01_12:00:00', '1989-01-01_12:00:00', GEOG_dir, RUN_DIR, 'FIX')
    f.write(s)
    f.close()

    #borrando ficheros viejos
    os.system('rm -f WPS:* GRIBFILE* PFILE*')

    #----------------------
    # runing WPS GFS LINKS
    #----------------------

    grbfile3  = "invariant_data.grib"

    os.system("ln -sf " + DATA_GRB + '/' + grbfile3 + " " + RUN_DIR)

    #----------------------
    # runing WPS UNGRID
    #----------------------

    # Linkeando ficheros
    os.system('csh ' + RUN_DIR + '/link_grib.csh ' + RUN_DIR + '/' + grbfile3)

    os.system('./ungrib.exe')


    #----------------------
    # runing WPS GEOGRID
    #----------------------

    if not os.path.exists(RDIR+'/geo_em.d01.nc'):
        os.system('mpirun -np '+str(NCPU)+' ./geogrid.exe')


    #----------------------
    # runing WPS METGRID
    #----------------------

    # eliminando namelist viejos
    os.system('rm -f namelist.wps')

    # write wps namelist
    f = open(fname_wps,'w')
    s = namelist_wps(sdates, edates, GEOG_dir, RUN_DIR, 'SFC')
    f.write(s)
    f.close()

    os.system('mpirun -np '+str(NCPU)+' ./metgrid.exe')


    #----------------------
    # runing WRF model
    #----------------------

    # Eliminando namelist viejos
    os.system('rm -f namelist.input')

    #---------------------------
    # Run real.exe
    #---------------------------

    #write init namelist    
    f = open(fname_wrf,'w')
    s = namelist_wrf(sdates, edates, RDIR)
    f.write(s)
    f.close()

    os.system('mpirun -np '+str(NCPU)+' ./real.exe')

    os.system('mv rsl.error.0000 real.rsl.error.0000')
    os.system('mv rsl.out.0000 real.rsl.out.0000')


    #---------------------------
    # Run wrf.exe
    #---------------------------

    # Parallel
    os.system('mpirun -np '+str(NCPU)+' ./wrf.exe')

    # Eliminando ficheros viejos
#    os.system('rm -f met_em* PFILE* FILE*')

    os.system('rm -f wrfbdy_d* wrfinput_d* wrflowinp_d* wrffdda_d* OBS_DOMAIN* wrfout_d*')
    os.system('mv ' + RUN_DIR + '/wrfxtrm_d*_'+edates+' ' + RUN_DIR + '/outputs')
    os.system('mv ' + RUN_DIR + '/wrfrain_d*_'+edates+' ' + RUN_DIR + '/outputs')


# REAL & WRF

def namelist_wrf(startTime, endTime, RDIR):

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
 interval_seconds                    = 21600,
 input_from_file                     = .true.,.true.,
 history_interval                    = 44640,  44640,  44640,
 frames_per_outfile                  = 1, 1, 1,
 restart                             = .false.,
 restart_interval                    = 44640,
 io_form_history                     = 2
 io_form_restart                     = 2
 io_form_input                       = 2
 io_form_boundary                    = 2
 debug_level                         = 0
 auxinput4_inname = "wrflowinp_d<domain>"
 auxinput4_interval = 360,
 io_form_auxinput4 = 2,
 output_diagnostics = 1 ,
 auxhist3_outname                    = "wrfxtrm_d<domain>_<date>",
 io_form_auxhist3                    = 2,
 auxhist3_interval                   = 1440,1440,
 frames_per_auxhist3                 = 1,1,
 auxhist16_outname = "wrfrain_d<domain>_<date>",
 auxhist16_interval = 180,180,180,
 io_form_auxhist16   = 2,
 frames_per_auxhist16 = 1,1,1,1,
 iofields_filename = "{8}/my_file_d01.txt","{8}/my_file_d01.txt",
 ignore_iofields_warning = .true.,
 /

 &domains
time_step                = 90,
time_step_fract_num      = 0,
time_step_fract_den      = 1,
! time_step = 150, 
! time_step_fract_num = 0, 
! time_step_fract_den = 1, 
! use_adaptive_time_step = .true. 
! step_to_output_time = .true. 
! starting_time_step = 150,50, 
! max_time_step = 300,100, 
! adaptation_domain = 2, 
 max_dom                             = 1,
e_we                     = 270,
e_sn                     = 186,
 e_vert                              = 50,  50,  50,  
 p_top_requested                     = 10000, 
 num_metgrid_levels                  = 38, 
 num_metgrid_soil_levels             = 4, 
dx                       = 15000,
dy                       = 15000,
grid_id                  = 1,        2,
parent_id                = 1,        1,
i_parent_start           = 1,       98,
j_parent_start           = 1,       68,
parent_grid_ratio        = 1,        5,
parent_time_step_ratio   = 1,        5,
 feedback                            = 0,     
 smooth_option                       = 0,     
 nproc_x = 4
 nproc_y = 8
 /


 &physics
 mp_physics                          = 2,    2,   2,
 ra_lw_physics                       = 4,     4,    4,
 ra_sw_physics                       = 4,     4,    4,
 radt                                = 5,    5,   5,
 sf_sfclay_physics                   = 1,     1,     1,
 sf_surface_physics                  = 2,     2,     2,
 bl_pbl_physics                      = 1,     1,     1,
 bldt                                = 0,     0,     0,
 cu_physics                          = 2,     2,     2,
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
 NUM_LAND_CAT = 21,
 sst_update = 1,
 /

&fdda
 grid_fdda                           = 2,  0,  0,  0,
 gfdda_inname                        = "wrffdda_d<domain>",
 gfdda_end_h                         = 140256,  72, 72, 72, 
 gfdda_interval_m                    = 360,  360,  360, 360,
 fgdt                                = 0,  0,  0,  0,
 fgdtzero                            = 1,  1,  1,  1,
 if_no_pbl_nudging_uv                = 1,  1,  1,  1,
 if_no_pbl_nudging_t                 = 1,  1,  1,  1,
 if_no_pbl_nudging_ph                = 1,  1,  1,  1,
 if_no_pbl_nudging_q                 = 1,  1,  1,  1,
 if_zfac_uv                          = 1,  1,  1,  1,
  k_zfac_uv                          = 20, 10, 10, 10,
 if_zfac_t                           = 1,  1,  1,  1,
  k_zfac_t                           = 20, 10, 10, 10,
 if_zfac_ph                          = 1,  1,  1,  1,
  k_zfac_ph                          = 20, 10, 10, 10,
 if_zfac_q                           = 1,  1,  1,  1,
  k_zfac_q                           = 20, 10, 10, 10,
 dk_zfac_uv                          = 5,  5,  5,  5,
 dk_zfac_t                           = 5,  5,  5,  5,
 dk_zfac_ph                          = 5,  5,  5,  5,
 guv                                 = 0.0003, 0.0003, 0.0003, 0.0003,
 gt                                  = 0.0003, 0.0003, 0.0003, 0.0003,
 gph                                 = 0.0003, 0.0003, 0.0003, 0.0003,
 xwavenum                            = 5, 9, 9, 9, 
 ywavenum                            = 4, 7, 7, 7,
 if_ramping                          = 0,
 dtramp_min                          = 60.0,
 io_form_gfdda                       = 2,
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


'''.format(YYYY0, MM0, DD0, HH0, YYYY1, MM1, DD1, HH1, RDIR)
  return s


# WPS
def namelist_wps(startTime, endTime, GEOG_dir, RDIR, dname):

  s = '''&share
 wrf_core = 'ARW',
 max_dom = 1,
 start_date = '{0}','{0}','{0}',
 end_date   = '{1}','{1}','{1}',
 interval_seconds = 21600,
 io_form_geogrid = 2,
 opt_output_from_geogrid_path = '{3}'
 debug_level = 1000
/

&geogrid
 parent_id         = 1,1,
 parent_grid_ratio = 1,5,
 i_parent_start    = 1,98,
 j_parent_start    = 1,68,
 e_we          = 270,
 e_sn          = 186,
 geog_data_res = 'geog_modis_15s+modis_fpar+modis_lai+30s','geog_modis_15s+modis_fpar+modis_lai+30s','geog_modis_15s+modis_fpar+modis_lai+30s',
 dx = 15000,
 dy = 15000,
 map_proj =  'mercator',
 ref_lat   = 4.497,
 ref_lon   = -58.768,
 truelat1  = 4.497,
 truelat2  = 0,
 stand_lon = -58.768,
 geog_data_path = '{2}',
 ref_x = 135.0,
 ref_y = 93.0,
/

&ungrib
 out_format = 'WPS',
 prefix = '{4}',
/

&metgrid
 fg_name = 'PL','SFC',
 constants_name = 'FIX:1989-01-01_12',
 io_form_metgrid = 2,
/
'''.format(startTime, endTime, GEOG_dir, RDIR, dname)
  return s



if __name__=='__main__':
    start()


