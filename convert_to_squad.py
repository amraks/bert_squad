import re
import os
import csv
import uuid
import json

squad_data = {
    'data' : [
    ]
}

def get_test_file_for_chapter(tests_dir, chapter_file_name):
     base, ext = chapter_file_name.replace('token', 'test').split('.')
     test_file_name = base + '_strip' + '.' + ext
     return os.path.join(tests_dir, test_file_name)

def get_chapter_number_from_file(f):
    return os.path.basename(f).split('_ch')[1].split('_')[0]

def get_answer_element_for_q_and_a_element_within_paragraph():
    return {
        'answer_start' : '',
        'text' : ''
    }

def get_q_and_a_element_for_paragraph():
    return {
        'id' : '',
        'question' : '',
        'answers' : [

        ]
    }

def get_paragraph_element():
    return {
        'context' : '',
        'qas' : [

        ]
    }

def get_squad_element():
    return {
        'title' : '',
        'paragraphs' : [

        ],
    }

def get_chapter_title(s):
    return ' '.join(re.findall(r'[A-Z]{2,}', s)) or ''

def get_dump_element_template():
    return {
        'context' : '',
        'q_and_a' : [

        ]
    }

def get_chapter_context(chapter_rows):
    return ''.join([x[1] for x in chapter_rows])

def get_question(text):
    return re.split(r'\.', text)[1] if text and len(text.split()) >= 2 else ''

used_uuids = set()

def process_chapter(chapter_file, test_file):
    with open(chapter_file) as chapter_fh, open(test_file) as test_fh:
        chapter_csv_reader = csv.reader(chapter_fh)
        test_csv_reader = csv.reader(test_fh)

        chapter_rows = []
        for row in chapter_csv_reader:
            row = [s.strip() for s in row if s]
            if len(row) != 2:
                continue
            # format of row: ['id', 'content']
            chapter_rows.append(row)

        squad_element = get_squad_element()
        squad_data['data'].append(squad_element)

        # 1st row has the title
        chapter_title = get_chapter_title(chapter_rows[0][1])
        squad_element['title'] = chapter_title
        chapter_context = get_chapter_context(chapter_rows)
        paragraph_element = get_paragraph_element()
        paragraph_element['context'] = chapter_context
        squad_element['paragraphs'].append(paragraph_element)

        q_and_a_rows = []

        number_questions = 0
        for row in test_csv_reader:
            if not row:
                continue

            text = row[0]

            if re.match(r'^\s+\d{0,4}\.\s+', text):
                # Question
                number_questions += 1
                # generate uuid
                q_id = str(uuid.uuid4())
                while q_id in used_uuids:
                    q_id = str(uuid.uuid4())
                used_uuids.add(q_id)
                squad_q_and_a_element_for_paragraph = get_q_and_a_element_for_paragraph()
                squad_q_and_a_element_for_paragraph['id'] = q_id
                squad_q_and_a_element_for_paragraph['question'] = get_question(text)
                paragraph_element['qas'].append(squad_q_and_a_element_for_paragraph)

        chapter_number = get_chapter_number_from_file(test_file)
        print('chapter %s:%s number_questions:%s' % (chapter_number, chapter_title, number_questions))

def main():
    chapters_dir = os.path.join(os.path.abspath('.'), "process_chapter")
    tests_dir = os.path.join(os.path.abspath('.'), "process_test")
    for chapter_file_name in os.listdir(chapters_dir):
        if not chapter_file_name.endswith('.csv'):
            continue
        test_file = get_test_file_for_chapter(tests_dir, chapter_file_name)
        chapter_file = os.path.join(chapters_dir, chapter_file_name)
        process_chapter(chapter_file, test_file)
        #break
    print(json.dumps(squad_data))

if __name__ == '__main__':
    main()
