import oead
import os
import pathlib
import random

rangeWeaponLife = []
rangeWeaponPower = []
rangeShieldGuard = []
rangeEnemyLife = []
rangeEnemyPower = []
armorDefenses = [[1,2,3,4,5],[2,4,5,7,8],[3,6,8,12,14],[4,9,12,18,22],[5,16,18,28,32]]
for i in range(2):
    rangeEnemyLife.append(random.randint(3000,7500))
    rangeEnemyPower.append(random.randint(42,50))
    rangeWeaponLife.append(random.randint(101,120))
    rangeWeaponPower.append(random.randint(72,86))
    rangeShieldGuard.append(random.randint(72,86))
for i in range(5):
    rangeEnemyLife.append(random.randint(1000,3000))
    rangeEnemyPower.append(random.randint(35,42))
    rangeWeaponLife.append(random.randint(80,101))
    rangeWeaponPower.append(random.randint(60,72))
    rangeShieldGuard.append(random.randint(60,72))
for i in range(10):
    rangeEnemyLife.append(random.randint(400,1000))
    rangeEnemyPower.append(random.randint(29,35))
    rangeWeaponLife.append(random.randint(55,80))
    rangeWeaponPower.append(random.randint(48,60))
    rangeShieldGuard.append(random.randint(48,60))
for i in range(25):
    rangeEnemyLife.append(random.randint(120,400))
    rangeEnemyPower.append(random.randint(23,35))
    rangeWeaponLife.append(random.randint(35,55))
    rangeWeaponPower.append(random.randint(36,48))
    rangeShieldGuard.append(random.randint(36,48))
for i in range(40):
    rangeEnemyLife.append(random.randint(40,120))
    rangeEnemyPower.append(random.randint(16,23))
    rangeWeaponLife.append(random.randint(18,35))
    rangeWeaponPower.append(random.randint(22,36))
    rangeShieldGuard.append(random.randint(22,36))
for i in range(20):
    rangeEnemyLife.append(random.randint(10,40))
    rangeEnemyPower.append(random.randint(11,16))
    rangeWeaponLife.append(random.randint(12,18))
    rangeWeaponPower.append(random.randint(11,22))
    rangeShieldGuard.append(random.randint(11,22))
for i in range(8):
    rangeEnemyLife.append(random.randint(1,10))
    rangeEnemyPower.append(random.randint(1,11))
    rangeWeaponLife.append(random.randint(1,12))
    rangeWeaponPower.append(random.randint(1,11))
    rangeShieldGuard.append(random.randint(1,11))

allWeaponsModified = {}
allEnemiesModified = {}
allArmorsModified = {}
allMaterialsModified = {}
TypesArmors = ['None', 'ResistLightning', 'AttackUp', 'SnowMove', 'ClimbSpeed', 'SwimSpeed', 
'ResistHotAndWakeWind', 'ResistElectric', 'ResistCold', 'ResistElectricAndResistAncient', 
'ResistAncient', 'ResistBurnAndResistAncient', 'ResistColdAndResistAncient', 'ResistFreeze', 
'Quietness', 'ClimbSpeedAndBeamPowerUp', 'ResistHot', 'SandMove', 'SwimSpeedAndResistAncient', 'ResistBurn']
TypesItems = ['Fireproof', 'ExGutsMaxUp', 'ResistCold', 'ResistElectric', 'AttackUp', 'LifeMaxUp', 'DefenseUp', 
'Quietness', 'None', 'MovingSpeed', 'ResistHot', 'GutsRecover']

