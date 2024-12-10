import uuid
import re
from typing import Optional, Any

from fastapi import APIRouter, HTTPException
from app.core.es import ES_connector
from app.core.config import settings

router = APIRouter(prefix="/search", tags=["events|search"])
es = ES_connector()

index_name = settings.ES_INDEX
total_result_per_page = 10


def extract_filters(query):
    filters = []

    filter_regex = r'category:([^\s]+)\s*'
    m = re.search(filter_regex, query)
    if m:
        filters.append({
            'term': {
                'category.keyword': {
                    'value': m.group(1)
                }
            }
        })
        query = re.sub(filter_regex, '', query).strip()

    filter_regex = r'year:([^\s]+)\s*'
    m = re.search(filter_regex, query)
    if m:
        filters.append({
            'range': {
                'start_datetime': {
                    'gte': f'{m.group(1)}||/y',
                    'lte': f'{m.group(1)}||/y',
                }
            },
        })
        query = re.sub(filter_regex, '', query).strip()

    return {'filter': filters}, query


@router.get("/",
            summary="Lista los eventos en Elasticsearch",
            response_description="Lista de todos los eventos de Elasticsearch")
def handle_search(query: Optional[str] = "", start: Optional[int] = 0,
                  page_size: Optional[int] = 5) -> Any:
    """
    Busca los eventos en Elasticsearch de acuerdo al texto y filtros ingresados.
    Por defecto muestra los 5 primeros resultados.
    - **query**: opcional. Si no se envia nada en este campo, se muestran todos los eventos existentes 
        Ej: vallenato; vallenato category:Conciertos, category:Teatro
    - **start**: opcional
    - **page_size**: requopcionalerido
    """
    filters, parsed_query = extract_filters(query)

    if parsed_query:
        search_query = {
            'must': {
                'multi_match': {
                    'query': parsed_query,
                    'fields': ['title', 'description'],
                }
            }
        }
    else:
        search_query = {
            'must': {
                'match_all': {}
            }
        }

    event = es.search(index_name=index_name,
        query={
            'bool': {
                **search_query,
                **filters
            }
        },        
        aggs={
            'category-agg': {
                'terms': {
                    'field': 'category.keyword',
                }
            },
            'year-agg': {
                'date_histogram': {
                    'field': 'start_datetime',
                    'calendar_interval': 'year',
                    'format': 'yyyy',
                },
            },
        },
        size=page_size,
        from_=start
    )

    event_output = None
    if event and event["hits"]["hits"]:
        event_output = event["hits"]["hits"]
    return {"event_ouput": event_output}


@router.get("/{event_id}",
            summary="Lista un evento por id",
            response_description="Evento filtrado por id")
def read_event_id(event_id: uuid.UUID):

    document = es.retrieve_document(id)
    document = document['_source']
    event = {"id": event_id,
             "title": document["title"],
             "description": document["description"],
             "start_datetime": document["start_datetime"],
             "location": document["location"],
             "status": document["status"],
             "category": document["category"]}

    return event
