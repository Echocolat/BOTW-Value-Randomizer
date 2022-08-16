import json
from bcml import util
import pathlib
import oead

def getValuePools():

    with open("fileList.json","r") as f:
        file_list = json.loads(f.read())

    poolWeaponLife, poolWeaponPower, poolShieldGuard, poolEnemyLife, poolEnemyPower, poolArmorType, poolItemType, poolCureItem, poolEffectiveTime, poolArmorDefence = [], [], [], [], [], [], [], [], [], []

    for File in file_list['Materials']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        for file in sarc.get_files():
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if 'CureItem' in dataFile.objects:
                    poolCureItem.append(dataFile.objects['CureItem'].params['HitPointRecover'].v)
                    poolItemType.append([str(dataFile.objects['CureItem'].params['EffectType'].v),dataFile.objects['CureItem'].params['EffectLevel'].v])
                    if dataFile.objects['CureItem'].params['EffectiveTime'].v != 0:
                        poolEffectiveTime.append(dataFile.objects['CureItem'].params['EffectiveTime'].v)

    for File in file_list['Armors']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        for file in sarc.get_files():
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                poolArmorDefence.append(dataFile.objects['Armor'].params['DefenceAddLevel'].v)
                poolArmorType.append([str(dataFile.objects['ArmorEffect'].params['EffectType'].v),dataFile.objects['ArmorEffect'].params['EffectLevel'].v])

    for File in file_list['Enemies']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        for file in sarc.get_files():
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if 'General' in dataFile.objects:
                    poolEnemyLife.append(dataFile.objects['General'].params['Life'].v)
                if 'Enemy' in dataFile.objects:
                    poolEnemyPower.append(dataFile.objects['Enemy'].params['Power'].v)

    for File in file_list['Weapons']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        for file in sarc.get_files():
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                if 'General' in dataFile.objects:
                    poolWeaponLife.append(dataFile.objects['General'].params['Life'].v)
                if 'Attack' in dataFile.objects and not 'Shield' in file.name:
                    poolWeaponPower.append(dataFile.objects['Attack'].params['Power'].v)
                if 'WeaponCommon' in dataFile.objects and 'Shield' in file.name:
                    poolShieldGuard.append(dataFile.objects['WeaponCommon'].params['GuardPower'].v)

    return poolWeaponLife, poolWeaponPower, poolShieldGuard, poolEnemyLife, poolEnemyPower, poolArmorType, poolItemType, poolCureItem, poolEffectiveTime, poolArmorDefence

def main():
    print(getValuePools())

if __name__ == '__main__':
    main()