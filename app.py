import os
import sqlite3
import csv
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')
DB_PATH = Path('data.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def grade_essay(text, prompt=''):
    score = 0
    max_score = 1000
    feedback = []
    
    words = text.split()
    word_count = len(words)
    
    if word_count < 7:
        return 0, ['Redação muito curta. O ENEM exige no mínimo 7 linhas (aproximadamente 150 palavras).']
    
    if word_count >= 250:
        score += 200
        feedback.append('✅ Extensão adequada (250+ palavras)')
    elif word_count >= 150:
        score += 150
        feedback.append('⚠️ Extensão mínima atingida, mas recomenda-se 250+ palavras')
    else:
        feedback.append('❌ Redação muito curta. Mínimo: 150 palavras, recomendado: 250+')
    
    intro_keywords = ['atualmente', 'hoje em dia', 'no brasil', 'na sociedade', 'é possível observar', 'contextualização']
    has_intro = any(keyword in text.lower() for keyword in intro_keywords)
    if has_intro or word_count >= 100:
        score += 200
        feedback.append('✅ Introdução com contextualização presente')
    else:
        feedback.append('❌ Introdução deve contextualizar o tema')
    
    tese_keywords = ['portanto', 'dessa forma', 'assim', 'logo', 'por isso', 'é fundamental', 'é necessário', 'deve-se']
    has_tese = any(keyword in text.lower() for keyword in tese_keywords)
    
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    has_structure = len(paragraphs) >= 3
    
    if has_tese and has_structure:
        score += 200
        feedback.append('✅ Argumentação e tese identificadas')
    elif has_tese:
        score += 150
        feedback.append('⚠️ Tese presente, mas estrutura pode melhorar')
    else:
        feedback.append('❌ Falta clareza na tese/argumentação')
    
    conectivos = ['além disso', 'ademais', 'outrossim', 'por outro lado', 'entretanto', 'contudo', 'todavia', 'portanto', 'assim', 'dessa forma']
    conectivo_count = sum(1 for c in conectivos if c in text.lower())
    
    if conectivo_count >= 3:
        score += 200
        feedback.append('✅ Boa coesão textual com conectivos adequados')
    elif conectivo_count >= 1:
        score += 150
        feedback.append('⚠️ Coesão presente, mas pode usar mais conectivos')
    else:
        feedback.append('❌ Falta uso de conectivos para coesão textual')
    
    intervencao_keywords = ['proposta', 'governo', 'estado', 'sociedade', 'mídia', 'educação', 'conscientização', 'política pública', 'medida', 'ação']
    intervencao_count = sum(1 for k in intervencao_keywords if k in text.lower())
    
    agente_keywords = ['governo', 'estado', 'ministério', 'ongs', 'sociedade civil', 'escolas', 'família', 'mídia']
    has_agente = any(keyword in text.lower() for keyword in agente_keywords)
    
    acao_keywords = ['deve', 'devem', 'criar', 'promover', 'implementar', 'realizar', 'desenvolver', 'oferecer']
    has_acao = any(keyword in text.lower() for keyword in acao_keywords)
    
    if intervencao_count >= 3 and has_agente and has_acao:
        score += 200
        feedback.append('✅ Proposta de intervenção completa (agente, ação, detalhamento)')
    elif intervencao_count >= 2 and (has_agente or has_acao):
        score += 150
        feedback.append('⚠️ Proposta de intervenção presente, mas faltam elementos (agente/ação/detalhamento)')
    else:
        feedback.append('❌ Proposta de intervenção incompleta ou ausente')
    
    if score > max_score:
        score = max_score
    
    if score >= 800:
        nivel = 'Excelente'
    elif score >= 600:
        nivel = 'Bom'
    elif score >= 400:
        nivel = 'Regular'
    else:
        nivel = 'Precisa melhorar'
    
    feedback.insert(0, f'📊 Nota estimada: {score}/1000 - Nível: {nivel}')
    feedback.append('\n💡 Dica: Estude a estrutura dissertativa-argumentativa e pratique!')
    
    return score, feedback

@app.route('/')
def index():
    conn = get_db()
    areas = conn.execute('SELECT * FROM areas ORDER BY id').fetchall()
    total_resumos = conn.execute('SELECT COUNT(*) as count FROM resumos').fetchone()['count']
    conn.close()
    return render_template('index.html', areas=areas, total_resumos=total_resumos)

@app.route('/area/<int:area_id>')
def area(area_id):
    conn = get_db()
    area = conn.execute('SELECT * FROM areas WHERE id=?', (area_id,)).fetchone()
    topics = conn.execute('SELECT * FROM topics WHERE area_id=? ORDER BY title', (area_id,)).fetchall()
    conn.close()
    return render_template('area.html', area=area, topics=topics)

@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    conn = get_db()
    topic = conn.execute('SELECT * FROM topics WHERE id=?', (topic_id,)).fetchone()
    resumo = conn.execute('SELECT * FROM resumos WHERE topic_id=?', (topic_id,)).fetchone()
    explicacao = conn.execute('SELECT * FROM explicacoes WHERE topic_id=?', (topic_id,)).fetchone()
    questoes_count = conn.execute('SELECT COUNT(*) as count FROM questoes WHERE topic_id=?', (topic_id,)).fetchone()['count']
    conn.close()
    return render_template('topic.html', topic=topic, resumo=resumo, explicacao=explicacao, questoes_count=questoes_count)

@app.route('/resumos')
def resumos():
    search = request.args.get('search', '')
    area_filter = request.args.get('area', '')
    
    conn = get_db()
    
    if area_filter:
        query = '''SELECT r.*, t.title as topic_title, a.name as area_name 
                   FROM resumos r 
                   LEFT JOIN topics t ON r.topic_id=t.id 
                   LEFT JOIN areas a ON t.area_id=a.id
                   WHERE a.id=?'''
        params = (area_filter,)
    elif search:
        query = '''SELECT r.*, t.title as topic_title, a.name as area_name 
                   FROM resumos r 
                   LEFT JOIN topics t ON r.topic_id=t.id 
                   LEFT JOIN areas a ON t.area_id=a.id
                   WHERE r.title LIKE ? OR r.summary LIKE ?'''
        params = (f'%{search}%', f'%{search}%')
    else:
        query = '''SELECT r.*, t.title as topic_title, a.name as area_name 
                   FROM resumos r 
                   LEFT JOIN topics t ON r.topic_id=t.id 
                   LEFT JOIN areas a ON t.area_id=a.id
                   ORDER BY r.id'''
        params = ()
    
    rows = conn.execute(query, params).fetchall()
    areas = conn.execute('SELECT * FROM areas').fetchall()
    conn.close()
    return render_template('resumos.html', resumos=rows, areas=areas, search=search, area_filter=area_filter)

@app.route('/mapas')
def mapas():
    conn = get_db()
    areas = conn.execute('SELECT * FROM areas').fetchall()
    
    areas_with_topics = []
    for area in areas:
        topics = conn.execute('SELECT * FROM topics WHERE area_id=? ORDER BY title', (area['id'],)).fetchall()
        areas_with_topics.append({
            'area': area,
            'topics': topics
        })
    
    conn.close()
    return render_template('mapas.html', areas_with_topics=areas_with_topics)

@app.route('/redacao', methods=['GET', 'POST'])
def redacao():
    if request.method == 'POST':
        user_name = request.form.get('user_name', 'Anônimo')
        prompt = request.form.get('prompt', '')
        essay_text = request.form.get('essay_text', '')
        
        score, feedback = grade_essay(essay_text, prompt)
        
        conn = get_db()
        conn.execute('INSERT INTO essays (user_name, prompt, essay_text, score, feedback) VALUES (?,?,?,?,?)',
                    (user_name, prompt, essay_text, score, '\n'.join(feedback)))
        conn.commit()
        essay_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        
        return render_template('redacao.html', 
                             show_result=True, 
                             score=score, 
                             feedback=feedback,
                             essay_id=essay_id)
    
    return render_template('redacao.html', show_result=False)

@app.route('/cronograma', methods=['GET', 'POST'])
def cronograma():
    if request.method == 'POST':
        data = request.get_json()
        plan = data.get('plan', [])
        
        csv_path = Path('cronograma_enem.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Dia', 'Assunto', 'Duração (min)', 'Prioridade', 'Área'])
            for row in plan:
                writer.writerow([
                    row.get('day', ''),
                    row.get('topic', ''),
                    row.get('minutes', ''),
                    row.get('priority', ''),
                    row.get('area', '')
                ])
        
        return send_file(csv_path, as_attachment=True, download_name='cronograma_enem_2025.csv')
    
    conn = get_db()
    areas = conn.execute('SELECT * FROM areas').fetchall()
    topics = conn.execute('SELECT t.*, a.name as area_name FROM topics t JOIN areas a ON t.area_id=a.id ORDER BY a.id, t.title').fetchall()
    conn.close()
    
    return render_template('cronograma.html', areas=areas, topics=topics)

