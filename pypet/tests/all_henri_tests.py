__author__ = 'Henri Bunting'


from pypet.tests.testutils.ioutils import run_suite, discover_tests, TEST_IMPORT_ERROR, parse_args


if __name__ == '__main__':
    opt_dict = parse_args()
    suite = discover_tests(predicate=lambda class_name, test_name, tags: 'henri' in tags)

    run_suite(suite=suite, **opt_dict)