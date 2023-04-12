# Paper.GPT

This is a simple test to see if gpt-3.5-turbo can effectivley summarize a paper
given in a pdf form and then answer questions about that paper

## Installation
Install the requirments

	1) PyPDF2
	2) openai
	3) git clone this repository

## Setup
You will need a working openAI api key (I have found that one summarized paper tends to cost about 5 cents based on the Mid august 2023 openAI API pricing)

Once you have your api key place it in a file called key.pem in the same directory as you will be running the summarize script from (only put the key in there). Make sure not to share this key and MAKE SURE NOT TO ADD IT TO A GIT REPO! The git ignore for this repo ignores key.pem and all *.pem files...HOWEVER if you name it something else and then modify the summarize script to read that different file it may accidently get read. You can also (and probably should) set an env variable for your api key (to avoid this risk)

## Usage
Once everything is setup you can use the script as follows

```bash
python summarize.py <path/to/paper.pdf>
```

This will send each page of the paper to gpt-3.5-turbo and summarize each page. Then all
those summaries will be passed in at once at the end and an executive summary will be made.

At this point you will be asked if you want to ask any questions. If you ask a question the 
summaries of each page will be passed back to gpt-3.5-turbo along with your question and its response will be printed. This will continue in an infinite loop. You can close this by typing q or Q into the question prompt.

## Notes
This is for experimental purposes only and should not be used as a legitimate tool
of academic inquiry.
