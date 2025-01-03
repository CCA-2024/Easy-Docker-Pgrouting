FROM postgis/postgis:16-3.4

# EDIT NAME FOR YOUR FILE OSM
ENV FILE_OSM brazil-latest.osm.pbf

# EDIT YOUR GRAPH TYPE 
# CHOICE >> [mapconfig_for_cars.xml, mapconfig_for_bicycles.xml, mapconfig_for_cars.xml, mapconfig_for_pedestrian.xml]
ENV TYPEGRAPH mapconfig.xml  

# DEFAULTS VERSIONS
ENV OSM2PGROUTING_VERSION 2.3.8
ENV PGROUTING_VERSION 3.6.2
ENV PGROUTING_SHA256 f4a1ed79d6f714e52548eca3bb8e5593c6745f1bde92eb5fb858efd8984dffa2

# CODE MAKE PGROUTING
RUN set -ex \
 && apt update \
 && apt install -y \
        libboost-atomic1.74.0 \
        libboost-chrono1.74.0 \
        libboost-graph1.74.0 \
        libboost-date-time1.74.0 \
        libboost-program-options1.74.0 \
        libboost-system1.74.0 \
        libboost-thread1.74.0 \
 && apt install -y \
        build-essential \
        cmake \
        wget \
        libboost-graph-dev \
        libpq-dev \
        postgresql-server-dev-${PG_MAJOR} \
 && wget -O pgrouting.tar.gz "https://github.com/pgRouting/pgrouting/archive/v${PGROUTING_VERSION}.tar.gz" \
 && echo "$PGROUTING_SHA256 *pgrouting.tar.gz" | sha256sum -c - \
 && mkdir -p /usr/src/pgrouting \
 && tar \
        --extract \
        --file pgrouting.tar.gz \
        --directory /usr/src/pgrouting \
        --strip-components 1 \
 && rm pgrouting.tar.gz \
 && cd /usr/src/pgrouting \
 && mkdir build \
 && cd build \
 && cmake .. \
 && make \
 && make install \
 && cd / \
 && rm -rf /usr/src/pgrouting \
 && apt-mark manual postgresql-16
RUN rm /docker-entrypoint-initdb.d/10_postgis.sh

# CODE MAKE OSM2PGROUTING
RUN apt update \
&& apt install -y \
       libpqxx-6.4 \
&& apt install -y \
       build-essential \
       cmake \
       wget \
       libboost-program-options-dev \
       libexpat1 \
       libexpat-dev \
       libosmium2-dev \
       libpqxx-dev \
       zlib1g-dev \
&& cd /usr/local/src \
&& wget https://github.com/pgRouting/osm2pgrouting/archive/v${OSM2PGROUTING_VERSION}.tar.gz \
&& tar xvf v${OSM2PGROUTING_VERSION}.tar.gz \
&& cd osm2pgrouting-${OSM2PGROUTING_VERSION} \
&& mkdir build \
&& cd build \
&& cmake .. \
&& make \
&& make install \
&& cd ../tools/osmium/ \
&& mkdir build \
&& cd build \
&& cmake .. \
&& make \
&& make install \
&& cd /usr/local/src \
&& rm -rf ./* 

# CREATE PATH TO APP
WORKDIR /app
COPY . .

# CONVERT PBF TO OSM
RUN chmod +x ./OSM/brazil-latest.osm.pbf
RUN chmod +x ./OSM/osmconvert64
RUN ./OSM/osmconvert64 ./OSM/${FILE_OSM} --drop-author --drop-version --out-osm -o=./OSM/output_data_reduc.osm

# BUILD GRAPH TO DB
RUN wget https://github.com/pgRouting/osm2pgrouting/archive/v${OSM2PGROUTING_VERSION}.tar.gz
RUN tar xvf v${OSM2PGROUTING_VERSION}.tar.gz
RUN rm v${OSM2PGROUTING_VERSION}.tar.gz
RUN osm2pgrouting --f ./OSM/output_data_reduc.osm --conf ./osm2pgrouting-${OSM2PGROUTING_VERSION}/${TYPEGRAPH} --dbname postgres --username postgres --clean

# CLEAN LIBs
RUN apt purge -y --autoremove \
       build-essential \
       cmake \
       wget \
       libpq-dev \
       libboost-graph-dev \
       postgresql-server-dev-${PG_MAJOR} \
       libboost-program-options-dev \
       libexpat-dev \
       libosmium2-dev \
       libpqxx-dev \
       zlib1g-dev \
       && apt autoremove -y \
       && rm -rf /var/lib/apt/lists/*