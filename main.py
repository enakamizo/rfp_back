from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 質問データ（1つの日付に5つの質問を紐付け）
questions_by_date = {
    "2024-11-24": [
        {
            "id": 1,
            "question_text": "Tech Quiz - 質問1",
            "options": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
            "correct_index": 0,
            "explanation": "Tech Quiz - 質問1の解説。",
        },
        {
            "id": 2,
            "question_text": "Tech Quiz - 質問2",
            "options": ["選択肢E", "選択肢F", "選択肢G", "選択肢H"],
            "correct_index": 1,
            "explanation": "Tech Quiz - 質問2の解説。",
        },
        {
            "id": 3,
            "question_text": "Tech Quiz - 質問3",
            "options": ["選択肢I", "選択肢J", "選択肢K", "選択肢L"],
            "correct_index": 2,
            "explanation": "Tech Quiz - 質問3の解説。",
        },
        {
            "id": 4,
            "question_text": "Tech Quiz - 質問4",
            "options": ["選択肢M", "選択肢N", "選択肢O", "選択肢P"],
            "correct_index": 3,
            "explanation": "Tech Quiz - 質問4の解説。",
        },
        {
            "id": 5,
            "question_text": "Tech Quiz - 質問5",
            "options": ["選択肢Q", "選択肢R", "選択肢S", "選択肢T"],
            "correct_index": 0,
            "explanation": "Tech Quiz - 質問5の解説。",
        },
    ],
    "2024-09-24 Biz": [
        {
            "id": 6,
            "question_text": "Biz - 問1:バリュープロポジションキャンバスを使う意義は何ですか？",
            "options": ["顧客の解像度を上げて、本質的な価値を提供する。", "製品のコスト削減のみを目的とする。", "顧客との直接的な会話を避けるためのツールである。", "競合の成功事例を模倣するためのフレームワークである。"],
            "correct_index": 0,
            "explanation": "バリュープロポジションキャンバスは顧客の解像度を高め、そのニーズに基づいた価値提供を行うためのツールです​。",
        },
        {
            "id": 7,
            "question_text": "Biz - 問2:Juiceroの失敗の主な原因は何ですか？​",
            "options": ["技術的な欠陥があったため。", "顧客が必要としない価値に投資したため。", "他社の競争力に負けたため。G", "資金調達が不十分だったため。"],
            "correct_index": 1,
            "explanation": "Juiceroは顧客のニーズを正確に理解せず、誰も必要としない価値を提供したため失敗しました。",
        },
        {
            "id": 8,
            "question_text": "Biz - 問3:トヨタとフェラーリの顧客層における大きな違いは何ですか？",
            "options": ["トヨタは高級車、フェラーリは低価格車を提供する。", "トヨタは優越感、フェラーリは安心感を提供する。", "トヨタは誰もが手に入れられる移動手段、フェラーリはステータスを提供する。", "トヨタは環境重視、フェラーリは技術重視。"],
            "correct_index": 2,
            "explanation": "トヨタは「誰もが手に入れられる安心安全な移動手段」を提供し、フェラーリは「優越感溢れるステータス」を提供する顧客価値の違いがあります​。",
        },
        {
            "id": 9,
            "question_text": "Biz - 問4:顧客セグメント作成フローの最初のステップは何ですか？",
            "options": ["顧客の課題（ペイン）を洗い出す。", "提供する価値を特定する。", "顧客セグメントを特定する。", "製品の価格を設定する。"],
            "correct_index": 2,
            "explanation": "顧客セグメント作成フローでは、最初に「誰に」価値を提供するかを特定することから始めます。",
        },
        {
            "id": 10,
            "question_text": "Biz - 問5:バリューマップとは何をするためのツールですか？",
            "options": ["顧客に提供する価値を設計するためのツール。", "製品の生産コストを削減するためのツール。", "競合企業の模倣を促進するためのツール。", "顧客との直接的なコミュニケーションを避けるためのツール。"],
            "correct_index": 0,
            "explanation": "バリューマップは、顧客の利得を生み出し、悩みを取り除く製品やサービスを設計するためのツールです。",
        },
    ],
    "2024-02-13 Design": [
        {
            "id": 11,
            "question_text": "Design - 問1:UXデザインにおける「エクスペリエンスデザイン」とは、主に何を目指しているのでしょうか？",
            "options": ["高機能で便利なサービスを提供すること", "顧客が言葉にできなかったニーズを満たすこと", "顧客の声をそのまま反映すること", "企業の利益を最大化すること"],
            "correct_index": 1,
            "explanation": "エクスペリエンスデザインとは、顧客が心の底では欲していたが言葉にできなかったニーズや無意識に諦めていた経験を実現することを目指すプロセスです。便利さだけではなく、深い価値を提供することが重要です。",
        },
        {
            "id": 12,
            "question_text": "Design - 問2:以下の中で、「UXデザイン」におけるペルソナの目的として最も適切なものはどれでしょうか？",
            "options": ["顧客の属性だけでターゲットを分類する", "仮想の顧客像を具体化して理解を深める", "顧客行動を全てデータ化する", "既存顧客の不満を解消する"],
            "correct_index": 1,
            "explanation": "ペルソナは商品やサービスのターゲットとなる架空の顧客像を設定し、具体的な理解を深めるために活用されます。単に属性で分類するのではなく、趣味やライフスタイルなどの詳細情報を加えて作成します。",
        },
        {
            "id": 13,
            "question_text": "Design - 問3:次の「デザインの4原則」に含まれないものはどれでしょうか？",
            "options": ["近接", "整列", "均等", "強弱"],
            "correct_index": 3,
            "explanation": "デザインの4原則は、「近接」「整列」「反復」「強弱」の4つで構成されます。「均等」という項目は含まれません。",
        },
        {
            "id": 14,
            "question_text": "Design - 問4:「配色」において、RGBの組み合わせは主に何を表現するために使用されますか？",
            "options": ["選択肢ディスプレイ上の色", "印刷物の色", "白黒の濃淡", "補色の関係"],
            "correct_index": 0,
            "explanation": "RGB（赤・緑・青）の組み合わせはディスプレイ上で色を表現するために使用されます。一方、印刷物ではCMYKが使用されます。",
        },
        {
            "id": 15,
            "question_text": "Design - 問5:「彩度」が高い色はどのような印象を与えますか？",
            "options": ["落ち着いた印象", "柔らかい印象", "鮮やかで目を引く印象", "ぼんやりとした印象"],
            "correct_index": 2,
            "explanation": "彩度が高い色は鮮やかで目を引く効果があります。一方、彩度が低い色は落ち着いた印象を与えます。",
        },
    ],
}

# 新しいルートエンドポイントを追加
@app.get("/")
def read_root():
    return {"message": "Welcome to the Quiz API!"}

# 全ての日付を取得
@app.get("/get_all_dates")
def get_all_dates():
    return {"dates": list(questions_by_date.keys())}

# 特定の日付に紐付く質問を取得
@app.get("/get_questions_by_date/{selected_date}")
def get_questions_by_date(selected_date: str):
    selected_date = unquote(selected_date)
    if selected_date in questions_by_date:
        return questions_by_date[selected_date]
    return {"error": "No questions found for this date."}

# 特定の質問を取得
@app.get("/get_question/{question_id}")
def get_question(question_id: int):
    for date, questions in questions_by_date.items():
        for question in questions:
            if question["id"] == question_id:
                return question
    return {"error": "Question not found"}
