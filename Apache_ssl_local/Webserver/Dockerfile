FROM ubuntu:latest
#Variables Systema

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

ENV LANG=${OS_LOCALE} \
    LANGUAGE=${OS_LOCALE} \
    LC_ALL=${OS_LOCALE} \
    DEBIAN_FRONTEND=noninteractive

ENV APACHE_CONF_DIR=/etc/apache2

RUN \ 
   #BUILD_DEPS='software-properties-common python-software-properties' \
    dpkg-reconfigure locales \
    && apt-get update && apt-get install -y software-properties-common \
    #&& apt-get install --no-install-recommends -y $BUILD_DEPS \
    && add-apt-repository -y ppa:ondrej/apache2 \
    && apt-get update \
    && apt-get install -y curl apache2 \
    #Apache settings
    && cp /dev/null ${APACHE_CONF_DIR}/conf-available/other-vhosts-access-log.conf \
    && rm ${APACHE_CONF_DIR}/sites-enabled/000-default.conf ${APACHE_CONF_DIR}/sites-available/000-default.conf \
    && a2enmod rewrite ssl 

#OPENSSl Instalació del certificat, si es vol canviar el site, cal canviar el registre CN="" de la comanda.
RUN \
    apt-get install -y openssl \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=ES/ST=Catalonia/L=VilaNova/O=Terminal 2/OU=Org/CN=areportvilacat.ddns.net" \
    && mkdir /etc/apache2/ssl \
    && cp server.crt /etc/apache2/ssl/server.crt \
    && cp server.key /etc/apache2/ssl/server.key

    # Copy configurations
COPY ./configs/proxy_html.conf ${APACHE_CONF_DIR}/mods-available/
COPY ./configs/security.conf ${APACHE_CONF_DIR}/conf-available/
COPY ./configs/apache2.conf ${APACHE_CONF_DIR}/apache2.conf
COPY ./configs/httpd.conf /usr/local/apache2/httpd.conf

#Activar els mods de apache per a que treballi amb ssl
RUN \
    a2enmod rewrite \
    && a2enmod ssl \
    && a2enmod http2 \
    && a2enmod proxy \
    && a2enmod proxy_http \
    #&& a2ensite aeroportvila.conf \
    && service apache2 restart

#Copiar la configuració dels llocs que tenim al terminal
ADD ./Apache_Conf ${APACHE_CONF_DIR}/sites-available/

#Habilitar els sites, enlloc de aeroportvila.conf, el domini que dessitjeu
RUN \
    a2ensite aeroportvila.conf \
    && service apache2 restart \
    && service apache2 status \
    && apachectl -S

#Script per a que el container no es tanqui, i permeti la neteja de processos vells d'apache
# Copy the entrypoint  
COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

# Start all components
CMD ["/sbin/entrypoint.sh"]