import json
from bcml import util
import pathlib
import oead

def get_drop_files():
    
    with open("fileList.json","r") as f:
        file_list = json.loads(f.read())

    pool_drops = []

    for File in file_list['Enemies']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        for file in sarc.get_files():
            if ".bdrop" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                for table in list(dataFile.objects):
                    if not 'TableNum' in dataFile.objects[table].params:
                        pool_drops.append(dataFile.objects[table])
        
    return pool_drops

def main():
    print(get_drop_files())

if __name__ == '__main__':
    main()