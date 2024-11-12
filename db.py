from datetime import datetime

import models

current_id = 0
DB = {}


def get_new_id():
    global current_id
    current_id += 1
    return current_id


def save_model(model):
    model.id = get_new_id()
    model.created_at = datetime.now()
    DB[model.id] = model
    return model


def get_all(page, page_size):
    data = sorted(list(DB.values()), key=lambda k: k.created_at, reverse=True)
    page = models.Page(items=data[(page - 1) * page_size: page * page_size],
                       hasMore=len(data) > page * page_size)
    return page


def get_by_id(id):
    return DB.get(id)
