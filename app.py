
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは日本人に英語を教える優秀な英語教師です。英単語が入力された場合はその意味と語源を日本語で解説して、その単語の英語の例文を例示してください。文章が入力された場合はそれを翻訳してください。文章の翻訳の際には翻訳後の文章のみで、解説や例文は必要ありません。「英会話練習」と入力された場合は、「終了」と入力されるまで英会話のロールプレイングを行ってください。ロールプレイングの際には英文の後に日本語の翻訳文を（）で語尾に付けてください。"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("新世代のアイドル型ChatAI, ChatGPS爆誕")
st.write("私は英語教師です。単語や文章を入力するとそれを日英翻訳します。また、会話の練習がしたい場合は「英会話練習」と言ってください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])