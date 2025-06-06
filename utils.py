import csv
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

OLLAMA_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

client = WebClient(token="SLACK_BOT_TOKEN")

def save_or_update_summary_to_csv(channel_id, thread_ts, summary, filename='summaries.csv'):
    rows = []
    found = False

    # Read existing data
    if os.path.isfile(filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['channel_id'] == channel_id and row['thread_ts'] == thread_ts:
                    # Update the summary for this row
                    row['summary'] = summary
                    found = True
                rows.append(row)

    # If not found, append new entry
    if not found:
        rows.append({
            'channel_id': channel_id,
            'thread_ts': thread_ts,
            'summary': summary
        })

    # Write all rows back to CSV (overwrite)
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['channel_id', 'thread_ts', 'summary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_thread_text(channel_id, thread_ts):
    try:
        replies = client.conversations_replies(channel=channel_id, ts=thread_ts)
        thread_text = "\n".join(msg["text"] for msg in replies["messages"])
        return thread_text
    except SlackApiError as e:
        return f"[Slack Error] {e.response['error']}"


def summarize_text(text):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"Summarize the following Slack thread:\n\n{text}",
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json()["response"]
    except Exception as e:
        return f"[Summarization Error] {e}"

def read_summaries_from_csv(filename='summaries.csv'):
    summaries = []
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                summaries.append(row['summary'])
    except FileNotFoundError:
        pass
    return summaries

def ask_question(question, context_text):
    prompt = f"Based on the following information, answer the question:\n\nContext:\n{context_text}\n\nQuestion: {question}\nAnswer:"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json().get("response", "No answer from model.")
    except Exception as e:
        return f"[QA Error] {e}"