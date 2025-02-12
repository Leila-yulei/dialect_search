from extension import db

# 定义数据库模型
class Meaning(db.Model):
    __tablename__ = 'meanings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meaning = db.Column(db.String(100), nullable=False)

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(50), nullable=False)
    volume = db.Column(db.String(50), nullable=True)  # 卷数
    entry = db.Column(db.String(50), nullable=True)   # 条目

class WordMeaning(db.Model):
    __tablename__ = 'word_meaning'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    meaning_id = db.Column(db.Integer, db.ForeignKey('meanings.id'), nullable=False)

class Dialect(db.Model):
    __tablename__ = 'dialects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dialect_word = db.Column(db.String(50), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    region = db.Column(db.String(100), nullable=True)  # 地区可以为空
    initial = db.Column(db.String(10), nullable=True)  # 声母可以为空
    rhyme = db.Column(db.String(10), nullable=True)  # 韵部可以为空
    comment = db.Column(db.String(200), nullable=True)  # 备注可以为空
    original_text = db.Column(db.String(200), nullable=True)  # 原文可以为空