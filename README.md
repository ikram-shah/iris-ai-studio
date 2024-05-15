# IRIS AI Studio

[![Gitter](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://openexchange.intersystems.com/package/iris-ai-studio)

A no-code/low-code tool to explore the capabilities of vector embeddings in InterSystems IRIS DB. 

- **Connectors** let load data from files as vector embeddings into IRIS DB

- **Playground** let users explore different retrival channels on the vector embeddings reside in IRIS DB

![Process Flow](assets/pipeline.png)

### Try Online
https://iris-ai-studio.vercel.app/

**Step 1**: Setup the Instance details and API Keys in settings

**Step 2**: Through connectors load data into IRIS DB

**Step 3**: In playground, explore different retrieval options

###### ⚠️ This application is deployed on render.com and the IRIS instance & API key info used on the live version may have been logged. Strongly recommended to use only development or temporary IRIS instances to explore the solution, and deactivate or delete the keys after use. Also, backend runs on a tiny server and won't be able to handle heavy workloads.

### Tech Stack

- Frontend: VueJS, TailwindCSS, Flowbite
  
- Backend: Python, Flask
  
- Database: InterSystems IRIS

- Frameworks/Libraries/Services: Llama-Index, SQLalchemy-iris, OpenAI, Cohere
  
- Infrastructure: Vercel (frontend hosting), Render (backend hosting)

### Instructions to Run

#### IRIS Instance

[Follow the instructions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=ACLOUD) to spin off an InterSystems Community Edition of your choice - Local, Cloud, Web 

Once you have the credentials, in the frontend application's settings page the credentials can be added. You may add more than one instance and choose to use whichever one for data ingestion or retrival process independently. 

#### Frontend (VueJS)

Start from application's root directory

```
cd frontend
npm i
npm run dev
```

Access the UI at http://localhost:5173

#### Backend (Python)

Start from application's root directory

```
cd backend
pip install -r requirements.txt
gunicorn app:app
```

Access the APIs at http://127.0.0.1:8000

#### Folder Structure

```
iris-ai-studio/
├──frontend                
│   ├── src/
│   ├── .env                 
│   └── ...
├── backend/
│   └── app.py
│   ├── data_loader.py
│   ├── chat_llama.py
│   ├── query_llama.py
│   ├── similarity_llama.py
│   ├── reco_llama.py
│   ├── requirements.txt
│   │   └── ...
├── assets/
├── README.md
└── LICENSE
```

## License

This project is licensed under the [MIT License](LICENSE).

You can find the full text of the license in the [LICENSE](LICENSE) file.


