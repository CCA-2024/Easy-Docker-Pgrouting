import subprocess
import os

class OsmComsumer:
    def __init__(self)->None:
        self.volume_path = "./OSMs"
        
    def run_file(self)-> str:
        '''Verifica se o diretorio é valido'''
        try: 
            if os.path.exists(self.volume_path):
                print(self.volume_path)
                for filename in os.listdir(self.volume_path):
                    filepath = os.path.join(self.volume_path, filename)
                    command = f"osm2pgrouting --f .{filepath} --conf ./osm2pgrouting-2.3.8/mapconfig_for_cars.xml --host PGROUTING --dbname postgres --schema public --username postgres --password cca_roteirizador --port 5432 --addnodes --attributes --tags --chunk 1000"
                    print(f"\Insert: {command}")
                    result = subprocess.run(command.split(' '), capture_output=True, text=True, check=True)
                    print(result.stdout)
                    print(result.stderr)
        except Exception as e:
            print('Deu errroo', e)