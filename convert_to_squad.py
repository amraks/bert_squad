import os
import csv

def get_test_file_for_chapter(tests_dir, chapter_file_name):
     base, ext = chapter_file_name.replace('token', 'test').split('.')
     test_file_name = base + '_strip' + '.' + ext
     return os.path.join(tests_dir, test_file_name)

def get_chapter_number(chapter_file):
    return os.path.basename(chapter_file).split('_ch')[1].split('_')[0]

def process_chapter(chapter_file, test_file):
    with open(chapter_file) as chapter_fh, open(test_file) as test_fh:
        chapter_csv_reader = csv.reader(chapter_fh)
        test_csv_reader = csv.reader(test_fh)

        chapter_number = get_chapter_number(chapter_file)

        print('chapter %s' % chapter_number)
        for row in chapter_csv_reader:
            values = [s.strip() for s in row if s]
            print(values)


def main():
    chapters_dir = os.path.join(os.path.abspath('.'), "process_chapter")
    tests_dir = os.path.join(os.path.abspath('.'), "process_test")
    for chapter_file_name in os.listdir(chapters_dir):
        # only csv
        if not chapter_file_name.endswith('.csv'):
            continue

        test_file = get_test_file_for_chapter(tests_dir, chapter_file_name)
        chapter_file = os.path.join(chapters_dir, chapter_file_name)

        process_chapter(chapter_file, test_file)

if __name__ == '__main__':
    main()
