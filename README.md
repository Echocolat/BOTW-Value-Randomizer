## BOTW Value Randomizer

This lets you randomize health and damage values for enemies and weapons, defense and effects for armors and / or health given and effects for materials.  

#### How to make it work

First, make sure you have the `oead` module installed (`pip install oead`). Then, if you :  

* want to randomize weapon values : Go into your BOTWUpdateFolder/content/Actor/Pack and grab all the files that start with "Weapon" except for those that have "Sheath" in the name.
* want to randomize enemy values : Go into your BOTWUpdateFolder/content/Actor/Pack and grab all the files that start with "Enemy".
* want to randomize armor values : Go into your BOTWUpdateFolder/content/Actor/Pack and grab all the files that start with "Armor".
* want to randomize material values : Go into your BOTWUpdateFolder/content/Actor/Pack and grab all the files that start with "Animal_Insect", "Item_Chilled", "Item_Roast", "Item_Enemy", "Item_FishGet", "Item_Fruit", "Item_InsectGet", "Item_Material", "Item_Meat", "Item_Mushroom", "Item_Ore", "Item_PlantGet", and the files "Item_Boiled_01.sbactorpack", "BeeHome.sbactorpack" and "Obj_FireWoodBundle".

Then, copy all of them and paste them in botwValueRandomizer/content/Actor/Pack.  

Finally, copy your BOTWUpdateFolder/content/Actor/ActorInfo.product.sbyml and paste it in botwValueRandomizer/content/Actor/Pack.  

Then you can launch the script, choose your options, (if it doesn't work somewhere feel free to contact me @Echocolat#9988 on Discord or on the Gamebanana post) after it finished, use BCML to install the mod (there is a rules.txt file in botwValueRandomizer/). Then enjoy !