<p align="center">
  <img src="https://camo.githubusercontent.com/2e67eb232c50c65aeae8ecfb6ad0861551ec881104a3e4eafa7021a6c7373aaa/68747470733a2f2f73332e61702d736f7574682d312e616d617a6f6e6177732e636f6d2f6432632d63646e2d6d756d6261692f75706c6f6164732f757365722d70726f6a6563742d66696c65732f363838346638313863363631665f617377696e5f6f746865722e706e67" alt="Banner"/>
</p>

# AI-Powered PDF Context Retrieval Chatbot (RAG) 🤖📄

**Repository:** [Ashprogrammer29/AI-Powered-PDF-Context-Retrieval-Chatbot-RAG](https://github.com/Ashprogrammer29/AI-Powered-PDF-Context-Retrieval-Chatbot-RAG)

Unlock intelligent context retrieval and querying from your PDFs using state-of-the-art AI! This Retrieval-Augmented Generation (RAG) chatbot leverages FastAPI, LangChain, Google Gemini, and powerful vector search for document Q&A.

---

## 🗂️ Files & Structure

| File/Folder                           | Description                                                                            |
|---------------------------------------|----------------------------------------------------------------------------------------|
| `PDF Context Retrieval Chatbot.ipynb` | Main Jupyter notebook: code, API, model setup, PDF ingestion, and querying logic       |
| `requirements[1].txt`                 | Python dependencies (FastAPI, LangChain, vector DB, Google GenAI, etc.)                |
| `LICENSE`                             | Boost Software License v1.0 (see below)                                                |

**Key Notebook Functions**:
- PDF upload & text extraction (`get_pdf_text`)
- Text chunking & vector store creation (`create_vectorstore`)
- API endpoints (`/process`)
- Utility scripts: file/folder handling, model config, embedding setup
- Uses FastAPI for serving endpoints

---

## ⚡️ Quick Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Ashprogrammer29/AI-Powered-PDF-Context-Retrieval-Chatbot-RAG.git
   cd AI-Powered-PDF-Context-Retrieval-Chatbot-RAG
   ```

2. **Install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements[1].txt
   ```

3. **Configure Model**
   - Setup your Google Gemini API key (via notebook or environment)
   - Place model configs/weights as needed

---

## 🚦 Running the Chatbot

### 📝 Jupyter Notebook
- Open `PDF Context Retrieval Chatbot.ipynb`
- Step through: mount storage, set up API keys, upload PDFs, run cells for context retrieval & Q&A

### 🌐 API Server (FastAPI)
- Inside the notebook, the FastAPI app is initialized; you can run locally using:
   ```bash
   uvicorn main:app --reload
   ```
- Endpoints available for PDF upload & query

---

## 📡 API Endpoints

### 1. **Upload PDF**
   - **Endpoint:** `/process`
   - **Method:** `POST`
   - **Payload:** JSON (see notebook's `File` model)
   ```json
   {
     "files": ["https://example.com/file1.pdf", ...],
     "rewrite": true
   }
   ```

### 2. **Query Context**
   - Use the vectorstore and Q&A logic in the notebook to ask questions about uploaded PDFs.

---

## 🧠 Model & Config Notes

- **LLM:** Google Gemini (via `langchain-google-genai`, API key required)
- **Embeddings:** GoogleGenerativeAIEmbeddings + FAISS for semantic search
- **PDF Parsing:** PyMuPDF (`pymupdf`)
- **Text Splitting:** RecursiveCharacterTextSplitter from LangChain
- **API Models:** Pydantic-based request bodies
- **Configurable:** Chunk size, rewrite mode, user/session IDs, etc.

---

## 📒 Example Usage

1. **Upload PDFs** via `/process` endpoint or notebook cell
2. **Ask questions!**: "What is the summary of the document?" or "Find the legal clause about termination."
3. **Get answers** with full context, citations, and semantic retrieval from your documents.

---

## 🎯 Use Cases

- **Legal Document Q&A** ⚖️  
  Instantly find clauses, obligations, or summaries from contracts and agreements.
- **Academic Research Assistant** 🎓  
  Extract findings, definitions, and references from research papers.
- **Business Report Analysis** 📊  
  Query for revenue, trends, and executive summaries in reports.
- **Technical Manual & FAQ Chatbot** 🛠️  
  Retrieve procedures and troubleshooting from manuals.
- **Compliance & Policy Checking** 🏢  
  Automate policy and HR queries from company documents.
- **Customer Support Automation** 💬  
  Answer product, feature, or troubleshooting questions from help docs.
- **Onboarding & Training** 👩‍💼  
  Enable instant answers for new employee training materials.

---

## 🙌 Contributing

Pull requests, issues, and suggestions are welcome! 🎉

---

## 📜 License

This project is licensed under the **Boost Software License - Version 1.0 - August 17th, 2003**.

See the [LICENSE](LICENSE) file for details.

---

## 💡 Tech Stack

- FastAPI 🚀
- LangChain 🦜
- Google Gemini 🤖
- FAISS/Vector DB 🔍
- PyMuPDF 📄
- Pydantic 🛠️

---

## 🌟 Acknowledgements

Big thanks to the open-source AI/NLP community, LangChain, Google, and all contributors!

---

<p align="center">
  <b>Made with ❤️ by <a href="https://github.com/Ashprogrammer29">Ashprogrammer29</a></b>
</p>
