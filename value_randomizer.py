import getValuePools
import oead
from bcml import util
import json
import pathlib
import random
from bcml.dev import create_bnp_mod
from bcml.install import install_mod, link_master_mod

with open("filelist.json","r") as f:
    file_list = json.loads(f.read())

poolWeaponLife, poolWeaponPower, poolShieldGuard, poolEnemyLife, poolEnemyPower, poolArmorType, poolItemType, poolCureItem, poolEffectiveTime, poolArmorDefence = getValuePools.getValuePools()

for List in [poolWeaponLife, poolWeaponPower, poolShieldGuard, poolEnemyLife, poolEnemyPower, poolArmorType, poolItemType, poolCureItem, poolEffectiveTime, poolArmorDefence]:
    random.shuffle(List)

allModified = {}

def modifyMaterials():

    for File in file_list['Materials']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        newFilePath = 'BOTW Value Randomizer/content/Actor/Pack/' + File
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
        for file in sarc.get_files():
            sarc_writer.files[file.name] = file.data.tobytes()
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                allModified[File.replace('.sbactorpack','')] = {}
                if 'CureItem' in dataFile.objects:
                    dataFile.objects['CureItem'].params['HitPointRecover'] = poolCureItem.pop()
                    allModified[File.replace('.sbactorpack','')]['Health'] = dataFile.objects['CureItem'].params['HitPointRecover'].v
                    effectData = poolItemType.pop()
                    dataFile.objects['CureItem'].params['EffectType'] = oead.FixedSafeString32(effectData[0])
                    allModified[File.replace('.sbactorpack','')]['EffectType'] = str(dataFile.objects['CureItem'].params['EffectType'].v)
                    dataFile.objects['CureItem'].params['EffectLevel'] = effectData[1]
                    allModified[File.replace('.sbactorpack','')]['EffectLevel'] = dataFile.objects['CureItem'].params['EffectLevel'].v
                    if effectData[0] != 'None':
                        dataFile.objects['CureItem'].params['EffectiveTime'] = poolEffectiveTime.pop()
                    else:
                        dataFile.objects['CureItem'].params['EffectiveTime'] = 0
                    allModified[File.replace('.sbactorpack','')]['Time'] = dataFile.objects['CureItem'].params['EffectiveTime'].v
                sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
        _, sarc_bytes = sarc_writer.write()
        with open(newFilePath,'wb') as f:
            f.write(oead.yaz0.compress(sarc_bytes))

def modifyArmors():

    for File in file_list['Armors']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        newFilePath = 'BOTW Value Randomizer/content/Actor/Pack/' + File
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
        for file in sarc.get_files():
            sarc_writer.files[file.name] = file.data.tobytes()
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                allModified[File.replace('.sbactorpack','')] = {}
                effectData = poolArmorType.pop()
                dataFile.objects['ArmorEffect'].params['EffectType'] = oead.FixedSafeString32(effectData[0])
                allModified[File.replace('.sbactorpack','')]['Type'] = str(dataFile.objects['ArmorEffect'].params['EffectType'].v)
                dataFile.objects['ArmorEffect'].params['EffectLevel'] = effectData[1]
                allModified[File.replace('.sbactorpack','')]['EffectLevel'] = dataFile.objects['ArmorEffect'].params['EffectLevel'].v
                dataFile.objects['Armor'].params['DefenceAddLevel'] = poolArmorDefence.pop()
                allModified[File.replace('.sbactorpack','')]['Defense'] = dataFile.objects['Armor'].params['DefenceAddLevel'].v
                sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
        _, sarc_bytes = sarc_writer.write()
        with open(newFilePath,'wb') as f:
            f.write(oead.yaz0.compress(sarc_bytes))

def modifyEnemies():
    
    for File in file_list['Enemies']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        newFilePath = 'BOTW Value Randomizer/content/Actor/Pack/' + File
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
        for file in sarc.get_files():
            sarc_writer.files[file.name] = file.data.tobytes()
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                allModified[File.replace('.sbactorpack','')] = {}
                if 'General' in dataFile.objects:
                    dataFile.objects['General'].params['Life'] = poolEnemyLife.pop()
                    allModified[File.replace('.sbactorpack','')]['Life'] = dataFile.objects['General'].params['Life'].v
                if 'Enemy' in dataFile.objects:
                    dataFile.objects['Enemy'].params['Power'] = poolEnemyPower.pop()
                    allModified[File.replace('.sbactorpack','')]['Power'] = dataFile.objects['Enemy'].params['Power'].v
                sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
        _, sarc_bytes = sarc_writer.write()
        with open(newFilePath,'wb') as f:
            f.write(oead.yaz0.compress(sarc_bytes))

