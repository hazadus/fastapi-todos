"""Содержит константы, используемые во всём приложении."""

from sqlalchemy import TextClause, text

CURRENT_TIMESTAMP_UTC: TextClause = text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")
