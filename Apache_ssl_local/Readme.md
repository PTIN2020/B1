# Llegiu abans de fer canvis

**Aquest projecte és una plantilla, està pensat perquè es modifiqui segons les necessitats**

**Llistat de les carpetes/fitxers que heu de modificar segons les vostres necessitats**

- **_docker-compose_**: Fitxer del compose per fer el muntatge o construcció del contenidor, cal només tocar la part de **_volumes:_** i la de **_ports:_**

- **_Dockerfile_**: Fitxer on hi ha la configuració d'Ubuntu amb Apache instal·lat. Es pot canviar tant d'imatge de sistema , com de programes instal·lats. El codi ja està documentat.

- **_ApacheConf i ApacheFiles_**: Són les carpetes contenidores de la configuració del domini i del contingut d'aquest. Es poden reutilitzar i guardar les configuracions a dins o es poden canviar les carpetes dins del _docker-compose_ i dins del _Dockerfile_


- **_configs_**: Conté la configuració del servidor Apache en l'àmbit de servidor així com en l'àmbit de client. No es recomana tocar les configuracions a menys que sigui necessari.