  1. CONNEXION                                                         
  Chef de projet → SSO Microsoft (compte @[enervivo.fr](http://enervivo.fr)) → /projects      


  2. DÉCLENCHEMENT                                                     
  Clic sur "Lancer l’audit complet" sur un projet                      
  → l’audit se lance en arrière-plan, l’UI reste disponible            


  3. COLLECTE SHAREPOINT                                               
  - Listing des fichiers du dossier /09-Projets/<CODE>                 
  - Filtrage : on ignore les vidéos, archives, fichiers 3D, GIS, code… 
  - Téléchargement en mémoire (jamais stocké sur disque)               

  4. ANALYSE IA (par fichier, 5 en parallèle)                          
  - Extraction du texte (PDF, Word, Excel, PowerPoint…)                
  - Pour les images / scans : analyse visuelle directe                 
  - Envoi à Claude (modèle Anthropic) avec le catalogue des 107 docs   
  - Retour : { type, confiance 0-100, justification }                  
  - Cache intelligent : un doc déjà vu = gratuit                       


  5. CONFRONTATION AU RÉFÉRENTIEL V12                                  
  - 107 documents attendus répartis sur 9 jalons                       
  - Chaque attendu reçoit un statut :                                  
     ✅ Présent   ⚠️ Ambigu   ❌ Manquant   ⬜ Non applicable          
  - Calcul du score de complétude par jalon                            

  6. RAPPORT INTERACTIF                                                
  - Vue par jalon avec filtre                                          
  - Mise en avant des documents critiques manquants (bandeau rouge)    
  - Pour chaque ligne : justification IA + lien direct SharePoint      
  - Progression en temps réel pendant l’audit (pas besoin d’attendre)  
