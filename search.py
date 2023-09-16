from common import PDF_INDEX, elasticsearch as es


def search_pdf_text(keyword):
    search_result = es.search(index=PDF_INDEX, body={'query': {'match': {'text': keyword}}})
    hits = search_result.get('hits', {}).get('hits', [])
    if not hits:
        print(f"No hits on query {keyword}")
        return []
    for hit in hits:
        print(hit.get("_id", "Error: Malformatted response"))
    return list(map(lambda x: {"id": hit.get("_id"), "text": hit.get("_source").get("text")}, hits))