#!/usr/bin/python3
import os

# initialize variables that hold all notes and titles
notes = []
titles = []


class Note:

    # making a new note sets its values and adds it to the lists
    def __init__(self, title, content, important=False):
        self.title = title
        self.content = content
        self.important = important
        notes.append(self)
        titles.append(self.title)

    # function for writing content to a file and initializing a relationships file. hidden from direct user access.
    def writeToFile(self, relationships=[]):

        # write main note to disk
        with open(f"{self.title}.txt", "w") as file:
            file.write(self.content)

        # make / clear relationships file
        with open(f"{self.title}_relationships.txt", "w") as file:
            pass

        # add relationships to file
        with open(f"{self.title}_relationships.txt", "a") as file:
            for i in relationships:
                file.write(f"{i}\n")

    # function for relating two notes together. hidden from direct user access.
    def relate(self, note: str):
        # add each other's name to each others relationships file
        with open(f"{self.title}_relationships.txt", "a") as f:
            f.write(f"{note}\n")
        with open(f"{note}_relationships.txt", "a") as f:
            f.write(f"{self.title}\n")

    # function for unrelating two notes. hidden from direct user access.
    def unrelate(self, note: str):
        note1rel = []
        note2rel = []
        tmprel = []

        # get old relationships and strip them of \n
        with open(f"{self.title}_relationships.txt", "r") as f:
            note1rel = f.readlines()
        for i in note1rel:
            tmprel.append(i.strip())
        note1rel = tmprel

        # if the note is in the relationship list for self, make a new list with everything except the note's name and write that as self's new list
        if note in note1rel:
            newnote1rel = []
            for i in note1rel:
                if i != f"{note}":
                    newnote1rel.append(i)
            if newnote1rel != []:
                self.writeToFile(newnote1rel)
            else:
                self.writeToFile()

            # then repeat for that note's relationships
            with open(f"{note}_relationships.txt", "r") as f:
                note2rel = f.readlines()
            for i in note2rel:
                tmprel.append(i.strip())
            note2rel = tmprel
            newnote2rel = []
            for i in note2rel:
                if i != f"{self.title}":
                    newnote2rel.append(i)
            if newnote1rel != []:
                notes[titles.index(note)].writeToFile(newnote2rel)
            else:
                notes[titles.index(note)].writeToFile()

    # function for marking note as important
    def markImportant(self):
        # mark note as important in memory, then try marking in file
        self.important = True
        try:
            oldRel = []
            # only add important if it isn't already in the file
            with open(f"{self.title}_relationships.txt", "r") as f:
                oldRel = f.readlines()
            if "Important\n" not in oldRel:
                with open(f"{self.title}_relationships.txt", "a") as f:
                    f.write("Important\n")
        # if the file doesn't exist, create it and mark as important
        except FileNotFoundError:
            with open(f"{self.title}_relationships.txt", "w") as f:
                f.write("Important\n")

    # function for unmarking note as important
    def unmarkImportant(self):
        # mark note as unimportant in memory, then try marking in file
        self.important = False
        try:
            oldRel = []
            newRel = []
            # cycle through old relationships and rewrite every one except important to relationships file
            with open(f"{self.title}_relationships.txt", "r") as f:
                oldRel = f.readlines()
            if "Important\n" in oldRel:
                for i in oldRel:
                    if i != "Important\n":
                        newRel.append(i)
                if newRel != []:
                    with open(f"{self.title}_relationships.txt", "w") as f:
                        pass
                    with open(f"{self.title}_relationships.txt", "a"):
                        for i in newRel:
                            f.write(i)
                # if the notes relationships are empty without important, clear the file
                else:
                    with open(f"{self.title}_relationships.txt", "w") as f:
                        pass
        # if the file doesn't exist, create it
        except FileNotFoundError:
            with open(f"{self.title}_relationships.txt", "w") as f:
                pass


# function for asking the user what they want to do
def askAction() -> str:
    # action loops until it gets a valid action
    while True:
        # take action input
        action = input(
            "\nWould you like to [view] existing notes, write a [new] note, [edit] a note, [delete] a note,\n[rel]ate two notes, [unrel]ate two notes, [mark] a note as important, [unmark] an important note, or [quit]? "
        )
        # verify action is valid
        if (
            action.lower() == "view"
            or action.lower() == "new"
            or action.lower() == "edit"
            or action.lower() == "delete"
            or action.lower() == "rel"
            or action.lower() == "unrel"
            or action.lower() == "mark"
            or action.lower() == "unmark"
            or action.lower() == "quit"
        ):
            # return if valid
            return action
        else:
            # err if invalid
            print("\nPlease input a valid action.")


