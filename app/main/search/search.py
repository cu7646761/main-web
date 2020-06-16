from app.search import add_to_index, query_full_text, query_fuzzy, query_suggestion


class KindSearch:
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        pass


class FullTextSearch(KindSearch):
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        return query_full_text(table_name, expression, page, per_page)


class FuzzySearch(KindSearch):
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        return query_fuzzy(table_name, expression, page, per_page)


class SuggestionSearch(KindSearch):
    @classmethod
    def query_index(cls, table_name, expression, page, per_page):
        return query_suggestion(table_name, expression)


class SearchableMixin(object):

    @classmethod
    def search(cls, expression, page, per_page, kind_search):
        print(cls.__tablename__)
        print(expression)
        ids, obj = kind_search.query_index(cls.__tablename__, expression, page, per_page)
        print(ids)
        print(obj)
        ids = [str(_id) for _id in ids]
        if len(obj) == 0:
            return cls.objects(id__exact=0), 0
        arr_model = []
        for _id in ids:
            try:
                arr_model.append(cls.objects.get(id=_id))
            except Exception as e:
                continue
        print(arr_model)
        return arr_model, obj

    @classmethod
    def reindex(cls):
        for obj in cls.objects:
            add_to_index(cls.__tablename__, obj)

    @classmethod
    def add_to_index_into_table(cls, obj):
        add_to_index(cls.__tablename__, obj)
