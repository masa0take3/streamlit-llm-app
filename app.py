import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

#from dotenv import load_dotenv
#load_dotenv()

# Streamlit Secrets から API キーを取得
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]

def get_expert_response(user_input, expert_type):
    """LLMからの回答を返す関数"""
    
    # 専門家タイプに応じてシステムメッセージを設定
    if expert_type == 'プログラミング専門家':
        system_message = "あなたはプログラミングの専門家です。技術的な質問に詳しく答えてください。"
    else:  # 料理専門家
        system_message = "あなたは料理の専門家です。料理に関する質問に詳しく答えてください。"
    
    try:
        # ChatOpenAIインスタンスの作成
        chat = ChatOpenAI(
            model="gpt-4o-mini",  # モデル名を指定
            temperature=0.7,
            max_tokens=500,
        )
        
        # メッセージの作成
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_input)
        ]
        
        # LLMに送信して回答を取得
        response = chat(messages)
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlitアプリ
st.title("専門家チャットアプリ")

st.markdown("""
## 使い方
1. 専門家を選択
2. 質問を入力
3. 「回答を取得」ボタンをクリック
""")

# 専門家選択
expert_type = st.radio(
    "専門家を選択してください:",
    ["プログラミング専門家", "料理専門家"]
)

# 質問入力
user_input = st.text_area(
    "質問を入力してください:",
    height=100,
    placeholder="例: Pythonのリスト操作について教えて"
)

# 回答取得ボタン
if st.button("回答を取得"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            response = get_expert_response(user_input, expert_type)
            st.subheader(f"{expert_type}の回答:")
            st.write(response)
    else:
        st.warning("質問を入力してください。")
