# LangChain Documentation Assistant

Une application Streamlit qui utilise LangChain pour interagir avec la documentation de LangChain de manière conversationnelle.

## Configuration requise

- Python 3.12+
- Pipenv
- Compte Pinecone
- Ollama

## Installation

1. Cloner le repository
```bash
git clone <votre-repo-url>
cd langchain_documentation_app
```

2. Installer les dépendances
```bash
pipenv install
```

3. Configurer les variables d'environnement
- Copier `.env.example` vers `.env`
- Remplir les variables dans `.env` avec vos propres valeurs

4. Lancer l'application
```bash
pipenv run streamlit run main.py
```

## Structure du projet

```
├── backend/           # Backend de l'application
│   └── core.py       # Logique principale LangChain
├── main.py           # Interface Streamlit
├── ingestion.py      # Script d'ingestion des documents
└── Pipfile           # Dépendances du projet
```

## Fonctionnalités

- Chat interactif avec la documentation LangChain
- Recherche sémantique avec Pinecone
- Interface utilisateur conviviale avec Streamlit
- Historique des conversations
- Affichage des sources pour chaque réponse