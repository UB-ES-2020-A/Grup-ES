import unittest

from tests.base_test import BaseTest
from model.library import LibraryModel, LibraryType, State


class UnitTestOfUS(BaseTest):

    # TEST TASK 2
    def test_model_add(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.Bought, State.Dropped)

            entry.save_to_db()
            self.assertEqual(entry, LibraryModel.find_by_id_and_isbn(1, 1))

    def test_model_add_duplicate(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.WishList, State.Reading)
            entry.save_to_db()

            same_entry = LibraryModel(1, 1, LibraryType.WishList, State.Reading)
            with self.assertRaises(Exception):
                same_entry.save_to_db()

    def test_model_delete(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.Bought)
            entry.save_to_db()
            entry.delete_from_db()

            self.assertEqual(False, entry.visible)

    def test_model_update(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.Bought, State.Finished)
            entry.save_to_db()

            data = {"isbn": 2, "user_id": 2, "state": "Reading", "visible": True, "library_type": "WishList"}
            entry.update_from_db(data)

            self.assertEqual(entry.json(), data)

    def test_model_invalid_update(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.WishList, State.Pending)
            entry.save_to_db()

            with self.assertRaises(Exception):
                data = {"isbn": 1, "user_id": 1, "state": "Pending2", "visible": True, "library_type": "WishList"}
                entry.update_from_db(data)


if __name__ == '__main__':
    unittest.main()
