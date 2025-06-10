# Slack Integration with ML model POC

This project summarizes Slack threads using an LLM (such as Mistral) via Ollama, stores the summaries in a CSV file, and utilizes those summaries to answer questions using another LLM (such as LLaMA3). The entire setup runs locally using the Flask framework.

Components
1. Slack Setup
   • Create a Slack App: Go to https://api.slack.com/apps > Create New App
   • Enable OAuth & Permissions:
        Scopes:
          - channels: history
          - channels: read
          - groups: history
          - groups: read
   • Install in the  workspace
   • Get Bot Token: Found in the OAuth & Permissions page after installation
   
2. Ollama Installation
   • https://ollama.com/download
   • In the command line, run
        ollama run llama3
        ollama run mistral
   • Verify its working by hitting api http://localhost:11434/api/tags

3. Paste the bot token in utils.js
4.  Run the application **python main.py**    
5.  Hit Flask App APIs in postman
     /get_thread_messages
     /summarize_thread
     /ask_question





