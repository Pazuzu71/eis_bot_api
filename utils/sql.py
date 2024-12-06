from datetime import datetime
import os

import asyncpg


async def create_tables(pool: asyncpg.Pool):
    await pool.execute(
        '''
            create table if not exists paths
            (
                id SERIAL PRIMARY KEY,
                path VARCHAR,
                creationdate timestamp
            )
        '''
    )


async def create_path(pool: asyncpg.Pool, WORK_DIR, file):
    path = os.path.join(WORK_DIR, file)
    await pool.execute('''INSERT INTO paths (path, creationdate) VALUES ($1, $2)''',
                       path, datetime.now()
                       )
    # doc_id = await pool.execute('''select id from callbacks where path = $1''',
    #                             path
    #                             )
    doc_id = await pool.fetchrow('''select max(id) from paths where path = $1''',
                                 path
                                 )
    print('doc_id', doc_id)
    return doc_id[0]


async def get_path(pool: asyncpg.Pool, doc_id):
    path = await pool.fetchrow('''select path from paths where id = $1''', doc_id)
    return path[0]
