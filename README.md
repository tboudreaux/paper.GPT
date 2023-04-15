# Paper.GPT

This is a simple test to see if gpt-3.5-turbo can effectivley summarize a paper
given in a pdf form and then answer questions about that paper (<a href="https://algebrist.ddns.net/~tboudreaux/files/summaryResults.html">live demo</a>)

## Installation
Install the requirments

	1) PyPDF2
	2) openai
	3) Milvus
	4) postgres
	5) GPT-retreival-api
	3) git clone this repository

## Setup
You will need a working openAI api key (I have found that one summarized paper
tends to cost about 0.1 cents based on the Mid april 2023 openAI API pricing)

Once you have your api key place it in a file called key.pem in the same
directory as you will be running the summarize script from (only put the key in
there). Make sure not to share this key and MAKE SURE NOT TO ADD IT TO A GIT
REPO! The git ignore for this repo ignores key.pem and all *.pem
files...HOWEVER if you name it something else and then modify the summarize
script to read that different file it may accidently get read. You can also
(and probably should) set an env variable for your api key (to avoid this risk)

You will then need to setup a table in a postgres database called arxiv schema
with the following schema

```sql
CREATE TABLE arxivSummary 
(id SERIAL PRIMARY KEY, 
title VARCHAR(200) NOT NULL, 
first_author VARCHAR(100) NULL, 
author_list VARCHAR(5000) NULL, 
url VARCHAR(100) NOT NULL, 
abstract VARCHAR(5000) NULL, 
comments VARCHAR(5000), 
published_date DATE NOT NULL, 
added_date DATE NOT NULL DEFAULT CURRENT_DATE, 
last_used DATE NULL, 
arxiv_id VARCHAR(30) NULL, 
doi VARCHAR(100) NULL, 
subjects VARCHAR(200) NULL, 
hasTex BOOLEAN NULL)
```

Also you will need to go through the steps to setup the GPT-Retrival-API (given
on their repository). You do not need to use Milvus; however, if you choose to
use another vector database such as pinecone you will need to modify the
enviromental variables which you set

Finally, setup all the variables in config.py.user and then rename that file to
config.py, also make sure to update the paths in the bash script summarize.sh
if you wish to use that.

## Usage
Once everything is setup you can use the script as follows

```bash
./summarize.sh
```

This will first query the arxiv for all papers in every catagory given in
config.py for that day and register each of them first in a relational databse
and then send them to the openAI retrival api for text embedding. The ebmedding
vectors will be sent to a vector database (configured as milvus). If a paper is
detectedf to already be in the relational databse then it will be fully
skipped.

Next, each paper title in the relational database will be looped over and
passed to the retrival api again, along with a prompt asking it to summarize in
1-2 sentences. This will get the embeddings from the vector databse and then
pass them to gpt-3.5-turbo. The response from gpt will be written out to an
html file called ./summaryResults.html. 

This file will be copied to some location on your computer (remove this step if
you want its not important if you dont want to host the html as a static
website)

Finally, the html file will be emailed out to every email in the emails list in
config.py

Overall I find that this takes about 5 mintues and 10 cents to summarize the
entire astro-ph arxiv (based on the April 2023 openAI api prices)


## Notes
This is for experimental purposes only and should not be used as a legitimate
tool of academic inquiry.
