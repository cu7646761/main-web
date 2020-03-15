from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload, doc_type={})


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_full_text(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [hit['_id'] for hit in search['hits']['hits']]
    return ids, search['hits']['hits']


def query_fuzzy(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*'], 'fuzziness': '3'}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [hit['_id'] for hit in search['hits']['hits']]
    return ids, search['hits']['hits']


def query_suggestion(index, query):
    if not current_app.elasticsearch:
        return [], 0

    field_all = ["name"]

    ids_all = []
    search_obj_all = []
    for field in field_all:
        search = current_app.elasticsearch.search(
            index=index,
            body={
                'query':
                    {
                        'match_phrase_prefix':
                            {
                                field:
                                    {
                                        'query': query,
                                        'slop': 3,
                                        'max_expansions': 10
                                    }
                            }
                    },
            })
        ids = [hit['_id'] for hit in search['hits']['hits']]
        ids_all.extend(ids)
        search_obj_all.extend(search['hits']['hits'])

    return ids_all, search_obj_all
