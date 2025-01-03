FROM postgis/postgis:16-3.4

# Variáveis de ambiente
ENV FILE_OSM=brazil-latest.osm.pbf \
    TYPEGRAPH=mapconfig.xml \
    OSM2PGROUTING_VERSION=2.3.8 \
    PGROUTING_VERSION=3.6.2 \
    PGROUTING_SHA256=f4a1ed79d6f714e52548eca3bb8e5593c6745f1bde92eb5fb858efd8984dffa2

# Instalação de dependências e configuração do ambiente
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip zip \
    libboost-atomic1.74.0 libboost-chrono1.74.0 libboost-graph1.74.0 \
    libboost-date-time1.74.0 libboost-program-options1.74.0 \
    libboost-system1.74.0 libboost-thread1.74.0 libboost-graph-dev \
    libpq-dev postgresql-server-dev-${PG_MAJOR} libpqxx-6.4 libpqxx-dev \
    build-essential cmake libexpat1 libexpat-dev libosmium2-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Instalação do pgRouting
RUN wget -O pgrouting.tar.gz "https://github.com/pgRouting/pgrouting/archive/v${PGROUTING_VERSION}.tar.gz" \
 && echo "$PGROUTING_SHA256 *pgrouting.tar.gz" | sha256sum -c - \
 && mkdir -p /usr/src/pgrouting \
 && tar --extract --file pgrouting.tar.gz --directory /usr/src/pgrouting --strip-components 1 \
 && rm pgrouting.tar.gz \
 && cd /usr/src/pgrouting \
 && mkdir build && cd build \
 && cmake .. && make && make install \
 && cd / && rm -rf /usr/src/pgrouting

# Instalação do osm2pgrouting
RUN wget -O osm2pgrouting.tar.gz "https://github.com/pgRouting/osm2pgrouting/archive/v${OSM2PGROUTING_VERSION}.tar.gz" \
 && chmod +x osm2pgrouting.tar.gz \
 && tar xvf osm2pgrouting.tar.gz -C /usr/local/src \
 && rm osm2pgrouting.tar.gz \
 && cd /usr/local/src/osm2pgrouting-${OSM2PGROUTING_VERSION} \
 && mkdir build && cd build \
 && cmake .. && make && make install \
 && cd /usr/local/src && rm -rf osm2pgrouting-${OSM2PGROUTING_VERSION}

# Definição do diretório de trabalho e cópia dos arquivos
WORKDIR /app
COPY . .

# Configuração e execução do processamento
RUN chmod +x ./OSM/osmconvert64 \
 && ./OSM/osmconvert64 ./OSM/${FILE_OSM} --drop-author --drop-version --out-osm -o=./OSM/output_data_reduc.osm \
 && osm2pgrouting --f ./OSM/output_data_reduc.osm --conf ./osm2pgrouting-${OSM2PGROUTING_VERSION}/${TYPEGRAPH} --dbname postgres --username postgres --clean