def modify_weapon(filePath):
    data: bytes = pathlib.Path(filePath).read_bytes()
    data = oead.yaz0.decompress(data)
    sarc = oead.Sarc(data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    for file in sarc.get_files():
        sarc_writer.files[file.name] = file.data.tobytes()
        if ".bgparamlist" in file.name:
            dataFile: bytes = file.data
            dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
            allWeaponsModified[filePath[34:].replace('.sbactorpack','')] = {}
            if 'General' in dataFile.objects:
                dataFile.objects['General'].params['Life'] = random.choice(rangeWeaponLife)
                allWeaponsModified[filePath[34:].replace('.sbactorpack','')]['Life'] = dataFile.objects['General'].params['Life'].v
            if 'Attack' in dataFile.objects and not 'Shield' in file.name:
                dataFile.objects['Attack'].params['Power'] = random.choice(rangeWeaponPower)
                allWeaponsModified[filePath[34:].replace('.sbactorpack','')]['Power'] = dataFile.objects['Attack'].params['Power'].v
            if 'WeaponCommon' in dataFile.objects and 'Shield' in file.name:
                dataFile.objects['WeaponCommon'].params['GuardPower'] = random.choice(rangeShieldGuard)
                allWeaponsModified[filePath[34:].replace('.sbactorpack','')]['Guard'] = dataFile.objects['WeaponCommon'].params['GuardPower'].v
            if 'MasterSword' in dataFile.objects:
                dataFile.objects['MasterSword'].params['TrueFormAttackPower'] = random.choice(rangeWeaponPower)
                dataFile.objects['MasterSword'].params['TrueFormBreakRatio'] = random.uniform(0.1,0.6)
                allWeaponsModified[filePath[34:].replace('.sbactorpack','')]['TrueFormAttackPower'] = dataFile.objects['MasterSword'].params['TrueFormAttackPower'].v
                allWeaponsModified[filePath[34:].replace('.sbactorpack','')]['TrueFormBreakRatio'] = dataFile.objects['MasterSword'].params['TrueFormBreakRatio'].v
            sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
    _, sarc_bytes = sarc_writer.write()
    with open(filePath,'wb') as f:
        f.write(oead.yaz0.compress(sarc_bytes))

def modify_enemy(filePath):
    data: bytes = pathlib.Path(filePath).read_bytes()
    data = oead.yaz0.decompress(data)
    sarc = oead.Sarc(data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    for file in sarc.get_files():
        sarc_writer.files[file.name] = file.data.tobytes()
        if ".bgparamlist" in file.name:
            dataFile: bytes = file.data
            dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
            allEnemiesModified[filePath[34:].replace('.sbactorpack','')] = {}
            if 'General' in dataFile.objects:
                dataFile.objects['General'].params['Life'] = random.choice(rangeEnemyLife)
                allEnemiesModified[filePath[34:].replace('.sbactorpack','')]['Life'] = dataFile.objects['General'].params['Life'].v
            if 'Enemy' in dataFile.objects:
                dataFile.objects['Enemy'].params['Power'] = random.choice(rangeEnemyPower)
                allEnemiesModified[filePath[34:].replace('.sbactorpack','')]['Power'] = dataFile.objects['Enemy'].params['Power'].v
            sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
    _, sarc_bytes = sarc_writer.write()
    with open(filePath,'wb') as f:
        f.write(oead.yaz0.compress(sarc_bytes))

def modify_armor(filePath):
    data: bytes = pathlib.Path(filePath).read_bytes()
    data = oead.yaz0.decompress(data)
    sarc = oead.Sarc(data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    for file in sarc.get_files():
        sarc_writer.files[file.name] = file.data.tobytes()
        if ".bgparamlist" in file.name:
            dataFile: bytes = file.data
            dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
            allArmorsModified[filePath[34:].replace('.sbactorpack','')] = {}
            dataFile.objects['ArmorEffect'].params['EffectType'] = oead.FixedSafeString32(random.choice(TypesArmors))
            allArmorsModified[filePath[34:].replace('.sbactorpack','')]['Type'] = str(dataFile.objects['ArmorEffect'].params['EffectType'].v)
            dataFile.objects['ArmorEffect'].params['EffectLevel'] = random.choice([1,2])
            allArmorsModified[filePath[34:].replace('.sbactorpack','')]['EffectLevel'] = dataFile.objects['ArmorEffect'].params['EffectLevel'].v
            dataFile.objects['Armor'].params['DefenceAddLevel'] = random.choice(armorDefenses[dataFile.objects['Armor'].params['StarNum'].v - 1])
            allArmorsModified[filePath[34:].replace('.sbactorpack','')]['Defense'] = dataFile.objects['Armor'].params['DefenceAddLevel'].v
            sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
    _, sarc_bytes = sarc_writer.write()
    with open(filePath,'wb') as f:
        f.write(oead.yaz0.compress(sarc_bytes))

def modify_material(filePath):
    data: bytes = pathlib.Path(filePath).read_bytes()
    data = oead.yaz0.decompress(data)
    sarc = oead.Sarc(data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    for file in sarc.get_files():
        sarc_writer.files[file.name] = file.data.tobytes()
        if ".bgparamlist" in file.name:
            dataFile: bytes = file.data
            dataFile = oead.aamp.ParameterIO.from_binary(dataFile)
            allMaterialsModified[filePath[34:].replace('.sbactorpack','')] = {}
            if 'CureItem' in dataFile.objects:
                dataFile.objects['CureItem'].params['HitPointRecover'] = random.randint(0,24)
                allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['Health'] = dataFile.objects['CureItem'].params['HitPointRecover'].v
                dataFile.objects['CureItem'].params['EffectType'] = oead.FixedSafeString32(random.choice(TypesItems))
                allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['EffectType'] = str(dataFile.objects['CureItem'].params['EffectType'].v)
                if allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['EffectType'] == 'LifeMaxUp':
                    dataFile.objects['CureItem'].params['EffectLevel'] = random.randint(1,20)
                elif allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['EffectType'] in ['GutsRecover','ExGutsMaxUp']:
                    dataFile.objects['CureItem'].params['EffectLevel'] = random.randint(1,6)
                elif not allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['EffectType'] == 'None':
                    dataFile.objects['CureItem'].params['EffectLevel'] = random.randint(1,3)
                else:
                    dataFile.objects['CureItem'].params['EffectLevel'] = 0
                if 'EffectLevel' in dataFile.objects['CureItem'].params:
                    allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['EffectLevel'] = dataFile.objects['CureItem'].params['EffectLevel'].v
                dataFile.objects['CureItem'].params['EffectiveTime'] = random.choice([0,300,900,1200,1800,3000])
                allMaterialsModified[filePath[34:].replace('.sbactorpack','')]['Time'] = dataFile.objects['CureItem'].params['EffectiveTime'].v
            sarc_writer.files[file.name] = oead.aamp.ParameterIO.to_binary(dataFile)
    _, sarc_bytes = sarc_writer.write()
    with open(filePath,'wb') as f:
        f.write(oead.yaz0.compress(sarc_bytes))

def actorInfoModify(listModif):
    data: bytes = pathlib.Path('botwValueRandomizer\\content\\Actor\\ActorInfo.product.sbyml').read_bytes()
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
    with open('botwValueRandomizer\\content\\Actor\\ActorInfo.product.sbyml', 'wb') as f:
        f.write(oead.yaz0.compress(oead.byml.to_binary(data,True)))

def main():
    randomizeEnemies = input('Do you want to randomize HP and Attack of enemies ? y for yes, ignore for no : ') == 'y'
    randomizeWeapons =  input('Do you want to randomize Durability and Attack of weapons ? y for yes, ignore for no : ') == 'y'
    randomizeArmors = input('Do you want to randomize Defense and effect of armors ? y for yes, ignore for no : ') == 'y'
    randomizeMaterials = input('Do you want to randomize properties of materials ? y for yes, ignore for no : ') == 'y'
    for filename in os.listdir('botwValueRandomizer\\content\\Actor\\Pack\\'):
        if 'Weapon' in filename and not 'Enemy' in filename and randomizeWeapons:
            modify_weapon('botwValueRandomizer\\content\\Actor\\Pack\\'+filename)
        elif 'Enemy' in filename and randomizeEnemies and not 'Item' in filename:
            modify_enemy('botwValueRandomizer\\content\\Actor\\Pack\\'+filename)
        elif 'Armor' in filename and randomizeArmors:
            modify_armor('botwValueRandomizer\\content\\Actor\\Pack\\'+filename)
        elif ('Item' in filename or 'Animal_Insect' in filename) and randomizeMaterials:
            modify_material('botwValueRandomizer\\content\\Actor\\Pack\\'+filename)
    actorInfoModify(allWeaponsModified)
    actorInfoModify(allArmorsModified)
    actorInfoModify(allMaterialsModified)

if __name__ == '__main__':
    main()