# Benchmark de multiplication scalaire sur courbes elliptiques

## Description

Ce projet implémente et compare plusieurs méthodes de multiplication scalaire sur courbes elliptiques, en particulier sur la courbe standard **secp256k1**.

L’objectif est d’analyser l’impact du choix de la représentation des points sur les performances, en mesurant :

* le temps d’exécution ;
* le nombre de multiplications modulaires ;
* le nombre d’inversions modulaires.

La multiplication scalaire étudiée est :

```text
Q = kP
```

où `P` est un point de la courbe elliptique, `k` un scalaire de 256 bits et `Q` le point résultat.

## Objectifs

Les objectifs du projet sont :

* implémenter la multiplication scalaire sur une courbe elliptique ;
* comparer différentes représentations de points ;
* mesurer expérimentalement les performances ;
* compter les opérations coûteuses ;
* analyser le meilleur choix pour un environnement embarqué comme les smart cards.

Les méthodes comparées sont :

* coordonnées affines ;
* coordonnées projectives standard ;
* coordonnées de Jacobi ;
* Montgomery ladder.

## Courbe utilisée

La courbe utilisée pour les tests principaux est **secp256k1**, courbe elliptique utilisée notamment dans Bitcoin.

Elle est définie sur un corps fini premier par l’équation :

```text
y² = x³ + ax + b mod p
```

avec :

```text
a = 0
b = 7
```

Le nombre premier utilisé est :

```text
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
```

Le point générateur `G` est celui de la courbe secp256k1.

## Structure du projet

```text
projet-ecc/
│
├── affine.py
├── jacobian.py
├── projective.py
├── montgomery.py
├── field.py
├── curve.py
├── benchmark.py
├── main.py
├── gui.py
└── README.txt
```

## Rôle des fichiers

### `curve.py`

Ce fichier définit la classe `EllipticCurve`.

Il contient aussi la fonction `get_secp256k1()` qui initialise la courbe secp256k1 avec ses paramètres :

* le nombre premier `p` ;
* les coefficients `a` et `b` ;
* le point générateur `G`.

Il contient également des méthodes permettant de vérifier :

* si la courbe est non singulière ;
* si un point appartient à la courbe.

### `field.py`

Ce fichier contient la classe `FieldOps`, qui regroupe les opérations dans le corps fini :

* addition modulaire ;
* soustraction modulaire ;
* multiplication modulaire ;
* inversion modulaire.

Il permet aussi de compter :

* le nombre de multiplications modulaires ;
* le nombre d’inversions modulaires.

### `affine.py`

Ce fichier implémente la multiplication scalaire en coordonnées affines.

Les points sont représentés sous la forme :

```text
P = (x, y)
```

Cette représentation est simple, mais elle nécessite une inversion modulaire à chaque addition ou doublement de point.

Les inversions modulaires étant très coûteuses, cette méthode est généralement la moins performante.

### `projective.py`

Ce fichier implémente la multiplication scalaire en coordonnées projectives standard.

Un point est représenté sous la forme :

```text
P = (X, Y, Z)
```

avec la correspondance affine :

```text
x = X / Z
y = Y / Z
```

Cette représentation permet d’éviter les inversions modulaires intermédiaires. Une seule inversion est nécessaire à la fin pour revenir en coordonnées affines.

### `jacobian.py`

Ce fichier implémente la multiplication scalaire en coordonnées de Jacobi.

Un point est représenté sous la forme :

```text
P = (X, Y, Z)
```

avec la correspondance affine :

```text
x = X / Z²
y = Y / Z³
```

Les coordonnées de Jacobi sont particulièrement adaptées aux courbes de Weierstrass comme secp256k1, surtout lorsque `a = 0`.

Elles permettent de réduire fortement le nombre d’inversions modulaires, ce qui améliore les performances.

### `montgomery.py`

Ce fichier implémente une Montgomery ladder sur la courbe secp256k1.

La Montgomery ladder est une méthode de multiplication scalaire plus régulière que le double-and-add classique.

À chaque bit du scalaire, l’algorithme effectue toujours :

* une addition de points ;
* un doublement de point.

Cela donne une structure plus régulière, intéressante dans un contexte de sécurité embarquée.

Cependant, dans ce projet, la Montgomery ladder est implémentée en coordonnées affines complètes `(x, y)`.

Il ne s’agit donc pas d’une version `x-only` optimisée comme celle utilisée avec Curve25519, car secp256k1 est une courbe de Weierstrass et non une courbe de Montgomery.

