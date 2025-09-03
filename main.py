import os
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Application Flask pour Vercel
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "algoria-vercel-secret-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration base de données
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tmp/algoria.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Créer les dossiers nécessaires
os.makedirs('/tmp/uploads', exist_ok=True)
os.makedirs('/tmp', exist_ok=True)

db.init_app(app)

# Configuration complète des 15 agents IA
AGENTS_CONFIG = {
    'llm_central': {
        'name': 'LLM Central',
        'description': 'Orchestrateur principal et coordinateur intelligent de tous les agents',
        'icon': '🎯',
        'speciality': 'Coordination et routage intelligent des demandes',
        'provider': 'OpenAI'
    },
    'agent_mail': {
        'name': 'Agent Mail',
        'description': 'Spécialiste en analyse d\'emails et réponses automatisées',
        'icon': '📧',
        'speciality': 'Gestion des emails et communication',
        'provider': 'Anthropic'
    },
    'agent_explorateur': {
        'name': 'Agent Explorateur',
        'description': 'Expert en recherche de données externes et web scraping',
        'icon': '🔍',
        'speciality': 'Recherche web et collecte de données',
        'provider': 'Perplexity'
    },
    'agent_project_manager': {
        'name': 'Agent Project Manager',
        'description': 'Gestionnaire de projets et création de roadmaps',
        'icon': '📋',
        'speciality': 'Gestion de projets et planification',
        'provider': 'OpenAI'
    },
    'agent_task_manager': {
        'name': 'Agent Task Manager',
        'description': 'Décomposition et gestion avancée des tâches',
        'icon': '✅',
        'speciality': 'Organisation et suivi des tâches',
        'provider': 'OpenAI'
    },
    'agent_analyste': {
        'name': 'Agent Analyste',
        'description': 'Spécialiste en analyse de données et génération d\'insights',
        'icon': '📊',
        'speciality': 'Analyse de données et visualisations',
        'provider': 'Gemini'
    },
    'agent_ecosysteme': {
        'name': 'Agent Écosystème',
        'description': 'Expert en intégrations externes et gestion d\'APIs',
        'icon': '🌐',
        'speciality': 'Intégrations et écosystème technique',
        'provider': 'xAI'
    },
    'agent_archiver': {
        'name': 'Agent Archiver',
        'description': 'Gestionnaire de documentation et base de connaissances',
        'icon': '📚',
        'speciality': 'Documentation et archivage',
        'provider': 'Anthropic'
    },
    'agent_strategique': {
        'name': 'Agent Stratégique',
        'description': 'Analyse stratégique business et étude de marché',
        'icon': '🎯',
        'speciality': 'Stratégie business et analyse marché',
        'provider': 'OpenAI'
    },
    'agent_dev': {
        'name': 'Agent Dev',
        'description': 'Développeur expert en code et prototypage technique',
        'icon': '💻',
        'speciality': 'Développement et prototypage rapide',
        'provider': 'xAI'
    },
    'agent_client': {
        'name': 'Agent Client',
        'description': 'Tests d\'expérience utilisateur et simulation client',
        'icon': '👤',
        'speciality': 'UX/UI et expérience utilisateur',
        'provider': 'Anthropic'
    },
    'agent_securite': {
        'name': 'Agent Sécurité',
        'description': 'Audit de sécurité et vérification de conformité',
        'icon': '🔒',
        'speciality': 'Sécurité et conformité',
        'provider': 'Gemini'
    },
    'agent_prospecteur': {
        'name': 'Agent Prospecteur',
        'description': 'Identification d\'opportunités et génération de leads',
        'icon': '🎪',
        'speciality': 'Prospection et opportunités business',
        'provider': 'Perplexity'
    },
    'agent_equipes': {
        'name': 'Agent Équipes',
        'description': 'Gestion d\'équipes et ressources humaines',
        'icon': '👥',
        'speciality': 'Management et ressources humaines',
        'provider': 'Anthropic'
    },
    'agent_marketing': {
        'name': 'Agent Marketing',
        'description': 'Campagnes marketing digital et communication',
        'icon': '📢',
        'speciality': 'Marketing digital et communication',
        'provider': 'OpenAI'
    }
}

