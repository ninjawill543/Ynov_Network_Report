# Etat des lieux du réseau Ynov

- [I - Introduction](#i---introduction)
    - [Contexte du projet](#contexte-du-projet)
    - [Objectifs de l'état des lieux](#objectifs-de-létat-des-lieux)
- [II - Infrastructure réseau](#ii---infrastructure-réseau)
    - [Description de l'infrastructure](#description-de-linfrastructure)
        - [Réseau Wifi](#réseau-wifi)
        - [Réseau Bluetooth](#réseau-bluetooth)
    - [Équipements réseau](#équipements-réseau)
- [III - Sécurité du réseau](#iii---sécurité-du-réseau)
    - [Mesures de sécurité actuelles](#mesures-de-sécurité-actuelles)
    - [Vulnérabilités et menaces potentielles](#vulnérabilités-et-menaces-potentielles)
        - [MITM potentiel via les télévisions](#mitm-potentiel-via-les-télévisions)
    - [Recommandations à mettre en place](#recommandations-à-mettre-en-place)
- [IV - Conclusion](#iv---conclusion)

# I - Introduction

![](images/mr_robot.gif)

## Contexte du projet

Se projet est un exercice visant à explorer et à analyser le réseau Ynov en respectant des ordres strictes afin de garantir un comportement éthique et légal. L'objectif principal est de collecter des informations sur le réseau tout en évitant toute action agressive, inappropriée ou illégale. Nous avons été organisés en deux groupes, chacun composé d'environ cinq étudiants

## Objectifs de l'état des lieux

 - Réaliser un état des lieux du réseau YNOV en effectuant des prises d'informations en situation réelle.
 - Identifier les éléments à risque en termes de sécurité et mettre en évidence les vulnérabilités potentielles.
 - Agir de manière responsable et discret, sans se prendre pour des agents secrets

![](images/agent.gif)

# II - Infrastructure réseau

## Description de l'infrastructure

### Réseau Wifi

L'infrastructure du réseau Ynov est conçue pour prendre en charge un nombre significatif d'appareils connectés. Le réseau principal a pour addresse réseau 10.33.64.0/20, avec donc un total de 4096 adresses IP uniques. Nous avons identifié environ 600 appareils connectés à ce réseau, vous pouvez aller consulter la liste des addresses ip et des adresses mac correspondants dans ce ![fichier](files/Live_Devices_Main_Network.txt)

Cependant, il est important de noter qu'il y avait également un deuxième réseau en place, spécialement destiné aux télévisions et à quelques autres appareils. Pour identifier ce réseau, nous avons observer les adresses IP qui s'affichaient sur chaque télévision lorsque nous les allumions. Le réseau secondaire a donc pour adresse réseau le 10.33.80.0/20. Vous pouvez consulter la liste des appareils connectés à ce réseau dans ce ![fichier] (files/Live_Devices_Secondary_Network.txt)

### Réseau Bluetooth

Après avoir scanné toutes les adresses ip des reseaux wifi et ethernet, nous avons choisi de documenter les appareils bluetooth présent dans le batiment. 

![](images/bluetooth.gif)

#### Scan

En utilisant l'outil `bluetoothctl`, il suffisait de se déplacer dans le batiment et de sauvegarder les appareils détectés par le scan :

```sh
$ bluetoothctl scan on

$ bluetoothctl devices > device01.txt
```

#### Traitement des données

Pour interpréter les résultats obtenus nous avons utilisé les réorganiser et analyser à l'aide de ![scripts Python](files/orderDevices.py).

#### Centralisation des données

Tout d'abord il faut rassembler les données dans un seul fichier, en évitant les doublons (les mêmes appareils peuvent apparaîttrent dans plusieurs scans).


```python
// Ouvre un fichier

def openFiles(x: str) -> []:
    file = open("/devices"+x+".txt", "r")
    result = file.read().split("\n")
    file.close()
    return result

// Ouvre tous les fichiers à l'aide de openFiles

def openAllFiles() -> []:
    allFiles = []
    for i in range(1, 16):
        number = str(i)
        if i < 10:
            number = "0" + number
        allFiles += openFiles(number)
    return allFiles

// Retire les répétitions des mêmes appareils

def deleteDoubleEntries() -> []:
    allDevices = openAllFiles()
    i = 0
    while (i < len(allDevices)):
        k = 0
        while (k < len(allDevices)):
            if (i != k) and ((allDevices[i] == allDevices[k]) or (allDevices[k] == "")):
                allDevices = allDevices[:k] + allDevices[k+1:]
            else:
               k += 1
        i += 1
    return allDevices

// Ecrit toutes les macs dans allDevices.txt 

def writeAllDevices():
    allDevices = deleteDoubleEntries()
    f = open("allDevices.txt", "a")
    for i in allDevices:
        f.write(i + "\n")
        f.close()
```


On obtient [ce rendu final](files/allDevices.txt) contenant les addresses MAC de 565 appareils.

#### MAC address lookup

En utilisant l'api api.macvendors.com on peut maintenant essayer de trouver les fabricants des cartes réseaux trouvées.

```python
// Envoie un requête à l'api
def macLookup(file: [], index: int) -> str:
    request = site + getMac(file, index)
    result = get(request).text
    if ("Not Found" in result) or (len(result) == 0):
        return "Not found"
    else:
        return result

// Formate le résultat envoyé par l'api (pour enlever les espaces)
def formatVendor(vendor: str) -> str:
    return "_".join(vendor.split(" "))

// Appel macLookup pour toutes les macs des appareils donnés
def reverseAllMac(allDevices: []):
    allVendors = ""
    for i in range(0, len(allDevices)-1):
        time.sleep(10) // Evite de spam l'api
        vendor = formatVendor(macLookup(allDevices, i))
        
        // Si l'api est pas gentille attends 10 secondes en espérant que maintenant l'api sera gentille
        while vendor == '{"errors":{"detail":"Too_Many_Requests","message":"Please_slow_down_your_requests_or_upgrade_your_plan_at_https://macvendors.com"}}':
            time.sleep(10)
            vendor = formatVendor(macLookup(allDevices, i))
        allVendors += vendor + "\n"
    
    // Ecrit le résultat dans allVendors.txt
    f = open("allVendors.txt", "a")
    f.write(allCendors)
    f.close()
```

On obtient [ce rendu final](files/allVendors.txt) contenant les constructeurs des cartes réseaux trouvées chaque ligne de ce fichier corresponds à l'appareil de la même ligne dans [le rendu précédent](files/allDevices.txt).

#### Organisation des addresses MACs par constructeurs

Il faut maintenant regrouper les addresses MACs par constructeurs pour interpréter les données.

```python
def writeVendors():
    file = open("allVendors.txt", "r")
    vendors = file.read().split("\n")
    file.close()

    file = open("allDevices.txt", "r")
    devices = file.read().split("\n")
    file.close()

    for i in range(0, len(devices)-1):
        file = open("Vendors/"+vendors[i]+".txt", "a")
        file.write(devices[i] + "\n")
        file.close()
```

On obtient [tous ces fichiers](files/Vendors/).

#### Interprétation des données

Nous avons un total de 565 appareils parmis lesquels se trouvent 17 catégories.

### [Apple](files/Vendors/Apple_Inc.txt)

1 MacBook Pro et 1 MacBook Air avec les noms de familles des propriétaires dans le nom de l'appareil.

### [Aruba Hewlett Packard](files/Vendors/Aruba_a_Hewlett_Packard_Enterprise_Company.txt)

30 appareils qui semblent être des routeurs wifi d'après cette page : https://www.arubanetworks.com/resources/case-studies/hewlett-packard-enterprise/

### [AzureWave Technology](files/Vendors/AzureWave_Technology_Inc.txt)

2 appareils qui semblent être des ordinateurs portables en conséquence de leurs noms.

### [Bose](files/Vendors/Bose_Corporation.txt)

1 casque Bose.

### [Cloud Technology Singapore](files/Vendors/CLOUD_NETWORK_TECHNOLOGY_SINGAPORE_PTE._LTD.txt)

1 ordinateur d'après son nom.

### [Cypress Semiconducteur](files/Vendors/CYPRESS_SEMICONDUCTOR.txtt)

10 appareils inconnus semblant appartenir à Ynov d'après leurs noms. Potentiellement les TVs utilisés à travers le batiment.

### [GuangDong Oppo Mobile Telecommunication](files/Vendors/GUANGDONG_OPPO_MOBILE_TELECOMMUNICATIONS_CORP.LTD.txt)

7 smartphones.

### [Intel](files/Vendors/Intel_Corporate.txt)

14 ordinateurs.

### [Liteon technology](files/Vendors/Liteon_Technology_Corporation.txt)

4 appareils Liteon inconnus.

### [Nintendo](files/Vendors/Nintendo_Co.Ltd.txt)

4 Pokemon Go Plus.

### [Not found](files/Vendors/Not_found.txt)

386 appareils dont l'addresse MAC n'a pas été identifié. Parmis ces appareils certains possèdent des noms permettant d'émettre des hypothèses :

```sh
Device 4D:77:38:D3:E2:37 JBL TUNE6 # casque JBL
Device 52:B7:D9:E8:DC:86 JBL LIVE660NC-LE # casque JBL
Device 55:69:56:F8:CB:39 Galaxy Watch5 (FN9R) # montre connecté Samsung
Device 53:86:AA:DC:D4:56 LE-Bose AE2 SoundLink # casque Bose
Device 69:75:BB:85:E4:2F JBL TUNE230NC TWS-LE # écouteurs JBL
Device FE:89:46:7F:70:FF BV6600 # smartphone Blackview
Device C0:9D:FA:E5:10:08 LE-Philips TAT5506 # écouteurs Philips
Device 54:E1:70:A4:99:BF Galaxy Watch5 (9GGT) # Montre connecté Samsung
Device 44:BB:12:58:F3:2D JBL TUNE130NC TWS-LE # écouteurs JBL
Device 45:E7:65:3B:F2:1F JBL LIVE300TWS-LE # écouteurs JBL
```

### [OnePlus](files/Vendors/OnePlus_Technology_Shenzhen_Co._Ltd.txt)

5 smartphone OnePlus.

### [Polar Electro](files/Vendors/Polar_Electro_Oy.txt)

1 équipement d'entraînement sportif.

### [Realme](files/Vendors/Realme_Chongqing_Mobile_Telecommunications_Corp.Ltd.txt)

1 smartphone Realme.

### [Salto systems](files/Vendors/SALTO_SYSTEMS_S.L.txt)

95 serrures electroniques Salto.

### [Samsung](files/Vendors/Samsung_Electronics_Co.Ltd.txt)

1 smartphone Samsung.

### [Sony](files/Vendors/Sony_Home_EntertainmentSound_Products_Inc.txt)

2 casques Sony.


## Équipements réseau

Après avoir scanné l'adresse IP de la télévision dans la salle 201, nous pouvons constater que les ports 1443 et 8000 sont accessibles via un navigateur Web.

```bash
m4ul@thinkpad:~$ nmap 10.33.81.194
Starting Nmap 7.80 ( https://nmap.org ) at 2023-11-06 10:23 CET
Nmap scan report for 10.33.81.194
Host is up (0.0030s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE
1080/tcp open  socks
1443/tcp open  ies-lm
5000/tcp open  upnp
5555/tcp open  freeciv
8000/tcp open  http-alt
8600/tcp open  asterix
```

En allant regarder cette adresse ip `10.33.81.194:1443` via un navigateur web, on tombe sur le site `eshare.app`, qui est en fait hebergé en local sur la télévision, en https. Ce site nous permet normalement de partager notre ecran sur la télé, mais malheuresement, le site hebergé nous renvoie tout simplement un message d'erreur `Receiver is offline, please try again`, à chaque fois qu'on essaie de se connecter.

Le port 8000 est aussi ouvert et consultable via un navigateur web `10.33.81.194:8000`, cette fois par contre étant en http. Ce site nous permet d'installer le client mobile de Eshare, afin de pouvoir partager notre écran. Vous pouvez lire une explication de la vulnerabilité que ce site contient [ici](#mitm-potentiel-via-les-télévisions)

Nous avons ensuite scanné le réseaux secondaire afin de trouver les adresses ip de chaque télévision actuellement allumée. 
```bash
m4ul@thinkpad:~$ sudo nmap 10.33.80.0/20 -p1443 --open
```
Nous avons choisi de filtrer toutes les appareils afin de voir que ceux avec le port 1443 d'ouvert, c'est à dire le port utilisé sur chaque télévision afin qu'un utilisateur puisse se connecter. Vous pouvez consulter la liste des adresses ip des télés ![ici](files/Live_TVs_Secondary_Network.txt)



# III - Sécurité du réseau

## Mesures de sécurité actuelles

## Vulnérabilités et menaces potentielles

### MITM potentiel via les télévisions

## Recommandations à mettre en place

# IV - Conclusion



