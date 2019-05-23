import os

def get_test_file_for_chapter(tests_dir, chapter_file_name):
     base, ext = chapter_file_name.replace('token', 'test').split('.')
     test_file_name = base + '_strip' + '.' + ext
     return os.path.join(tests_dir, test_file_name)

def main():
    chapters_dir = os.path.join(os.path.abspath('.'), "process_chapter")
    tests_dir = os.path.join(os.path.abspath('.'), "process_test")
    for chapter_file_name in os.listdir(chapters_dir):
        # only csv
        if not chapter_file_name.endswith('.csv'):
            continue

        test_file = get_test_file_for_chapter(tests_dir, chapter_file_name)
        chapter_file_csv = os.path.join(chapters_dir, chapter_file_name)

        print('ch_file:%s test_file:%s' % (chapter_file_csv, test_file))

if __name__ == '__main__':
    main()
