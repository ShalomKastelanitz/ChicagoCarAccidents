from database.connect import accidents,injuries


def insertManyDocuments(name_collection, my_list):
    try:
        if name_collection == 'accidents':
            accidents.insert_many(my_list)
        else:
            injuries.insert_many(my_list)
    except Exception as e:
        print(f"An error occurred: {e}")