def simulate_ai_response(message, agent_type):
    """Simuler les réponses des agents IA avec personnalité unique"""
    agent_info = AGENTS_CONFIG.get(agent_type, AGENTS_CONFIG['llm_central'])
    
    responses = {
        'llm_central': f"🎯 LLM Central - Coordination : '{message[:40]}...' → Je route votre demande vers l'agent optimal et coordonne la réponse multi-agent.",
        'agent_mail': f"📧 Agent Mail - Communication : Analyse de '{message[:30]}...' → Je peux traiter vos emails, créer des templates et automatiser vos réponses.",
        'agent_explorateur': f"🔍 Agent Explorateur - Recherche : '{message[:30]}...' → Je vais explorer le web pour vous trouver les données les plus récentes et pertinentes.",
        'agent_project_manager': f"📋 Project Manager - Planification : '{message[:30]}...' → Je structure votre projet avec timeline, milestones et allocation des ressources.",
        'agent_task_manager': f"✅ Task Manager - Organisation : '{message[:30]}...' → Je décompose votre demande en tâches priorisées avec deadlines optimisées.",
        'agent_analyste': f"📊 Agent Analyste - Données : '{message[:30]}...' → J'analyse vos données avec visualisations avancées et insights business.",
        'agent_ecosysteme': f"🌐 Agent Écosystème - APIs : '{message[:30]}...' → Je gère vos intégrations externes et optimise votre architecture technique.",
        'agent_archiver': f"📚 Agent Archiver - Documentation : '{message[:30]}...' → Je centralise vos connaissances et crée une base documentaire structurée.",
        'agent_strategique': f"🎯 Agent Stratégique - Business : '{message[:30]}...' → Analyse stratégique complète avec étude concurrentielle et recommandations.",
        'agent_dev': f"💻 Agent Dev - Code : '{message[:30]}...' → Développement rapide avec architecture scalable et bonnes pratiques techniques.",
        'agent_client': f"👤 Agent Client - UX : '{message[:30]}...' → Test utilisateur complet avec recommandations d'amélioration de l'expérience.",
        'agent_securite': f"🔒 Agent Sécurité - Audit : '{message[:30]}...' → Audit sécuritaire complet avec conformité RGPD et recommandations de protection.",
        'agent_prospecteur': f"🎪 Agent Prospecteur - Leads : '{message[:30]}...' → Identification d'opportunités business avec stratégies de prospection ciblées.",
        'agent_equipes': f"👥 Agent Équipes - RH : '{message[:30]}...' → Gestion d'équipe optimisée avec évaluation des performances et développement des talents.",
        'agent_marketing': f"📢 Agent Marketing - Communication : '{message[:30]}...' → Campagne marketing multi-canal avec ROI optimisé et engagement maximal."
    }
    
    return responses.get(agent_type, f"🤖 {agent_info['icon']} {agent_info['name']} - {agent_info['provider']} : Traitement expert de '{message[:40]}...' en cours avec notre IA spécialisée.")