def modifyWeapons():

    for File in file_list['Weapons']:
        filePath = util.get_game_file('Actor/Pack/' + File)
        newFilePath = 'BOTW Value Randomizer/content/Actor/Pack/' + File
        data: bytes = pathlib.Path(filePath).read_bytes()
        data = oead.yaz0.decompress(data)
        sarc = oead.Sarc(data)
        sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
        for file in sarc.get_files():
            sarc_writer.files[file.name] = file.data.tobytes()
            if "bgparamlist" in file.name:
                dataFile: bytes = file.data
                dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
                allModified[File.replace('.sbactorpack','')] = {}
                if 'General' in dataFile.objects:
                    dataFile.objects['General'].params['Life'] = poolWeaponLife.pop()
                    allModified[File.replace('.sbactorpack','')]['Life'] = dataFile.objects['General'].params['Life'].v
                if 'Attack' in dataFile.objects and not 'Shield' in file.name:
                    dataFile.objects['Attack'].params['Power'] = poolWeaponPower.pop()
                    allModified[File.replace('.sbactorpack','')]['Power'] = dataFile.objects['Attack'].params['Power'].v
                if 'WeaponCommon' in dataFile.objects and 'Shield' in file.name:
                    dataFile.objects['WeaponCommon'].params['GuardPower'] = poolShieldGuard.pop()
                    allModified[File.replace('.sbactorpack','')]['Guard'] = dataFile.objects['WeaponCommon'].params['GuardPower'].v
                if 'MasterSword' in dataFile.objects:
                    dataFile.objects['MasterSword'].params['TrueFormAttackPower'] = dataFile.objects['Attack'].params['Power'].v + random.randint(-5,30)
                    allModified[File.replace('.sbactorpack','')]['TrueFormAttackPower'] = dataFile.objects['MasterSword'].params['TrueFormAttackPower'].v
                sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
        _, sarc_bytes = sarc_writer.write()
        with open(newFilePath,'wb') as f:
            f.write(oead.yaz0.compress(sarc_bytes))

def actorInfoModify(listModif):
    data: bytes = pathlib.Path(util.get_game_file('Actor/ActorInfo.product.sbyml')).read_bytes()
    data = oead.byml.from_binary(oead.yaz0.decompress(data))
    for i in range(len(data['Actors'])):
        if data['Actors'][i]['name'] in listModif:
            if 'Guard' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['weaponCommonGuardPower'] = oead.S32(listModif[data['Actors'][i]['name']]['Guard'])
            if 'Power' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['attackPower'] = oead.S32(listModif[data['Actors'][i]['name']]['Power'])
            if 'Life' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['generalLife'] = oead.S32(listModif[data['Actors'][i]['name']]['Life'])
            if 'TrueFormAttackPower' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['masterSwordTrueFormAttackPower'] = oead.S32(listModif[data['Actors'][i]['name']]['TrueFormAttackPower'])
            if 'Type' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['armorEffectEffectType'] = listModif[data['Actors'][i]['name']]['Type']
            if 'EffectLevel' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['armorEffectEffectLevel'] = oead.S32(listModif[data['Actors'][i]['name']]['EffectLevel'])
            if 'Defense' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['armorDefenceAddLevel'] = oead.S32(listModif[data['Actors'][i]['name']]['Defense'])
            if 'Health' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['cureItemHitPointRecover'] = oead.S32(listModif[data['Actors'][i]['name']]['Health'])
            if 'EffectType' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['cureItemEffectType'] = listModif[data['Actors'][i]['name']]['EffectType']
            if 'EffectLevel' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['cureItemEffectLevel'] = oead.S32(listModif[data['Actors'][i]['name']]['EffectLevel'])
            if 'EffectiveTime' in listModif[data['Actors'][i]['name']]:
                data['Actors'][i]['cureItemEffectiveTime'] = oead.S32(listModif[data['Actors'][i]['name']]['EffectiveTime'])
    with open('BOTW Value Randomizer/content/Actor/ActorInfo.product.sbyml', 'wb') as f:
        f.write(oead.yaz0.compress(oead.byml.to_binary(data,True)))

def bnpBuilder(input_path,output_path):
    create_bnp_mod(
        mod = pathlib.Path(input_path),
        output = pathlib.Path(output_path),
        meta = json.loads(pathlib.Path(f'{input_path}\\info.json').read_text()),
        options={}
    )

def bnpInstaller(input_path):
    remerge = True
    install_mod(
        pathlib.Path(input_path),
        merge_now=remerge)

    if remerge == True:
        link_master_mod()

def main():
    if input('Do you want to randomize properties of materials ? y for yes, anything else for no : ') == 'y':
        modifyMaterials()
        print('Materials values randomized!')
    if input('Do you want to randomize defence and effect of armors ? y for yes, anything else for no : ') == 'y':
        modifyArmors()
        print('Armors values randomized!')
    if input('Do you want to randomize health and damage of enemies ? y for yes, anything else for no : ') == 'y':
        modifyEnemies()
        print('Enemies values randomized!')
    if input('Do you want to randomize dura and damage of weapons ? y for yes, anything else for no : ') == 'y':
        modifyWeapons()
        print('Weapons values randomized!')
    actorInfoModify(allModified)
    print('Actor/ActorInfo.product.sbyml modified !')
    if input('Do you want to install it with BCML ? y for yes, anything else for no : ') == 'y':
        bnpBuilder("BOTW Value Randomizer","ValueRandomizerv1.bnp")
        bnpInstaller("ValueRandomizerv1.bnp")
    input('Press enter to quit...')

if __name__ == '__main__':
    main()