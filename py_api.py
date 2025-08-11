from flask import Flask, request, jsonify
from together import Together
import time

app = Flask(__name__)


def safe_chat_completion(client, model, messages, max_tokens, temperature=0, stream=False, retries=10, wait_time=300):
    for _ in range(retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )
        except Exception as e:
            if "max_new_tokens" in str(e):
                print(f"\n max_new_tokens error detected. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                raise
    raise RuntimeError("Exceeded retry attempts due to persistent max_new_tokens error.")

def fix_specific_bug_from_string(client, code_language: str, code_snippet: str, bug_description: str):
    Model = "Qwen/Qwen2.5-Coder-32B-Instruct"

    system_prompt_g = (
        f"You are a {code_language} code repair assistant specialized in fixing only one specific bug:\n"
        f"\"{bug_description}\"\n"
        "You will receive a single Python code snippet containing this type of bug.\n"
        "Your task is to fix only this specific bug — do not correct any other bugs, stylistic or functional.\n"
        "Any changes you make must be applied across the entire snippet if needed, as fixing one part in isolation may affect other parts of the code.\n"
        "The corrected code must preserve all original logic and behavior.\n"
        "Your output must consist only of the corrected Python code, with no explanations, comments, or formatting."
        "If and only any variable names are changed mention it as a comment."
    )

    system_prompt_d = (
        f"You are a {code_language} code inspection assistant that checks for exactly one specific bug:\n"
        f"\"{bug_description}\"\n"
        "You will be given a single Python code snippet as input.\n"
        "Your task is to analyze the code and determine whether this bug is present in the code.\n"
        "If the bug is present anywhere in the snippet, respond with: Y\n"
        "If the bug is not present at all, respond with: N\n"
        "Do not explain your answer or output anything else."
    )

    system_prompt_e = (
        f"You are a {code_language} bug explanation assistant specialized in explaining only one specific bug: "
        f"\"{bug_description}\"\n"
        "You will be given a single Python code snippet as input.\n"
        "Your task is to analyze the code and clearly explain what the bug is, if it exists.\n"
        "Describe what causes the issue—such as a syntax error, logic flaw, or incorrect use of a function or library.\n"
        "Do not assume anything not evident from the code.\n"
        "Be concise, accurate, and do not explain or mention any other bugs, stylistic issues, or unrelated problems."
    )

    user_code = code_snippet
    max_attempts = 3
    attempt = 0
    discriminator_output = "Y"

    while attempt < max_attempts and discriminator_output[0] != "N":
        print(f"\n--- Attempt {attempt + 1} ---")

        print("Generating code using generator model...")
        response_g = safe_chat_completion(
            client,
            model=Model,
            messages=[
                {"role": "system", "content": system_prompt_g},
                {"role": "user", "content": user_code}
            ],
            max_tokens=1024,
            temperature=0,
            stream=False
        )
        generated_code = response_g.choices[0].message.content

        print("Evaluating code using discriminator model...")
        response_d = safe_chat_completion(
            client,
            model=Model,
            messages=[
                {"role": "system", "content": system_prompt_d},
                {"role": "user", "content": generated_code}
            ],
            max_tokens=1,
            temperature=0,
            stream=False
        )
        discriminator_output = response_d.choices[0].message.content.strip()
        if discriminator_output[0] == "Y":
            print("Bug Fix Failed.....Retrying....")
        else:
            print("Bug Fix Successful")

        user_code = generated_code
        attempt += 1

    if discriminator_output[0] == 'N':
        return {"status": "success", "fixed_code": user_code}
    else:
        print("Bug persists after 3 attempts. Explaining the bug...")
        time.sleep(60)
        response_e = safe_chat_completion(
            client,
            model=Model,
            messages=[
                {"role": "system", "content": system_prompt_e},
                {"role": "user", "content": user_code}
            ],
            max_tokens=256,
            temperature=0,
            stream=False
        )

        explanation = response_e.choices[0].message.content
        return {"status": "failed", "explanation": explanation}

@app.route('/fix', methods=['POST'])
def fix_code():
    data = request.get_json()
    code = data.get("code_snippet")
    language = data.get("code_language")
    bug = data.get("bug_description")

    if not all([code, language, bug]):
        return jsonify({"error": "Missing required parameters"}), 400

    client = Together(api_key="enter your together token")

    result = fix_specific_bug_from_string(client, language, code, bug)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
