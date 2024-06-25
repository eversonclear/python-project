from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])


def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)


def index_task(task):
    es.index(
        index="tasks",
        id=task.id,
        body={
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "complete": task.complete,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        },
    )


def search_tasks(query, user_id):
    response = es.search(
        index="tasks",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"user_id": user_id}},
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title", "description"],
                            }
                        },
                    ]
                }
            }
        },
    )
    return response["hits"]["hits"]


def delete_index_task(task_id):
    es.delete(index="tasks", id=task_id)
