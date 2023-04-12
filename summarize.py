from PyPDF2 import PdfReader
import openai
import sys
import pickle as pkl

with open('key.pem', 'r') as f:
    key = f.read().strip()
openai.api_key = key

if __name__ == '__main__':
    filename = sys.argv[1]
    pdf = PdfReader(filename)

    print('Number of pages: {}'.format(len(pdf.pages)))
    totalPages = len(pdf.pages)

    summaries = list()
    for pageID, page in enumerate(pdf.pages):
        print('Extracting Page {}'.format(pageID))
        pageContent = page.extract_text()
        r = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': "You are a scientific paper summarizer"},
                    {'role': 'user', 'content': "You are a scientific paper summarizer. I have provided a single page of an academic paper. Please summarize that page in whatever way you see best. If the authors, title, publication data, and journal are given on the provided page make sure to clearly note them so that they can be pulled out for latter use. Finally, while writing keep in mind that after each page has been handed to you every individual summary you wrote will be passed back to you at once in order for you to generate an overall summary" },
                    {'role': 'user', 'content': pageContent}
                    ]
                )
        textReply = r.choices[0].message.content
        summaries.append(textReply)
        print("page {} summarized".format(pageID))

    with open('summaries.txt', 'w') as f:
        f.write('\n'.join(summaries))

    print("Summarizing all pages...")
    r = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': "You are a scientific paper summarizer"},
                {'role': 'user', 'content': "I have previously passed each page of the paper to you individually. Now I would like you to summarize the entire paper. Please keep in mind that the paper has {} pages. Present the summary in the following format\n\nTITLE: Some title\nAUTHOR(S): Author(s)\nPUBLICATION DATE: MM/DD/YYY\nJOURNAL: Journal Name\nSUMMARY: summary. If the title, author, publication data, or journal are not given in any summary simply leave that line out of the reply".format(totalPages)},
                {'role': 'user', 'content': '\n'.join(summaries)}
                ]
            )
    textReply = r.choices[0].message.content
    with open('reply.pkl', 'wb') as f:
        pkl.dump(r, f)
    print(textReply)

    while True:
        userQuery = input("Question about the summarized paper: ")

        if userQuery.lower() == 'q':
            break

        print("Asking GPT-3 to answer the question...")
        r = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': "You are a scientific paper summarizer"},
                    {'role': 'user', 'content': "Here is the of each page of an academic paper which you previously wrote. Each line The summary should be in page order. Additionally, I have asked a question. Please answer the question which follows the keyword %QUESTION% based on the provided paper summary. If you think you do not have enough information to answer the question please say so."},
                    {'role': 'user', 'content': '\n'.join(summaries)},
                    {'role': 'user', 'content': f"%QUESTION% {userQuery}"}
                    ]
                )
        textReply = r.choices[0].message.content
        print(textReply)