@app.route('/exercicios')
def exercicios():
    conn = get_db()
    areas = conn.execute('SELECT * FROM areas').fetchall()
    total_questoes = conn.execute('SELECT COUNT(*) as count FROM questoes').fetchone()['count']
    conn.close()
    return render_template('exercicios.html', areas=areas, total_questoes=total_questoes)

@app.route('/exercicios/area/<int:area_id>')
def exercicios_area(area_id):
    conn = get_db()
    area = conn.execute('SELECT * FROM areas WHERE id=?', (area_id,)).fetchone()
    questoes = conn.execute('''
        SELECT q.*, t.title as topic_title 
        FROM questoes q 
        JOIN topics t ON q.topic_id = t.id
        WHERE t.area_id = ?
        ORDER BY q.id
    ''', (area_id,)).fetchall()
    conn.close()
    return render_template('exercicios_area.html', area=area, questoes=questoes)

@app.route('/exercicios/questao/<int:questao_id>')
def questao(questao_id):
    conn = get_db()
    questao = conn.execute('SELECT q.*, t.title as topic_title FROM questoes q JOIN topics t ON q.topic_id = t.id WHERE q.id=?', (questao_id,)).fetchone()
    conn.close()
    return render_template('questao.html', questao=questao)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        admin_pass = os.getenv('ADMIN_PASS', 'admin123')
        
        if password == admin_pass:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Senha incorreta!', 'error')
            return redirect(url_for('admin'))
    
    if not session.get('admin'):
        return render_template('admin_login.html')
    
    conn = get_db()
    areas = conn.execute('SELECT * FROM areas').fetchall()
    topics = conn.execute('SELECT t.*, a.name as area_name FROM topics t JOIN areas a ON t.area_id=a.id ORDER BY t.id DESC LIMIT 20').fetchall()
    resumos = conn.execute('SELECT r.*, t.title as topic_title FROM resumos r LEFT JOIN topics t ON r.topic_id=t.id ORDER BY r.id DESC LIMIT 20').fetchall()
    essays = conn.execute('SELECT * FROM essays ORDER BY created_at DESC LIMIT 10').fetchall()
    conn.close()
    
    return render_template('admin.html', areas=areas, topics=topics, resumos=resumos, essays=essays)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/api/progress', methods=['POST'])
