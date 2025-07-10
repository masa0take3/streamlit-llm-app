import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Streamlit Secrets から API キーを取得
openai_api_key = st.secrets["openai"]["api_key"]

# LLMと専門家のプロンプトを定義する関数
def get_expert_answer(user_input, expert_type):
    # LLMの初期化
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key, max_tokens=500)

    # 専門家に応じたプロンプトのシステムメッセージ
    if expert_type == 'A：歴史学':
        expert_message = "あなたは歴史学の専門家です。次の質問に答えてください:"
    elif expert_type == 'B：料理':
        expert_message = "あなたは料理の専門家です。次の質問に答えてください:"
    else:
        expert_message = "あなたは一般的なアシスタントです。次の質問に答えてください:"

    # プロンプトテンプレートを定義
    prompt = PromptTemplate(input_variables=["user_input"], template=f"{expert_message} {{user_input}}")

    # プロンプトを使ってLLMチェーンを作成
    chain = LLMChain(llm=llm, prompt=prompt)

    # LLMを使って回答を取得
    result = chain.run(user_input)
    
    return result

# Streamlitアプリケーションの構成
def main():
    # アプリケーションタイトル
    st.title("専門家への質問")

    # アプリケーションの説明
    st.write("このWebアプリケーションでは、専門家に質問をすることができます。以下の入力フォームに質問を入力し、専門家を選んで送信してください。")

    # ユーザーからの入力を取得
    user_input = st.text_input("質問内容を入力してください:")

    # 専門家の選択肢を提供
    expert_type = st.radio(
        "専門家を選んでください",
        ('A：歴史学', 'B：料理'),
        index=0
    )

    # 質問が送信されたときの処理
    if st.button('質問を送信'):
        if user_input:
            # 入力された内容と選択された専門家に基づいてLLMから回答を取得
            answer = get_expert_answer(user_input, expert_type)
            st.write("### 回答:")
            st.write(answer)
        else:
            st.error("質問を入力してください。")

if __name__ == "__main__":
    main()
