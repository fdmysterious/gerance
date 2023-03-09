from gerance.gherkin import test_file

tests = test_file.parse("features/test.feature")

print(list(tests))
print(list(test_file.load_from_dir("features")))

