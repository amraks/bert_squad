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
        'answer_start' : None,
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
        chapter_context_lower = chapter_context.lower()

        q_and_a_rows = []

        number_questions = 0
        for row in test_csv_reader:
            if not row:
                continue
            q_and_a_rows.append(row)

        for index, row in enumerate(q_and_a_rows):

            text = row[0]

            if re.match(r'^\s+\d{0,4}\.\s+', text): # question
                number_questions += 1

                # construct the answer map; option -> answer
                answer_map = {}
                final_answer = None
                final_answer_offset = -1

                # next 9 lines will be options + answers
                if index + 9 < len(q_and_a_rows):
                    j = index + 1
                    while j < index + 10:
                        answer_text = q_and_a_rows[j][0]
                        m = re.match(r'^\s*(?P<option>[a-d])\.\s*$', answer_text) # matches option
                        if m:
                            opt = m.group('option')
                            if j + 1 < len(q_and_a_rows):
                                next_line_after_option_text = q_and_a_rows[j+1][0]
                                answer_map[opt] = next_line_after_option_text
                        j += 1

                        m = re.match(r'^\s*ANS:\s*(?P<answer_option>[A-D]).*', answer_text) #matches 'ANS:'
                        if m:
                            answer_option = m.group('answer_option')
                            answer_option_lower = answer_option.lower()
                            if answer_option_lower in answer_map:
                                final_answer = (answer_map[answer_option_lower]).strip('.\n\t ')
                                final_answer_offset = chapter_context_lower.find(final_answer.lower())

                if final_answer:

                    # generate uuid
                    q_id = str(uuid.uuid4())
                    while q_id in used_uuids:
                        q_id = str(uuid.uuid4())
                    used_uuids.add(q_id)

                    squad_q_and_a_element_for_paragraph = get_q_and_a_element_for_paragraph()
                    squad_q_and_a_element_for_paragraph['id'] = q_id
                    squad_q_and_a_element_for_paragraph['question'] = get_question(text)

                    squad_answer_element = get_answer_element_for_q_and_a_element_within_paragraph()
                    squad_answer_element['text'] = final_answer
                    if final_answer_offset != -1: # only put valid offset
                        squad_answer_element['answer_start'] = final_answer_offset

                    squad_q_and_a_element_for_paragraph['answers'].append(squad_answer_element)
                    paragraph_element['qas'].append(squad_q_and_a_element_for_paragraph)

            if number_questions >= 50:
                break

        #chapter_number = get_chapter_number_from_file(test_file)

def main():
    chapters_dir = os.path.join(os.path.abspath('.'), "process_chapter")
    tests_dir = os.path.join(os.path.abspath('.'), "process_test")

    for chapter_file_name in os.listdir(chapters_dir):
        if not chapter_file_name.endswith('.csv'):
            continue
        test_file = get_test_file_for_chapter(tests_dir, chapter_file_name)
        chapter_file = os.path.join(chapters_dir, chapter_file_name)
        process_chapter(chapter_file, test_file)

    with open('squad_output_richard.json', 'w') as f:
        json.dump(squad_data, f)

if __name__ == '__main__':
    main()
