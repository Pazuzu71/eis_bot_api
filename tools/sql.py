from datetime import datetime
import os

import asyncpg


async def create_pool(**kwargs):
    pool = await asyncpg.create_pool(**kwargs)
    return pool


async def create_tables(pool: asyncpg.Pool):
    await pool.execute(
        '''
            create table if not exists callbacks
            (
                id SERIAL PRIMARY KEY,
                path VARCHAR,
                eispublicationdate timestamp with time zone,
                creationdate timestamp
            )
        '''
    )


async def create_callback(pool: asyncpg.Pool, WORK_DIR, file, eispublicationdate):
    path = os.path.join(WORK_DIR, file)
    await pool.execute('''INSERT INTO callbacks (path, eispublicationdate, creationdate) VALUES ($1, $2, $3)''',
                       path, eispublicationdate, datetime.now()
                       )
    doc_id = await pool.execute('''select id from callbacks where path = $1 and eispublicationdate = $2''',
                                path, eispublicationdate
                                )
    return doc_id
