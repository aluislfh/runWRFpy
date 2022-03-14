# runWRFpy
Scripts para correr WRF con y sin Ndown.exe, asi como también con y sin asimilación de datos de observaciones meteorológicas.

En ambos scrips hay una función que se llama start() y está al inicio de ambos scripts, eso es para controlar que corrida quieres que se haga por la fecha y ya el luego hace todo en la funcion main(). Para una sola corrida la funcionn start() se puedes borrar y poner manual los datos de la fecha de la corrida que se quiere. Dentro de la función main() es donde esta lo más importante, al inicio de esa función aparece la declaración de las siguientes variables:

            # Definiendo directorios a usar
            WPSDIR   = '/opt/NWP/v4.1/WPS'
            WRFDIR   = '/opt/NWP/v4.1/WRF'
            DATA_GRB = '/home/cluster/DATA/Roque'
            RUN_DIR  = '/home/cluster/hdd1/DATA/D01/run_mp'+mp+'_l'+li+"_"+sYYYY+sMM+sDD+sHH
            GEOG_dir = '/opt/NWP/GEOG/geog_complete/'

Esas variables definen todas las carpetas necesarias; el WRF, WPS, los datos, donde quiero guardar las salidas, y donde estan los datos geográficos. Luego abajo el script hace todo con esas variables (aunque siempre abajo hay alguna que otra cosa que revisar como la cantidad de procesadores a utilizar, etc.).

Podras encontrar 2 scrips: 1) runWRFnodes_d1.py, ese es para hacer una corrida simple de 2 dominios (el ejemplo disponible es para 2 dominios de resoluciones espaciales de 27 y 9 km) y 2) runWRFnodes_d3.py: es otro script para hacer una corrida con NDOWN.EXE para el tercer dominio anidado. En este ultimo script la funcion main() se deberá cambiar otras cosas como:

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


Estos ultimo tramo del script que dice "Parámetros del namelist 2" es para correr ya WRF en el 3er dominio una vez de haber pasado por WPS, REAL.EXE y NDOWN.EXE

Más abajo en ambos scripts verá que vienen 2 funciones con los namelist de WPS y WRF, ahí la configuración de parametrizaciones, cantidad de puntos por X y Y, cantidad de niveles verticales, y etc, puede ser modificada a las desciciones de los usuarios. De igual forma en caso de no contar con un diseño de dominios a seguir se puede crear uno con el WRFWizzardDomain.


Scripts con WRFDA

Direcciones necesarias para realizar simulaciones con WRFDA:

    # Dirección de donde está instalado el WRFDA
    WRFDADIR    = '/home/adrian/WRF/WRF_4.3/WRFDA-CVCLOUD/WRF-4.3' 

    # Dirección de los datos de observaciones meteorologicas en formato BUFR
    OBS_DATA = '/media/adrian/hdd_glm/PHD_runs/OBS/PREPBUFR'

    # Dirección de los ficheros de matrices de covarianza creados previamente
    genbe = '/media/adrian/hdd_glm/PHD_runs/GenBE'
    
    # Dirección de los ficheros de pronosticos de ciclos anteriores para emplearlos como miembros del ensembre para 3DEnVAR/4DEnVAR
    ENS_DIR = '/media/adrian/hdd_glm/PHD_runs/RUNS_3DEnVAR/EnsData'
    
    El fichero table.txt tiene la descripcion del directorio EnsData.
    
    
    
    
    
    
    






