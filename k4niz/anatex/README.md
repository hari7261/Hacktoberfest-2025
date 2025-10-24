**Contributor:** k4niz


# AR Anatomy Explorer

An educational AR + AI web application for exploring 3D human organs in Augmented Reality. Tap/click an organ to get AI-generated anatomical explanations.

## Tech Stack
- Frontend: React + Vite + Tailwind + AR.js + Three.js
- Backend: FastAPI (Python)
- AI: OpenAI GPT API
- 3D Models: GLTF/GLB assets

## Structure
```
ar-anatex-explorer/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ARScene.jsx
│   │   │   ├── OrganCard.jsx
│   │   │   ├── AIDescriptionBox.jsx
│   │   │   └── QuizMode.jsx
│   │   └── utils/
│   │       └── api.js
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   └── organs.py
│   │   ├── controllers/
│   │   │   └── organ_controller.py
│   │   ├── services/
│   │   │   ├── gpt_service.py
│   │   │   └── organ_service.py
│   │   └── models/
│   │       └── organ_model.py
│   └── requirements.txt
└── README.md
```