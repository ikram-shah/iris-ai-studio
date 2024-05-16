# IRIS AI Studio

[![Gitter](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://openexchange.intersystems.com/package/IRIS-AI-Studio-2)

A no-code/low-code tool to explore the capabilities of vector embeddings in InterSystems IRIS DB. 

- **Connectors** let load data from files as vector embeddings into IRIS DB

- **Playground** let users explore different retrieval channels on the vector embeddings reside in IRIS DB

![Process Flow](assets/pipeline.png)

### Try Online
https://iris-ai-studio.vercel.app/

Designed and developed only for web interface, not compatible with mobile

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

Simply execute the script using the following command.

```
./build.sh
```

If any permission issue while executing the script, allow it through `chmod +x build.sh`

Access the **UI** at http://localhost:5173

Access the **APIs** at http://127.0.0.1:8000

**Credentials for Local InterSystems IRIS Instance**
username: demo
password: demo
hostname: localhost
port: 1972
namespace: USER

#### IRIS Instance

[Follow the instructions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=ACLOUD) to spin off a Cloud InterSystems Community Edition

Once you have the credentials, in the frontend application's settings page the credentials can be added. You may add more than one instance and choose to use whichever one for data ingestion or retrieval process independently. 

You may follow the following instructions to individually run the frontend and backend

#### Frontend (VueJS)

Start from application's root directory

```
cd frontend
npm i
npm run dev
```

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