# user facing function to ask for anything
def ask(question="\nPlease enter the name of a note: ") -> str:
    return input(question)


# user facing function to create a new note
def newNote(title: str, content: str) -> str:
    if title != "Important":
        note = Note(title, content, False)
        note.writeToFile()
        return "Note created."
    else:
        return("That name is reserved. Please pick another name")


# user facing function to edit an existing note
def editNote(note: str, content: str) -> str:
    # only edit if it exists
    if note in titles:
        # display current contents, ask for new content, then save file both in memory and on disk
        notes.remove(notes[titles.index(note)])
        titles.remove(note)
        newnote = Note(note, content, False)
        newnote.writeToFile()
        return "\nNote updated."
    # if it doesn't exist, error and exit function
    else:
        return "\nInvalid note, please try again."


# user facing function to delete an existing note
def delNote(note: str) -> str:
    rels = []
    # read note relationships
    with open(f"{note}_relationships.txt", "r") as f:
        rels = f.readlines()
    # for each relationship, remove from the other note's relationship to this one
    for i in rels:
        # don't try removing from important or an empty string
        if i != "Important\n" and i.strip() != "":
            oldrels = []
            newrels = []
            try:
                with open(f"{i.strip()}_relationships.txt", "r") as f:
                    oldrels = f.readlines()
                for rel in oldrels:
                    if rel != f"{note}\n":
                        newrels.append(rel)
                notes[titles.index(i.strip())].writeToFile(newrels)
            except FileNotFoundError:
                notes[titles.index(i.strip())].writeToFile()
    # remove files and list entries for note
    os.remove(f"{note}.txt")
    os.remove(f"{note}_relationships.txt")
    notes.remove(notes[titles.index(note)])
    titles.remove(note)
    return "\nNote deleted."


# user facing function to relate two notes together
def relNote(note1: str, note2: str) -> str:
    # only continue if notes exist
    if note1 in titles and note2 in titles:
        notes[titles.index(note1)].relate(note2)
        return f"\nRelated {note1} to {note2}..."
    # if notes don't exist, error and exit function
    else:
        return "\nInvalid note, please try again."


# user facing function to unrelate two notes
def unRelNote(note1: str, note2: str) -> str:
    # only continue if notes exist
    if note1 in titles and note2 in titles:
        notes[titles.index(note1)].unrelate(note2)
        return f"\nUnrelated {note1} from {note2}..."
    # if notes don't exist, error and exit function
    else:
        return "\nInvalid note, please try again."


# user facing function to mark note as important
def markImportant(note: str) -> str:
    # only mark important if not important
    if not notes[titles.index(note)].important:
        notes[titles.index(note)].markImportant()
        return f"\nMarked {note} as important..."
    else:
        return f"\n{note} is important."


# user facing function to unmark note as important
def unmarkImportant(note: str) -> str:
    # only unmark as important if important
    if notes[titles.index(note)].important:
        notes[titles.index(note)].unmarkImportant()
        return f"\nUnmarked {note} as important..."
    else:
        return f"\n{note} is not important, please try again."


