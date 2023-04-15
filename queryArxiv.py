import arxiv
from arxiv import SortCriterion
from arxiv import SortOrder
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import insert, select
from sqlalchemy import MetaData

from config import postgresIP, postgrsDB, postgrsPort, postgrsUser, postgrsPass 
from config import arxivCategories

from utils import upsert, build_postgrs_uri


currentWeekday = dt.datetime.today().weekday()
if currentWeekday == 5:
    TDELT = 2
elif currentWeekday == 6:
    TDELT = 3
else:
    TDELT = 1
for cat in arxivCategories:
    r = arxiv.Search(
        query = f"cat:{cat}",
        id_list = [],
        max_results = 300,
        sort_by = SortCriterion.SubmittedDate,
        sort_order = SortOrder.Descending,
    )

    key = build_postgrs_uri(postgresIP, postgrsPort, postgrsUser, postgrsPass, postgrsDB)

    engine = create_engine(key)

    with engine.connect() as connection:
        metadata = MetaData()
        metadata.reflect(connection)
        arxivsummary = metadata.tables['arxivsummary']
        for result in r.results():
            if result.published.date() == dt.datetime.today().date() - dt.timedelta(TDELT):
                ID = result.get_short_id()

                rs = connection.execute(text(f"SELECT COUNT(id) FROM arxivsummary WHERE arxiv_id = '{ID}'"))
                count = rs.fetchone()[0]

                if count == 0:
                    title = result.title
                    print(f"Adding {title} to database")
                    authors = ', '.join([x.name for x in result.authors])
                    published = result.published.date()
                    firstAuthor = result.authors[0].name
                    pdf_url = result.pdf_url
                    summary = result.summary
                    comments = result.comment
                    doi = result.doi
                    journal_ref = result.journal_ref
                    subject = cat
                    today = dt.datetime.today().date()

                    stmt = insert(arxivsummary).values(arxiv_id = ID, title = title, author_list = authors, published_date = published, first_author = firstAuthor, url = pdf_url, abstract = summary, comments = comments, doi = doi, added_date = today, subjects = subject)
                    compiled = stmt.compile()
                    InputResult = connection.execute(stmt)
                    connection.commit()

                    stmt = select(arxivsummary).where(arxivsummary.c.arxiv_id == ID)
                    rs = connection.execute(stmt)
                    paper = rs.fetchone()

                    vecInput = "Title: " + paper.title + "\n" + " Authors: " + paper.author_list + "\n" +  " Published: " + str(paper.published_date) + "\n" +  " URL: " + paper.url + "\n" + " ID: " + ID + "\n" + "Abstract: " + paper.abstract

                    upsert(ID, vecInput)

                else:
                    print(f"Skipping {ID} because it's already in the database")

            else:
                break


