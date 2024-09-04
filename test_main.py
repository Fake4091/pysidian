import unittest
import os
from main import *


class test_Note(unittest.TestCase):
    def tearDown(self) -> None:
        for i in os.listdir():
            if i.endswith(".txt"):
                os.remove(i)

    def test_init(self):
        self.assertEqual(notes, [])
        self.assertEqual(titles, [])
        Note("This", "That", False)
        self.assertEqual(notes[0].title, "This")
        self.assertEqual(notes[0].content, "That")
        self.assertEqual(notes[0].important, False)
        self.assertEqual(titles, ["This"])

    def test_write(self):
        self.assertNotIn("This.txt", os.listdir())
        self.assertNotIn("This_relationships.txt", os.listdir())
        Note("This", "That", False).writeToFile()
        self.assertIn("This.txt", os.listdir())
        self.assertIn("This_relationships.txt", os.listdir())

    def test_relate(self):
        note1 = Note("This", "That")
        note1.writeToFile()
        note2 = Note("That", "This")
        note2.writeToFile()
        note2.relate(note1.title)
        with open(f"{note1.title}_relationships.txt", "r") as f:
            self.assertIn(f"{note2.title}\n", f.readlines())
        with open(f"{note2.title}_relationships.txt", "r") as f:
            self.assertIn(f"{note1.title}\n", f.readlines())

    def test_unrelate(self):
        note1 = Note("This", "That")
        note1.writeToFile()
        note2 = Note("That", "This")
        note2.writeToFile()
        note2.relate(note1.title)
        note2.unrelate(note1.title)
        self.assertNotIn(
            f"{note1.title}\n", open(f"{note2.title}_relationships.txt").readlines()
        )
        self.assertNotIn(
            f"{note2.title}\n", open(f"{note1.title}_relationships.txt").readlines()
        )

    def test_markImportant(self):
        note1 = Note("This", "That")
        note1.writeToFile()
        note1.markImportant()
        self.assertEqual(note1.important, True)
        self.assertIn(
            "Important\n", open(f"{note1.title}_relationships.txt").readlines()
        )

    def test_unmarkImportant(self):
        note1 = Note("This", "That")
        note1.writeToFile()
        note1.markImportant()
        self.assertEqual(note1.important, True)
        self.assertIn(
            "Important\n", open(f"{note1.title}_relationships.txt").readlines()
        )
        note1.unmarkImportant()
        self.assertEqual(note1.important, False)
        self.assertNotIn(
            "Important\n", open(f"{note1.title}_relationships.txt").readlines()
        )


def test_newNote():
    newNote("This", "That")
    assert "This.txt" in os.listdir()
    with open("This.txt", "r") as f:
        assert f.read() == "That"
    assert "This_relationships.txt" in os.listdir()
    with open("This_relationships.txt", "r") as f:
        assert f.read() == ""


def test_editNote():
    newNote("This", "That")
    assert "This.txt" in os.listdir()
    with open("This.txt", "r") as f:
        assert f.read() == "That"
    editNote("This", "New")
    with open("This.txt", "r") as f:
        assert f.read() == "New"


def test_delNote():
    newNote("This", "That")
    assert "This.txt" in os.listdir()
    delNote("This")
    assert "This.txt" not in os.listdir()


def test_delNote_related():
    note1 = Note("This", "That")
    note1.writeToFile()
    note2 = Note("That", "This")
    note2.writeToFile()
    note1.relate(note2.title)
    assert "This_relationships.txt" in os.listdir()
    assert "That_relationships.txt" in os.listdir()
    with open("This_relationships.txt", "r") as f:
        assert "That\n" in f.readlines()
    with open("That_relationships.txt", "r") as f:
        assert "This\n" in f.readlines()
    delNote("This")
    assert "This_relationships.txt" not in os.listdir()
    assert "That_relationships.txt" in os.listdir()
    with open("That_relationships.txt", "r") as f:
        assert "This\n" not in f.readlines()


def test_relNote():
    note1 = Note("This", "That")
    note2 = Note("That", "This")
    relNote(note1.title, note2.title)
    assert "This_relationships.txt" in os.listdir()
    assert "That_relationships.txt" in os.listdir()
    with open("This_relationships.txt", "r") as f:
        assert "That\n" in f.readlines()
    with open("That_relationships.txt", "r") as f:
        assert "This\n" in f.readlines()


def test_unRelNote():
    note1 = Note("This", "That")
    note2 = Note("That", "This")
    relNote(note1.title, note2.title)
    assert "This_relationships.txt" in os.listdir()
    assert "That_relationships.txt" in os.listdir()
    with open("This_relationships.txt", "r") as f:
        assert "That\n" in f.readlines()
    with open("That_relationships.txt", "r") as f:
        assert "This\n" in f.readlines()
    unRelNote(note1.title, note2.title)
    assert "This_relationships.txt" in os.listdir()
    assert "That_relationships.txt" in os.listdir()
    with open("This_relationships.txt", "r") as f:
        assert "That\n" not in f.readlines()
    with open("That_relationships.txt", "r") as f:
        assert "This\n" not in f.readlines()


def test_markImportant():
    note1 = Note("This", "That")
    note1.markImportant()
    assert "Important\n" in open(f"{note1.title}_relationships.txt").readlines()
    assert note1.important == True


def test_unmarkImportant():
    note1 = Note("This", "That")
    note1.markImportant()
    assert "Important\n" in open(f"{note1.title}_relationships.txt").readlines()
    assert note1.important == True
    note1.unmarkImportant()
    assert "Important\n" not in open(f"{note1.title}_relationships.txt").readlines()
    assert note1.important == False