def mark_progress():
    data = request.get_json()
    user_name = data.get('user_name', 'Usuário')
    topic_id = data.get('topic_id')
    completed = data.get('completed', 1)
    
    conn = get_db()
    existing = conn.execute('SELECT * FROM progress WHERE user_name=? AND topic_id=?', (user_name, topic_id)).fetchone()
    
    if existing:
        conn.execute('UPDATE progress SET completed=?, last_reviewed=? WHERE user_name=? AND topic_id=?',
                    (completed, datetime.now(), user_name, topic_id))
    else:
        conn.execute('INSERT INTO progress (user_name, topic_id, completed, last_reviewed) VALUES (?,?,?,?)',
                    (user_name, topic_id, completed, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', quiz_started=False)

@app.route('/quiz/start', methods=['POST'])
def quiz_start():
    num_questions = int(request.form.get('num_questions', 20))
    
    conn = get_db()
    all_questions = conn.execute('SELECT * FROM questoes ORDER BY RANDOM() LIMIT ?', (num_questions,)).fetchall()
    conn.close()
    
    session['quiz_question_ids'] = [q['id'] for q in all_questions]
    
    return render_template('quiz.html', quiz_started=True, questions=all_questions)

@app.route('/quiz/submit', methods=['POST'])
def quiz_submit():
    quiz_question_ids = session.get('quiz_question_ids', [])
    
    if not quiz_question_ids:
        return redirect(url_for('quiz'))
    
    num_questions = len(quiz_question_ids)
    correct_count = 0
    results = []
    
    conn = get_db()
    
    for i, question_id_from_session in enumerate(quiz_question_ids, 1):
        question_id_from_form = request.form.get(f'question_{i}')
        user_answer = request.form.get(f'answer_{i}', '')
        
        if str(question_id_from_session) != str(question_id_from_form):
            conn.close()
            flash('Erro: Dados do quiz inválidos', 'error')
            return redirect(url_for('quiz'))
        
        db_question = conn.execute('SELECT * FROM questoes WHERE id=?', (question_id_from_session,)).fetchone()
        
        if db_question:
            correct_answer = db_question['resposta_correta']
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_num': i,
                'pergunta': db_question['pergunta'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explicacao': db_question['explicacao']
            })
    
    conn.close()
    
    score_percentage = (correct_count / num_questions * 100) if num_questions > 0 else 0
    is_approved = score_percentage >= 60
    
    session.pop('quiz_question_ids', None)
    
    return render_template('quiz_resultado.html', 
                         results=results, 
                         correct_count=correct_count, 
                         total_questions=num_questions,
                         score_percentage=score_percentage,
                         is_approved=is_approved)

if __name__ == '__main__':
    if not DB_PATH.exists():
        print('⚠️  Database not found. Please run: python db_init.py && python seed_resumos.py')
    app.run(host='0.0.0.0', port=5000, debug=True)
