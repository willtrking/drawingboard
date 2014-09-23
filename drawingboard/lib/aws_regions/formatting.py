# coding: utf-8

def formatted_row(row):
    return {
        'id' : int(row['id']),
        'name' : row['name'],
        'region' : row['region']
    }