def main() -> None:

    # search through files in current directory for notes and make a note in memory
    for file in os.listdir():
        if file.endswith(".txt") and not file.endswith("_relationships.txt"):
            with open(file, "r") as f:
                Note(file[:-4], f.read(), False)

    # search through files in current directory for relationships so that notes can be marked important in memory
    for file in os.listdir():
        if file.endswith("_relationships.txt"):
            with open(file, "r") as f:
                lines = f.readlines()
                if "Important\n" in lines:
                    notes[titles.index(file[:-18])].important = True

    # loop until user quit
    while True:
        # ask action
        action = askAction()

        # if user wants to view...
        if action.lower() == "view":
            # only display if there are notes
            if notes != []:
                # loop through each note, displaying title, content and related notes
                for i in notes:
                    # if it's important, add star
                    if i.important:
                        print(f"\n\033[1m{i.title} *\033[0m")
                        print(f"{i.content}")
                        print("\nRelated notes:")
                        try:
                            with open(f"{i.title}_relationships.txt", "r") as f:
                                lines = f.readlines()
                                for i in lines:
                                    if i.strip() != "Important":
                                        print(f" - {i.strip()}")
                        except FileNotFoundError:
                            pass
                        print()
                        print("-" * 20)
                    else:
                        print(f"\n\033[1m{i.title}\033[0m")
                        print(f"{i.content}")
                        print("\nRelated notes:")
                        try:
                            with open(f"{i.title}_relationships.txt", "r") as f:
                                lines = f.readlines()
                                for i in lines:
                                    if i.strip() != "Important":
                                        print(f" - {i.strip()}")
                        except FileNotFoundError:
                            pass
                        print()
                        print("-" * 20)
                    print()
            # if user has no notes, display message
            else:
                print("\nYou have no notes.")

        # if user wants to add new note, ask for title and contents, then pass that to newNote(), printing the output
        elif action.lower() == "new":
            title = ask("\nNote Title: ")
            # only continue if note doesn't already exist
            if title not in titles:
                content = ask("Note Content: ")
                print(newNote(title, content))
            # if note exists, error and loop
            else:
                print("\nNote already exists.")

        # if user wants to edit note, ask which note and new contents, then pass that to editNote(), printing the output
        elif action.lower() == "edit":
            note = ask("\nWhich note would you like to edit? ")
            # only continue if note exists
            if note in titles:
                content = ask("What would you like it to say now? ")
                print(editNote(note, content))
            # if note doesn't exist, error and loop
            else:
                print("\nNote doesn't exist yet.")

        # if user wants to delete note, ask which note, then ask confirmation, then delete if yes
        elif action.lower() == "delete":
            note = ask("\nWhich note would you like to delete? ")
            # only continue if note exists
            if note in titles:
                conf = ask(
                    "\nAre you sure you want to delete this note [ y(es) | n(o) ]? "
                )
                if conf.lower() == "y" or conf.lower() == "yes":
                    print(delNote(note))
                # print message if anything but y or yes
                else:
                    print("\nOkay, exiting...")
            # if note doesn't exist, error and loop
            else:
                print("\nNote doesn't exist yet.")

        # if user wants to relate notes, ask which notes, then pass those to relNote(), printing the output
        elif action.lower() == "rel":
            note1 = ask("\nWhat is the first note you would like to relate? ")
            # only continue if note1 exists
            if note1 in titles:
                note2 = ask(
                    f"\nWhat is the second note you would like to relate {note1} to? "
                )
                # only continue if note2 exists
                if note2 in titles:
                    print(relNote(note1, note2))
                # if note2 doesn't exist, error and loop
                else:
                    print(f"\nerror: {note2} doesn't exist")
            # if note1 doesn't exist, error and loop
            else:
                print(f"\nerror: {note1} doesn't exist")

        # if user wants to unrelate notes, ask which notes, then pass those to unRelNote(), printing the output
        elif action.lower() == "unrel":
            note1 = ask("\nWhat is the first note you would like to unrelate? ")
            # only continue if note1 exists
            if note1 in titles:
                note2 = ask(
                    f"\nWhat is the second note you would like to unrelate {note1} from? "
                )
                # only continue if note2 exists
                if note2 in titles:
                    print(unRelNote(note1, note2))
                # if note2 doesn't exist, error and loop
                else:
                    print(f"\nerror: {note2} doesn't exist")
            # if note1 doesn't exist, error and loop
            else:
                print(f"\nerror: {note1} doesn't exist")

        # if user wants to mark note as important, ask which note, then mark if note exists
        elif action.lower() == "mark":
            note = ask("\nWhat note would you like to mark as important? ")
            # only continue if note exists
            if note in titles:
                print(markImportant(note))
            # if note doesn't exist, error and loop
            else:
                print("\nNote doesn't exist yet.")

        # if user wants to unmark note as important, ask which note, then unmark if note exists
        elif action.lower() == "unmark":
            note = ask("\nWhat note would you like to unmark as important? ")
            # only continue if note exists
            if note in titles:
                print(unmarkImportant(note))
            # if note doesn't exist, error and loop
            else:
                print("\nNote doesn't exist yet.")

        # if user wants to quit, quit()
        elif action.lower() == "quit":
            quit()


# only run if in main.py
if __name__ == "__main__":
    main()
