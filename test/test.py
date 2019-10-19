#     def test_load_from_file(self):
#         #TODO : test qui assure que le fichier JSON est lu et que la classe est instanciée
#         address_book = AddressBook.load_from_file(FILENAME)
#         assert address_book is not None
#         assert len(address_book.addresses) == 1
#         pass
#
# class TestApp(object):
#     def test_index(self):
#         #TODO : rajouter un test qui assure que l'index retourne un 200 avec le nom des personnes du carnet d'adresse
#         client = app.test_client()
#         response = client.get("/")
#         assert response.status_code == 200
#         assert b"Gaston Lagaffe" in response.data
#         pass
#
#     def test_address(self):
#         client = app.test_client()
#
#         response = client.get("/0")
#         assert response.status_code == 200
#         assert b"Gaston Lagaffe" in response.data
#
#     def test_address_does_not_exist(self):
#         client = app.test_client()
#
#         response = client.get("/999")
#         assert response.status_code == 404
#
#     def test_new_address(self):
#         client = app.test_client()
#
#         response = client.get("/new")
#         assert response.status_code == 200
