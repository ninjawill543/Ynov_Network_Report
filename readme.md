# Etat des lieux du réseau Ynov

- [I - Introduction](#i---introduction)
    - [Contexte du projet](#contexte-du-projet)
    - [Objectifs de l'état des lieux](#objectifs-de-létat-des-lieux)
- [II - Infrastructure réseau](#ii---infrastructure-réseau)
    - [Description de l'infrastructure](#description-de-linfrastructure)
    - [Topologie du réseau](#topologie-du-réseau)
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

L'infrastructure du réseau Ynov est conçue pour prendre en charge un nombre significatif d'appareils connectés. Le réseau principal a pour addresse réseau 10.33.64.0/20, avec donc un total de 4096 adresses IP uniques. Nous avons identifié environ 600 appareils connectés à ce réseau, vous pouvez aller consulter la liste des addresses ip et des adresses mac correspondants dans ce ![fichier](files/Live_Devices_Main_Network.txt)

Cependant, il est important de noter qu'il y avait également un deuxième réseau en place, spécialement destiné aux télévisions et à quelques autres appareils. Pour identifier ce réseau, nous avons observer les adresses IP qui s'affichaient sur chaque télévision lorsque nous les allumions. Le réseau secondaire a donc pour adresse réseau le 10.33.80.0/20. Vous pouvez consulter la liste des appareils connectés à ce réseau dans ce fichier: Live_Devices_Secondary_Network.txt

## Topologie du réseau

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
Nous avons choisi de filtrer toutes les appareils afin de voir que ceux avec le port 1443 d'ouvert, c'est à dire le port utilisé sur chaque télévision afin qu'un utilisateur puisse se connecter. Vous pouvez consulter la liste des adresses ip des télés ici: Live_TVs_Secondary_Network.txt



# III - Sécurité du réseau

## Mesures de sécurité actuelles

## Vulnérabilités et menaces potentielles

### MITM potentiel via les télévisions

## Recommandations à mettre en place

# IV - Conclusion



