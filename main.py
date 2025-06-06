from flask import Flask, request, jsonify
from utils import save_or_update_summary_to_csv
from utils import get_thread_text
from utils import summarize_text
from utils import read_summaries_from_csv
from utils import ask_question

app = Flask(__name__)

@app.route('/get_thread_messages', methods=['POST'])
def get_thread_messages():
    data = request.json
    channel_id = data.get("channel_id")
    thread_ts = data.get("thread_ts")

    if not channel_id or not thread_ts:
        return jsonify({"error": "Missing channel_id or thread_ts"}), 400

    text = get_thread_text(channel_id, thread_ts)
    return jsonify({"messages": text})


@app.route('/summarize_thread', methods=['POST'])
def summarize_thread():
    data = request.json
    channel_id = data.get("channel_id")
    thread_ts = data.get("thread_ts")

    if not channel_id or not thread_ts:
        return jsonify({"error": "Missing channel_id or thread_ts"}), 400

    thread_text = get_thread_text(channel_id, thread_ts)
    if thread_text.startswith("[Slack Error]"):
        return jsonify({"error": thread_text}), 500

    summary = summarize_text(thread_text)
    save_or_update_summary_to_csv(channel_id, thread_ts, summary)
    return jsonify({"summary": summary})


@app.route('/ask_question', methods=['POST'])
def ask_question_api():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing question"}), 400

    # Read all summaries from CSV
    summaries = read_summaries_from_csv()

    if not summaries:
        return jsonify({"error": "No summaries found."}), 404

    # Combine summaries into one context string
    context = "\n\n".join(summaries)

    # Ask the question using Ollama
    answer = ask_question(question, context)

    return jsonify({"answer": answer})



if __name__ == "__main__":
    app.run(port=5000, debug=True)
