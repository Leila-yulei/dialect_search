from flask import Flask, request, jsonify, render_template
from extension import db
from models import Meaning, Word, Dialect, WordMeaning
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dialects.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.cli.command()
# 初始化数据库
def create():
    db.drop_all()
    db.create_all()

@app.cli.command()
def seed():
    """插入示例数据"""
    print("插入示例数据...")

    # 插入单词
    word_hui = Word(word='慧')
    db.session.add(word_hui)
    db.session.commit()

    # 插入含义
    meaning_clever = Meaning(meaning='聪明')
    meaning_cunning = Meaning(meaning='狡黠')
    db.session.add(meaning_clever)
    db.session.add(meaning_cunning)
    db.session.commit()

    # 插入单词和含义的关联
    word_meaning1 = WordMeaning(word_id=word_hui.id, meaning_id=meaning_clever.id)
    word_meaning2 = WordMeaning(word_id=word_hui.id, meaning_id=meaning_cunning.id)
    db.session.add(word_meaning1)
    db.session.add(word_meaning2)
    db.session.commit()

    # 插入方言用词
    dialect_qian = Dialect(dialect_word='虔', word_id=word_hui.id, region='楚', initial='端母', rhyme='阳部')
    dialect_xuan = Dialect(dialect_word='儇', word_id=word_hui.id, region='楚', initial='晓母', rhyme='宵部')
    db.session.add(dialect_qian)
    db.session.add(dialect_xuan)
    db.session.commit()

    print("示例数据插入完成！")


# 批量导入数据
@app.cli.command()
def word():
    # 加载 Excel 文件
    df = pd.read_excel('word.xlsx', sheet_name='Sheet1')

    # 遍历每一行数据并插入到数据库
    for index, row in df.iterrows():
        word_entry = Word(word=row['word'], volume=row['volume'], entry=row['entry'])  # 假设 Excel 文件中列名为 'word'
        db.session.add(word_entry)

    # 提交事务
    db.session.commit()
    print("数据导入完成！")

@app.cli.command()
def meaning():
    # 加载 Excel 文件
    df = pd.read_excel('meaning.xlsx', sheet_name='Sheet1')

    # 遍历每一行数据并插入到数据库
    for index, row in df.iterrows():
        meaning_entry = Meaning(meaning=row['meaning'])  # 假设 Excel 文件中列名为 'meaning'
        db.session.add(meaning_entry)

    # 提交事务
    db.session.commit()
    print("数据导入完成！")

@app.cli.command()
def wordmeaning():
    # 加载 Excel 文件
    df = pd.read_excel('meaning.xlsx', sheet_name='Sheet1')

    # 遍历每一行数据并插入到数据库
    for index, row in df.iterrows():
        # 创建 WordMeaning 对象，包含 word_id 和 meaning_id
        wordmeaning_entry = WordMeaning(word_id=row['word_id'], meaning_id=row['meaning_id'])
        db.session.add(wordmeaning_entry)

    # 提交事务
    db.session.commit()
    print("数据导入完成！")

@app.cli.command()
def dialect():
    # 加载 Excel 文件
    df = pd.read_excel('dialect.xlsx', sheet_name='Sheet1')

    # 遍历每一行数据并插入到数据库
    for index, row in df.iterrows():
        # 创建 WordMeaning 对象
        dialect = Dialect(dialect_word=row['dialect_word'], word_id=row['word_id'], region=row['region'], comment=row['comment'], original_text=row['original_text'], initial=row['initial'], rhyme=row['rhyme'])
        db.session.add(dialect)

    # 提交事务
    db.session.commit()
    print("数据导入完成！")

@app.route('/search_by_meaning', methods=['GET'])
def search_by_meaning():
    meaning_query = request.args.get('meaning', '')
    if not meaning_query:
        return jsonify({"error": "No meaning provided"}), 400

    meanings = Meaning.query.filter(Meaning.meaning.like(f'%{meaning_query}%')).all()
    if not meanings:
        return jsonify({"message": "No results found"}), 404

    results = []
    for meaning in meanings:
        word_meanings = WordMeaning.query.filter_by(meaning_id=meaning.id).all()
        for wm in word_meanings:
            word = Word.query.get(wm.word_id)
            dialects = Dialect.query.filter_by(word_id=word.id).all()
            results.append({
                "word": word.word,
                "volume": word.volume,  # 加入卷数
                "entry": word.entry,    # 加入条目
                "meaning": meaning.meaning,
                "dialects": [
                    {
                        "dialect_word": d.dialect_word,
                        "region": d.region,
                        "initial": d.initial,
                        "rhyme": d.rhyme,
                        "comment": d.comment,
                        "original_text": d.original_text
                    } for d in dialects
                ]
            })

    return jsonify(results)

@app.route('/search_by_word', methods=['GET'])
def search_by_word():
    word_query = request.args.get('word', '')
    if not word_query:
        return jsonify({"error": "No word provided"}), 400

    words = Word.query.filter(Word.word.like(f'%{word_query}%')).all()
    if not words:
        return jsonify({"message": "No results found"}), 404

    results = []
    for word in words:
        word_meanings = WordMeaning.query.filter_by(word_id=word.id).all()
        meanings = [Meaning.query.get(wm.meaning_id).meaning for wm in word_meanings]
        dialects = Dialect.query.filter_by(word_id=word.id).all()

        results.append({
            "word": word.word,
            "volume": word.volume,  # 加入卷数
            "entry": word.entry,  # 加入条目
            "meanings": meanings,
            "dialects": [
                {
                    "dialect_word": d.dialect_word,
                    "region": d.region,
                    "initial": d.initial,
                    "rhyme": d.rhyme,
                    "comment": d.comment,
                    "original_text": d.original_text
                } for d in dialects
            ]
        })

    return jsonify(results)
if __name__ == '__main__':
    app.run(debug=True)
