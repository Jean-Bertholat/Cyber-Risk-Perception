# Liste des risques globaux
INTRODUCTION = """
Bienvenue dans l'application "Cartographie de la perception des risques cyber" !

Cette plateforme a pour objectif de mieux comprendre la répartition de la perception entre différents risques cyber, tels que le changement climatique, les crises économiques, les pandémies, et bien d'autres. En participant à cet exercice, vous aiderez à identifier les relations possibles entre ces risques et les conséquences qu’ils peuvent engendrer les uns sur les autres.

Comment cela fonctionne :

10 risques cyber vous seront proposés :
Pour chaque risque proposé, vous serez invité à sélectionner jusqu'à 5 autres risques qui pourraient être déclenchés si ce risque se matérialisait.

Complétez les interconnexions :
Vous verrez une liste déroulante pour chaque risque proposé. Vous devrez sélectionner entre 1 et 5 risques (les options "Autre" et "Aucun" peuvent être utilisées).

Soumission des données :
Une fois que vous avez complété toutes les interconnexions, cliquez sur le bouton pour visualiser vos résultats.

Vos réponses seront enregistrées de manière anonyme dans un fichier JSON pour une analyse ultérieure. Merci pour votre contribution à ce projet !
"""

GLOBAL_RISKS = [
"Phishing",
"Ransomware",
"Malware",
"Attaque par déni de service (DDoS)",
"Exploitation de vulnérabilités logicielles",
"Vol de données personnelles",
"Ingénierie sociale",
"Exploitation de systèmes obsolètes",
"Usurpation d'identité numérique",
"Réseaux privés virtuels compromis (VPN)",
"Attaque par brute force",
"Logiciels espions",
"Usurpation d'identité",
"Malware polymorphe",
"Vol de propriété intellectuelle",
"Attaque par ransomware de chaîne d’approvisionnement",
"Fuite de données",
"Exploitation de failles de sécurité du réseau",
"Usurpation de site web (pharming)",
"Attaque par injection SQL",
"Réseaux sans fil compromis (Wi-Fi)",
"Menaces contre les infrastructures critiques",
"Exploitation de mot de passe faible",
"Attaque par spyware",
"Usurpation de numéro de téléphone (SIM swap)",
"Exploitation de systèmes industriels (ICS) compromis",
"Vol de jetons d’accès (token theft)",
"Exploitation de vulnérabilités de services cloud",
"Exploitation de failles dans la chaîne d’approvisionnement en logiciels",
"Exploitation de vulnérabilités de logiciels tiers",
"Risque de cybersécurité dans l’Internet des objets (IoT)",
"Menaces de l’ingénierie sociale via les réseaux sociaux",
"Vol de données de cartes bancaires",
"Exploitation de l’intelligence artificielle (IA) pour les cyberattaques",
"Attaque via les APIs non sécurisées",
"Cyber-espionnage industriel",
"Exploitation de la virtualisation",
"Attaque de type man-in-the-middle"
"Autre",
"Aucun"
]

