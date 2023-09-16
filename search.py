from common import PDF_INDEX, elasticsearch as es


def search_pdf_text(keywords):
    should_clauses = [{'match': {'text': keyword}} for keyword in keywords]
    query = {
        'bool': {
            'should': should_clauses
        }
    }

    # Perform the search using the standard Elasticsearch client
    search_result = es.search(index=PDF_INDEX, body={'query': query})
    hits = search_result.get('hits', {}).get('hits', [])
    if not hits:
        print(f"No hits on query {keywords}")
        return []
    for hit in hits:
        print(hit.get("_id", "Error: Malformatted response"))
    return list(map(lambda x: {"id": hit.get("_id"), "text": hit.get("_source").get("text")}, hits))


def search_pdf_context(vector):
    pass