Cette méthode est donc utile pour comparer la régularité de l’algorithme, mais elle reste coûteuse en inversions modulaires.

### `benchmark.py`

Ce fichier lance les tests de performance.

Il compare les méthodes suivantes :

* affine ;
* projective ;
* Jacobi ;
* Montgomery ladder.

Pour chaque méthode, il mesure :

* le temps moyen d’exécution ;
* le nombre moyen de multiplications ;
* le nombre moyen d’inversions ;
* la cohérence des résultats obtenus.

Les tests sont réalisés avec des scalaires aléatoires de 256 bits.

### `main.py`

Ce fichier fournit une interface en ligne de commande.

Il permet :

* de tester une multiplication scalaire sur secp256k1 ;
* de lancer le benchmark complet ;
* de tester une courbe personnalisée.

### `gui.py`

Ce fichier fournit une interface graphique simple avec Tkinter.

Elle permet de choisir :

* la courbe secp256k1 ou une courbe personnalisée ;
* le scalaire `k` ;
* la méthode de multiplication scalaire ;
* puis d’afficher le point résultat, le nombre d’opérations et le temps d’exécution.

## Méthodes implémentées

## 1. Coordonnées affines

Les coordonnées affines représentent un point par :

```text
P = (x, y)
```

Avantages :

* représentation simple ;
* formules faciles à comprendre ;
* peu de multiplications par opération.

Inconvénients :

* nécessite beaucoup d’inversions modulaires ;
* les inversions sont coûteuses ;
* peu adaptée aux environnements embarqués.

## 2. Coordonnées projectives standard

Les coordonnées projectives représentent un point par :

```text
P = (X, Y, Z)
```

Avantages :

* réduit fortement le nombre d’inversions ;
* plus rapide que l’affine dans la plupart des cas ;
* une seule inversion est nécessaire à la fin.

Inconvénients :

* utilise plus de multiplications ;
* formules plus complexes ;
* moins efficace que Jacobi sur secp256k1 dans nos tests.

## 3. Coordonnées de Jacobi

Les coordonnées de Jacobi représentent un point par :

```text
P = (X, Y, Z)
```

avec :

```text
x = X / Z²
y = Y / Z³
```

Avantages :

* très efficaces pour secp256k1 ;
* évitent presque toutes les inversions intermédiaires ;
* bon compromis entre vitesse et coût des opérations.

Inconvénients :

* formules plus complexes que l’affine ;
* plus de multiplications que l’affine.

## 4. Montgomery ladder

La Montgomery ladder est une méthode de multiplication scalaire régulière.

Elle utilise deux registres de points :

```text
R0 = O
R1 = P
```

Pour chaque bit du scalaire :

```text
si bit = 0 :
    R1 = R0 + R1
    R0 = 2R0

si bit = 1 :
    R0 = R0 + R1
    R1 = 2R1
```

Avantages :

* structure régulière ;
* une addition et un doublement à chaque bit ;
* intéressante pour limiter certaines fuites par canaux auxiliaires.

Inconvénients :

* dans ce projet, elle est implémentée en coordonnées affines ;
* elle conserve donc beaucoup d’inversions modulaires ;
* elle n’est pas aussi rapide que Jacobi ;
* ce n’est pas une version `x-only` optimisée.

## Protocole expérimental

Les tests sont effectués sur la courbe secp256k1.

Le benchmark utilise :

* 50 scalaires aléatoires ;
* des scalaires de 256 bits ;
* le même point générateur `G` pour toutes les méthodes ;
* la même liste de scalaires pour toutes les méthodes.

Pour chaque méthode, le programme calcule :

```text
Q = kG
```

Puis il mesure :

* le temps moyen d’exécution ;
* le nombre moyen de multiplications ;
* le nombre moyen d’inversions.

Le programme vérifie également que toutes les méthodes donnent les mêmes résultats que la méthode affine.

## Exécution

### Lancer le menu principal

```bash
python main.py
```

### Lancer directement le benchmark

```bash
python benchmark.py
```

### Lancer l’interface graphique

```bash
python gui.py
```

## Exemple de résultats

Les résultats peuvent varier selon la machine utilisée.

Exemple de sortie possible :

