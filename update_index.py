#!/usr/bin/env python3
"""
Script pour générer automatiquement la liste des exercices dans index.html
Usage: python update_index.py
"""

import os
import re
import json
from pathlib import Path

def extract_metadata_from_html(file_path):
    """Extraire les métadonnées d'un fichier HTML d'exercice"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire le titre de la page
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Exercice"
        title = title.replace(' - A1', '').replace(' - A2', '').replace(' - B1', '').replace(' - B2', '').replace(' - C1', '').replace(' - C2', '')
        
        # Extraire le niveau CECR du badge
        cecr_match = re.search(r'<div class="cecr-badge[^>]*>([ABC][12])</div>', content)
        level = cecr_match.group(1) if cecr_match else "A1"
        
        # Extraire le type d'exercice du config JavaScript
        type_match = re.search(r'type:\s*["\']([^"\']+)["\']', content)
        exercise_type = type_match.group(1) if type_match else "qcm"
        
        # Extraire la description du h1 ou subtitle
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
        subtitle_match = re.search(r'<p class="subtitle[^>]*>(.*?)</p>', content)
        
        if subtitle_match:
            description = subtitle_match.group(1)
        elif h1_match:
            description = f"Exercice de {h1_match.group(1).lower()}"
        else:
            description = "Exercice de français langue étrangère"
        
        # Nettoyer les balises HTML de la description
        description = re.sub(r'<[^>]+>', '', description).strip()
        
        return {
            'filename': file_path.name,
            'title': title.strip(),
            'level': level,
            'type': exercise_type,
            'description': description,
            'url': f'./exercises/{file_path.name}'
        }
    except Exception as e:
        print(f"Erreur lors de l'extraction de {file_path}: {e}")
        return None

def generate_exercise_list():
    """Scanner le dossier exercises/ et générer la liste"""
    exercises_dir = Path('exercises')
    if not exercises_dir.exists():
        print("❌ Dossier 'exercises/' non trouvé!")
        return []
    
    exercises = []
    html_files = list(exercises_dir.glob('*.html'))
    
    print(f"🔍 Scan de {len(html_files)} fichiers HTML...")
    
    for html_file in html_files:
        print(f"   📄 {html_file.name}")
        metadata = extract_metadata_from_html(html_file)
        if metadata:
            exercises.append(metadata)
    
    # Trier par niveau puis par titre
    level_order = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}
    exercises.sort(key=lambda x: (level_order.get(x['level'], 0), x['title']))
    
    return exercises

def update_index_html(exercises):
    """Mettre à jour index.html avec la nouvelle liste"""
    index_path = Path('index.html')
    
    if not index_path.exists():
        print("❌ Fichier index.html non trouvé!")
        return False
    
    # Lire index.html actuel
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Générer le code JavaScript pour les exercices
    js_exercises = []
    for ex in exercises:
        js_exercises.append(f"""                    {{
                        filename: '{ex['filename']}',
                        title: '{ex['title']}',
                        level: '{ex['level']}',
                        type: '{ex['type']}',
                        description: '{ex['description']}',
                        url: '{ex['url']}'
                    }}""")
    
    exercises_js = ',\n'.join(js_exercises)
    
    # Remplacer la section exercises dans le JavaScript
    # Pattern pour capturer la première occurrence dans le constructor
    pattern = r'(constructor\(\) \{[^}]*this\.exercises = \[)[^\]]*(\];)'
    replacement_made = False
    
    if re.search(pattern, content, flags=re.DOTALL):
        replacement = f'\\1\n{exercises_js}\n                \\2'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        replacement_made = True
    else:
        # Fallback: chercher juste this.exercises = [...]; et prendre la première occurrence
        simple_pattern = r'(this\.exercises = \[)[^\]]*(\];)'
        matches = list(re.finditer(simple_pattern, content, flags=re.DOTALL))
        if matches:
            # Prendre la première occurrence
            match = matches[0]
            start_pos = match.start(1) + len(match.group(1))
            end_pos = match.start(2)
            new_content = (content[:start_pos] + 
                          f'\n{exercises_js}\n                ' + 
                          content[end_pos:])
            replacement_made = True
    
    # Vérifier que le remplacement a eu lieu
    if not replacement_made:
        print("⚠️  Impossible de trouver la section à remplacer dans index.html")
        print("🔍 Sections recherchées :")
        print("   - constructor() { ... this.exercises = [...]")
        print("   - this.exercises = [...]")
        print("\n💡 Vérifiez que index.html contient une de ces structures")
        return False
    
    # Écrire le nouveau fichier
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("🚀 Génération automatique de l'index FLE...")
    
    # Scanner les exercices
    exercises = generate_exercise_list()
    
    if not exercises:
        print("❌ Aucun exercice trouvé!")
        return
    
    print(f"\n📚 {len(exercises)} exercices détectés:")
    for ex in exercises:
        print(f"   • {ex['level']} - {ex['title']} ({ex['type']})")
    
    # Mettre à jour index.html
    if update_index_html(exercises):
        print(f"\n✅ index.html mis à jour avec {len(exercises)} exercices!")
        print("🎯 Vous pouvez maintenant commit et push!")
    else:
        print("\n❌ Erreur lors de la mise à jour de index.html")

if __name__ == "__main__":
    main()