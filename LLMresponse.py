import pickle

Qfile = open('qa_chain_instructEmbed.pkl', 'rb')
modelF = pickle.load(Qfile)
Qfile.close()

## Cite sources

import textwrap

def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')
    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)
    return wrapped_text

def process_llm_response(llm_response):
    # print(wrap_text_preserve_newlines(llm_response['result']))
    # print('\nSources:')
    outcome = wrap_text_preserve_newlines(llm_response['result'])
    for source in llm_response["source_documents"]:
        source.metadata['source']
    return outcome

#llm_response = modelF('hi')
#outAns = process_llm_response(llm_response)
#print('ans', outAns)