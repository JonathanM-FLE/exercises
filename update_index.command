#!/bin/bash

# Script de mise à jour automatique de l'index FLE
# Usage: Double-clic sur ce fichier

# Se placer dans le dossier du script
cd "$(dirname "$0")"

echo "🚀 Mise à jour automatique de l'index FLE..."
echo "📁 Dossier de travail: $(pwd)"
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé ou accessible"
    echo "💡 Installez Python depuis python.org ou utilisez Homebrew:"
    echo "   brew install python"
    echo ""
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

# Vérifier que le script Python existe
if [ ! -f "update_index.py" ]; then
    echo "❌ Le fichier update_index.py n'existe pas dans ce dossier"
    echo "💡 Assurez-vous que update_index.py est dans le même dossier"
    echo ""
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

# Vérifier que le dossier exercises existe
if [ ! -d "exercises" ]; then
    echo "❌ Le dossier 'exercises' n'existe pas"
    echo "💡 Créez le dossier exercises/ et ajoutez-y vos exercices HTML"
    echo ""
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

# Vérifier que index.html existe
if [ ! -f "index.html" ]; then
    echo "❌ Le fichier index.html n'existe pas"
    echo "💡 Assurez-vous que index.html est dans le même dossier"
    echo ""
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

# Lancer le script Python
echo "⚡ Lancement du générateur d'index..."
python3 update_index.py

# Vérifier le résultat
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Mise à jour terminée avec succès !"
    echo "🎯 Vous pouvez maintenant faire un commit et push sur GitHub"
    echo ""
    echo "Commandes suggérées :"
    echo "  git add ."
    echo "  git commit -m 'Mise à jour automatique de l'index'"
    echo "  git push"
else
    echo ""
    echo "❌ Erreur lors de la mise à jour"
    echo "🔍 Vérifiez les messages d'erreur ci-dessus"
fi

echo ""
read -p "Appuyez sur Entrée pour fermer..."