import os
import csv

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

def get_context_key(chapter_number):
    return 'chapter-%s' % chapter_number

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

def get_chapter_title(chapter_row):
    pass

def process_chapter(chapter_file, test_file):
    with open(chapter_file) as chapter_fh, open(test_file) as test_fh:
        chapter_csv_reader = csv.reader(chapter_fh)
        test_csv_reader = csv.reader(test_fh)

        chapter_number = get_chapter_number_from_file(test_file)
        ctx_key = get_context_key(chapter_number)

        chapter_rows = []
        for row in chapter_csv_reader:
            row = [s.strip() for s in row if s]
            if len(row) != 2:
                continue
            chapter_rows.append(row)

        chapter_title = get_chapter_title(chapter_rows[0])
        print('Title:%s' % chapter_rows[0])

def main():
    chapters_dir = os.path.join(os.path.abspath('.'), "process_chapter")
    tests_dir = os.path.join(os.path.abspath('.'), "process_test")
    for chapter_file_name in os.listdir(chapters_dir):
        if not chapter_file_name.endswith('.csv'):
            continue
        test_file = get_test_file_for_chapter(tests_dir, chapter_file_name)
        chapter_file = os.path.join(chapters_dir, chapter_file_name)
        process_chapter(chapter_file, test_file)

if __name__ == '__main__':
    main()
