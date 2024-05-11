### IRIS AI Studio

A simple tool that can be used as no-code/low-code to explore the capabilities of vector embeddings in IRIS DB. 

![Process Flow](assets/pipeline.png)

### Instructions to Run

### IRIS Instance

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
