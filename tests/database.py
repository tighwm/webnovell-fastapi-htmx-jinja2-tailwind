import threading

from sqlalchemy.ext import asyncio as sa_asyncio

# https://docs.sqlalchemy.org/en/20/orm/contextual.html
# https://factoryboy.readthedocs.io/en/stable/orms.html#managing-sessions
async_scoped_session = sa_asyncio.async_scoped_session(
    sa_asyncio.async_sessionmaker(),
    threading.get_ident,
)
