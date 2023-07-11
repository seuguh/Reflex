# Reflex
jeu de réflexe. 

--- Le 11/07/23 le code est à priori fonctionnel.

Composé d'un boitier imprimé en 3d, d'un rp204, de deux boutons d'arcade et de 9 leds ws2812.

Comment ça se joue:

-led centrale clignotante rouge/jaune: attente debut manche
  attend un appui simultané des boutons jusqu'à ce que la led centrale devienne jaune.
  
-led centrale bleu: manche en cours
  les joueurs doivent attendre que la led passe vert pour appuyer sur le bouton.
  Chaque appui sur le bouton pendant cette phase retire un point.
  
-led centrale verte: GO GO GO!
  Le plus rapide à appuyer sur son bouton marque le point.
  
- les autres leds servent à afficher le score: de 1 à 4.
  
- Dès qu'un joueur atteint le score de 5, la partie est gagnée, ses leds clignotent.