```text
=== BENCHMARK ECC ===
Courbe testée : secp256k1
Nombre de scalaires testés : 50
Taille des scalaires : 256 bits

Méthode : AFFINE
Temps moyen           : 0.013000 s
Multiplications moy.  : 2168.74
Inversions moy.       : 383.02

Méthode : JACOBI
Temps moyen           : 0.004038 s
Multiplications moy.  : 5240.74
Inversions moy.       : 1.00

Méthode : PROJECTIF
Temps moyen           : 0.005031 s
Multiplications moy.  : 6641.44
Inversions moy.       : 1.00

Méthode : MONTGOMERY LADDER
Temps moyen           : variable selon la machine
Multiplications moy.  : variable selon les scalaires
Inversions moy.       : élevée
```

## Analyse des résultats

Les résultats montrent que les coordonnées affines utilisent relativement peu de multiplications, mais beaucoup d’inversions modulaires.

Or, l’inversion modulaire est beaucoup plus coûteuse qu’une multiplication modulaire.

C’est pourquoi la méthode affine est généralement moins performante malgré un nombre plus faible de multiplications.

Les coordonnées projectives et les coordonnées de Jacobi remplacent les inversions intermédiaires par des multiplications supplémentaires.

Cette stratégie est plus efficace, car les multiplications sont moins coûteuses que les inversions.

Les coordonnées de Jacobi donnent généralement les meilleurs résultats sur secp256k1, car elles sont bien adaptées aux courbes de Weierstrass avec `a = 0`.

La Montgomery ladder, dans notre implémentation, est plus régulière que le double-and-add classique. Elle effectue une addition et un doublement à chaque bit du scalaire.

Cependant, comme elle est implémentée en coordonnées affines, elle effectue encore beaucoup d’inversions modulaires. Elle n’est donc pas la plus rapide dans cette version.

## Conclusion

Ce projet montre que le choix de la représentation des points a un impact important sur les performances de la multiplication scalaire.

Les coordonnées affines sont simples mais coûteuses à cause des nombreuses inversions modulaires.

Les coordonnées projectives améliorent les performances en évitant les inversions intermédiaires.

Les coordonnées de Jacobi offrent le meilleur compromis dans les tests réalisés sur secp256k1.

La Montgomery ladder est intéressante pour sa régularité, ce qui est important dans un contexte embarqué ou face aux attaques par canaux auxiliaires. Cependant, dans ce projet, elle est implémentée en coordonnées affines, ce qui limite ses performances.

Pour les smart cards, le meilleur choix pratique est donc :

```text
coordonnées de Jacobi
```

car elles réduisent fortement les inversions et donnent les meilleures performances dans nos tests.

Toutefois, pour une application cryptographique réelle sur smart card, une solution encore plus robuste serait d’utiliser une multiplication scalaire régulière, de type Montgomery ladder, combinée avec des coordonnées projectives ou jacobiennes afin d’obtenir à la fois :

* de bonnes performances ;
* une meilleure régularité d’exécution ;
* une meilleure résistance aux attaques par canaux auxiliaires.

## Difficultés rencontrées

Les principales difficultés du projet ont été :

* comprendre les différentes représentations de points ;
* éviter les erreurs dans les formules d’addition et de doublement ;
* gérer correctement le point à l’infini ;
* compter séparément les multiplications et les inversions ;
* comparer équitablement les méthodes avec les mêmes scalaires ;
* intégrer la Montgomery ladder sur une courbe de Weierstrass comme secp256k1.

## Limites du projet

La Montgomery ladder implémentée n’est pas une version `x-only`.

Une vraie Montgomery ladder `x-only` est naturellement adaptée aux courbes de Montgomery comme Curve25519.

Comme secp256k1 est une courbe de Weierstrass, nous avons utilisé une ladder régulière sur points affines complets.

De plus, le benchmark est réalisé en Python. Les résultats donnent donc une comparaison expérimentale utile, mais une implémentation en C serait plus représentative pour une smart card.

## Améliorations possibles

Les améliorations possibles sont :

* implémenter une Montgomery ladder en coordonnées projectives ou jacobiennes ;
* ajouter une vraie courbe de Montgomery comme Curve25519 ;
* comparer avec une implémentation en C ;
* mesurer la consommation mémoire ;
* étudier les attaques par canaux auxiliaires ;
* ajouter des graphiques de comparaison ;
* augmenter le nombre de scalaires testés ;
* exporter les résultats du benchmark dans un fichier CSV.

## Auteurs

ONGONO MVEME BERTRAND 09U0529
TADJUIDJE KAMDEM ANDRE JORDAN 21T2472

## Licence

Projet académique – usage éducatif.