# Templates HTML intégrés
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Algoria LLM Center - Centre d'Intelligence Artificielle</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.29.0/feather.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .hero { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(15px); 
            border-radius: 20px; 
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .agent-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            height: 100%;
        }
        .agent-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.25);
            box-shadow: 0 12px 25px rgba(0,0,0,0.15);
        }
        .btn-glow {
            box-shadow: 0 0 20px rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }
        .btn-glow:hover {
            box-shadow: 0 0 30px rgba(255,255,255,0.5);
            transform: scale(1.05);
        }
        .stats-card {
            background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2));
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center align-items-center min-vh-100">
            <div class="col-lg-10">
                <div class="hero p-5 text-center text-white">
                    <div class="row mb-4">
                        <div class="col-12">
                            <h1 class="display-2 mb-3">🤖 Algoria LLM Center</h1>
                            <p class="lead mb-4 fs-4">Centre d'Intelligence Artificielle Multi-Agents</p>
                            <p class="mb-4">Plateforme unifiée avec 15 agents IA spécialisés pour tous vos besoins business</p>
                        </div>
                    </div>
                    
                    <!-- Statistiques -->
                    <div class="row mb-5">
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-3">
                                <h2 class="display-6 mb-0">15</h2>
                                <small>Agents IA</small>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-3">
                                <h2 class="display-6 mb-0">5</h2>
                                <small>Providers LLM</small>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-3">
                                <h2 class="display-6 mb-0">24/7</h2>
                                <small>Disponible</small>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-3">
                                <h2 class="display-6 mb-0">∞</h2>
                                <small>Possibilités</small>
                            </div>
                        </div>
                    </div>

                    <!-- Agents principaux -->
                    <div class="row mb-5">
                        {% for agent_id, agent in agents.items() %}
                        {% if loop.index <= 6 %}
                        <div class="col-lg-4 col-md-6 mb-4">
                            <div class="agent-card card h-100 text-white border-0">
                                <div class="card-body d-flex flex-column">
                                    <div class="mb-3">
                                        <h1 class="display-4 mb-0">{{ agent.icon }}</h1>
                                    </div>
                                    <h5 class="card-title mb-2">{{ agent.name }}</h5>
                                    <p class="card-text small mb-2">{{ agent.description }}</p>
                                    <div class="mt-auto">
                                        <span class="badge bg-light text-dark">{{ agent.provider }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endif %}
                        {% endfor %}
                    </div>

                    <!-- Actions principales -->
                    <div class="row mb-4">
                        <div class="col-12">
                            <a href="/dashboard" class="btn btn-light btn-lg me-3 mb-3 btn-glow">
                                🎯 Dashboard Complet
                            </a>
                            <a href="/chat" class="btn btn-outline-light btn-lg me-3 mb-3 btn-glow">
                                💬 Chat Multi-Agents
                            </a>
                            <a href="/api/test" class="btn btn-outline-light btn-lg mb-3 btn-glow">
                                🔧 Test API
                            </a>
                        </div>
                    </div>

                    <!-- Status Vercel -->
                    <div class="row">
                        <div class="col-12">
                            <div class="alert alert-success bg-transparent border-light">
                                <h4>✅ Déployé avec succès sur Vercel !</h4>
                                <p class="mb-0">🌐 Application en ligne • ⚡ Performance optimisée • 🔒 HTTPS sécurisé</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.29.0/feather.min.js"></script>
    <script>feather.replace()</script>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Algoria LLM Center</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #1a1a2e; color: #eee; }
        .sidebar { background: #16213e; min-height: 100vh; }
        .agent-card { background: #0f3460; border: 1px solid #533483; transition: all 0.3s; }
        .agent-card:hover { background: #533483; transform: scale(1.02); }
        .main-content { background: #0f3460; min-height: 100vh; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-2 sidebar p-3">
                <h4>🤖 Algoria</h4>
                <hr>
                <div class="nav flex-column">
                    <a href="/" class="nav-link text-light">🏠 Accueil</a>
                    <a href="/dashboard" class="nav-link text-warning">🎯 Dashboard</a>
                    <a href="/chat" class="nav-link text-light">💬 Chat</a>
                    <a href="/api/test" class="nav-link text-light">🔧 API</a>
                </div>
            </div>
            
            <!-- Main content -->
            <div class="col-md-10 main-content p-4">
                <h2 class="mb-4">🎯 Dashboard Multi-Agents</h2>
                
                <div class="row">
                    {% for agent_id, agent in agents.items() %}
                    <div class="col-lg-3 col-md-4 col-sm-6 mb-3">
                        <div class="agent-card card h-100">
                            <div class="card-body text-center">
                                <h2 class="mb-3">{{ agent.icon }}</h2>
                                <h6 class="card-title">{{ agent.name }}</h6>
                                <p class="card-text small">{{ agent.speciality }}</p>
                                <span class="badge bg-primary">{{ agent.provider }}</span>
                                <div class="mt-3">
                                    <button class="btn btn-sm btn-outline-light" onclick="selectAgent('{{ agent_id }}', '{{ agent.name }}')">
                                        Sélectionner
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <!-- Zone de chat intégrée -->
                <div class="row mt-4">
                    <div class="col-12">
                        <div class="card bg-dark">
                            <div class="card-header">
                                <h5 id="current-agent">💬 Chat avec LLM Central</h5>
                            </div>
                            <div class="card-body">
                                <div id="chat-messages" style="height: 300px; overflow-y: auto; background: #1a1a2e; padding: 15px; border-radius: 8px;">
                                    <div class="alert alert-info">
                                        🎯 <strong>LLM Central :</strong> Bienvenue ! Sélectionnez un agent spécialisé ou discutez avec moi pour être orienté.
                                    </div>
                                </div>
                                <div class="input-group mt-3">
                                    <input type="hidden" id="selected-agent" value="llm_central">
                                    <input type="text" class="form-control bg-dark text-light border-secondary" id="message-input" placeholder="Tapez votre message...">
                                    <button class="btn btn-primary" onclick="sendMessage()">Envoyer</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function selectAgent(agentId, agentName) {
        document.getElementById('selected-agent').value = agentId;
        document.getElementById('current-agent').innerHTML = `💬 Chat avec ${agentName}`;
        
        const messages = document.getElementById('chat-messages');
        messages.innerHTML += `<div class="alert alert-warning"><strong>Système :</strong> Agent ${agentName} sélectionné !</div>`;
        messages.scrollTop = messages.scrollHeight;
    }
    
    function sendMessage() {
        const input = document.getElementById('message-input');
        const agent = document.getElementById('selected-agent').value;
        const messages = document.getElementById('chat-messages');
        
        if (input.value.trim()) {
            messages.innerHTML += `<div class="alert alert-primary mb-2"><strong>Vous :</strong> ${input.value}</div>`;
            
            // Simulation réponse agent
            const agentResponses = {
                'llm_central': `🎯 <strong>LLM Central :</strong> "${input.value}" → Je coordonne votre demande avec les agents spécialisés !`,
                'agent_dev': `💻 <strong>Agent Dev :</strong> Pour "${input.value}", je génère du code optimisé et des architectures scalables !`,
                'agent_analyste': `📊 <strong>Agent Analyste :</strong> Analyse de "${input.value}" avec visualisations et insights business !`,
                'agent_marketing': `📢 <strong>Agent Marketing :</strong> "${input.value}" → Campagne multi-canal avec ROI optimisé !`
            };
            
            setTimeout(() => {
                const response = agentResponses[agent] || `🤖 <strong>Agent :</strong> Traitement expert de "${input.value}" en cours !`;
                messages.innerHTML += `<div class="alert alert-success mb-2">${response}</div>`;
                messages.scrollTop = messages.scrollHeight;
            }, 1000);
            
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }
    }
    
    document.getElementById('message-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    </script>
</body>
</html>
"""

# Routes principales
@app.route('/')
def index():
    """Page d'accueil avec tous les agents"""
    return render_template_string(HOME_TEMPLATE, agents=AGENTS_CONFIG)

@app.route('/dashboard')
def dashboard():
    """Dashboard complet avec tous les agents"""
    return render_template_string(DASHBOARD_TEMPLATE, agents=AGENTS_CONFIG)

@app.route('/chat')
def chat():
    """Interface de chat simplifiée"""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat - Algoria LLM Center</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #1a1a2e; color: #eee; }
            .chat-container { background: #0f3460; border-radius: 15px; }
            .message-user { background: #533483; }
            .message-agent { background: #16213e; }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <div class="chat-container p-4">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h3>🤖 Chat Algoria Multi-Agents</h3>
                            <a href="/" class="btn btn-outline-light btn-sm">🏠 Accueil</a>
                        </div>
                        
                        <div id="chat-messages" class="mb-4" style="height: 500px; overflow-y: auto; background: #1a1a2e; padding: 20px; border-radius: 10px;">
                            <div class="message-agent p-3 mb-3 rounded">
                                🎯 <strong>LLM Central :</strong> Bonjour ! Je suis le coordinateur d'Algoria. Quel agent souhaitez-vous consulter ?
                            </div>
                        </div>
                        
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <select class="form-select bg-dark text-light border-secondary" id="agent-select">
                                    {% for agent_id, agent in agents.items() %}
                                    <option value="{{ agent_id }}">{{ agent.icon }} {{ agent.name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="col-md-6">
                                <div class="input-group">
                                    <input type="text" class="form-control bg-dark text-light border-secondary" id="message-input" placeholder="Votre message...">
                                    <button class="btn btn-primary" onclick="sendMessage()">Envoyer</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        function sendMessage() {
            const input = document.getElementById('message-input');
            const agent = document.getElementById('agent-select').value;
            const messages = document.getElementById('chat-messages');
            
            if (input.value.trim()) {
                messages.innerHTML += `<div class="message-user p-3 mb-3 rounded">👤 <strong>Vous :</strong> ${input.value}</div>`;
                
                // Réponses simulées des agents
                const responses = {
                    'llm_central': `🎯 <strong>LLM Central :</strong> "${input.value}" → Coordination avec les agents spécialisés en cours !`,
                    'agent_dev': `💻 <strong>Agent Dev :</strong> Code généré pour "${input.value}" avec architecture optimisée !`,
                    'agent_analyste': `📊 <strong>Agent Analyste :</strong> Analyse complète de "${input.value}" avec insights business !`,
                    'agent_marketing': `📢 <strong>Agent Marketing :</strong> Campagne "${input.value}" avec stratégie multi-canal !`
                };
                
                setTimeout(() => {
                    const response = responses[agent] || `🤖 <strong>Agent :</strong> Traitement expert de "${input.value}" !`;
                    messages.innerHTML += `<div class="message-agent p-3 mb-3 rounded">${response}</div>`;
                    messages.scrollTop = messages.scrollHeight;
                }, 1200);
                
                input.value = '';
                messages.scrollTop = messages.scrollHeight;
            }
        }
        
        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        </script>
    </body>
    </html>
    """, agents=AGENTS_CONFIG)

@app.route('/api/test')
def api_test():
    """Test de l'API avec informations complètes"""
    return {
        "status": "success",
        "message": "🤖 Algoria LLM Center fonctionne parfaitement sur Vercel !",
        "platform": "Vercel",
        "version": "1.0.0",
        "agents_total": len(AGENTS_CONFIG),
        "agents_available": list(AGENTS_CONFIG.keys()),
        "providers": ["OpenAI", "Anthropic", "Gemini", "Perplexity", "xAI"],
        "features": [
            "15 agents IA spécialisés",
            "Chat multi-agents en temps réel",
            "Dashboard interactif complet",
            "API REST complète",
            "Interface responsive",
            "Déploiement Vercel optimisé"
        ],
        "timestamp": str(datetime.datetime.now())
    }

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API de chat avec tous les agents"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent_type = data.get('agent', 'llm_central')
        
        if agent_type not in AGENTS_CONFIG:
            agent_type = 'llm_central'
        
        response = simulate_ai_response(message, agent_type)
        agent_info = AGENTS_CONFIG[agent_type]
        
        return {
            "status": "success",
            "agent": {
                "id": agent_type,
                "name": agent_info['name'],
                "icon": agent_info['icon'],
                "provider": agent_info['provider']
            },
            "message": message,
            "response": response,
            "timestamp": str(datetime.datetime.now())
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/api/agents')
def api_agents():
    """API pour lister tous les agents disponibles"""
    return {
        "status": "success",
        "total_agents": len(AGENTS_CONFIG),
        "agents": AGENTS_CONFIG
    }

# Point d'entrée pour Vercel
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)

# Export pour Vercel
app