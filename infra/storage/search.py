import logging

from dataclasses import asdict
from typing import Any, Iterable, Dict, Optional, List
from uuid import UUID

from elasticsearch import Elasticsearch

from core.entities import Email

logger = logging.getLogger(__name__)


class EmailSearchRepo:
    client: Elasticsearch
    index: str = 'email'

    def __init__(self):
        self.client = Elasticsearch(hosts=['http://localhost:9200'])

    def add(self, obj: Email):
        res = self.client.index(index=self.index, id=str(obj.id), document=asdict(obj))
        logger.info(f'Added email to search: {asdict(obj)}: result: {res}')
        return res

    def get(self, pk: UUID) -> Optional[Email]:
        res = self.client.get(index=self.index, id=str(pk))
        eml = Email(**res['_source'])
        logger.info(f'get email fr search: {res}: result: {eml}')
        return eml

    def search(self, text: str) -> List[Email]:
        q = {
            "query_string": {
                "query": text,
            }
        }
        res = self.client.search(
            index=self.index,
            query=q,
            highlight={"fields": {'*': {}}},
            sort=[
                {'_score': {'order': 'desc'}},
                {'updated_at': {'order': 'desc'}},
            ]
        )

        return [
            Email(**e['_source'])
            for e in res['hits']['hits']
        ]
