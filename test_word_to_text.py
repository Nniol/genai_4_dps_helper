from genai_4_dps_helper.text_extractors import TextExtractors

SAMPLE_INPUT_FILENAME = "sample-docx-files-sample4.docx"
SAMPLE_OUTPUT_FILENAME = "sample-docx-files-sample4.txt"

extractors: TextExtractors = TextExtractors()
word_file_data: bytes = None

with open(SAMPLE_INPUT_FILENAME, "rb") as test_file:
    word_file_data = test_file.read()

text: str = extractors.word2text(SAMPLE_INPUT_FILENAME, word_file_data)

with open(SAMPLE_OUTPUT_FILENAME, "w") as test_file_output:
    test_file_output.write(text)
