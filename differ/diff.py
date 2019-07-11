import diff_match_patch as dmp_module


class Differ(object):
    def __init__(self, old_content: str, new_content: str):
        """
            Module to find the diff between two html nodes
        Args:
            content_selector (str): Css selector of the content node
            old_content (str): Text representation of the old html node
            new_content (str): Text representation of the new html node
        Example:
            input: Dette er noe : Dette er annet => "Dette er <old>noe<old/><new>annet<new/>"
        """
        self.old_content = old_content
        self.new_content = new_content
        self.is_diff = False
        self.diff = self.create_diff_of_text()

    def mark_added(self, text: str) -> str:
        """
            Marks text as added by encapsulating it in a <span> tag with a css class
        Args:
            text (str): The text to be marked as added.

        Returns (str):
            Text representation of a span tag encapsulating the text
        """
        return self.mark(text, "new")

    def mark_removed(self, text: str) -> str:
        """
            Marks text as removed by encapsulating it in a <span> tag with a css class
        Args:
            text (str): The text to be marked as removed.

        Returns (str):
            Text representation of a span tag encapsulating the text
        """
        return self.mark(text, "old")

    def mark(self, text: str, change: str) -> str:
        """
            Encapsulates a text with a fake tag new or old depending on it being new or old.
        Args:
            text (str): The text to be marked .
            change (str): Node name
        Returns (str):
            Text representation of a span tag encapsulating the text with the css class
        """
        result = ''
        try:
            result = '|' + change + '|' + text + '|' + change + '|'
        except TypeError:
            print(text)
            print(change)
            print(self)

        return result

    def create_diff_of_text(self) -> str:
        """
        Merges diff between two strings with the most recent one.
        I.E "You are beautiful" And "You are not ugly." renders to
        You are |new|not|new| |old|beautiful|old||new|ugly|new|

        Returns (str):
            String representation of off the diff between two files, merged with the diff.
        """
        if not self.old_content:
            self.is_diff = True
            return self.mark_added(self.new_content)
        if not self.new_content:
            self.is_diff = True
            return self.mark_removed(self.old_content)

        dmp = dmp_module.diff_match_patch()
        changes = dmp.diff_main(self.old_content, self.new_content)
        dmp.diff_cleanupSemantic(changes)
        diff = ""
        for op, word in changes:
            if op == 1:  # in old file
                diff += self.mark_added(word)
                self.is_diff = True
            if op == 0:  # in both files
                diff += word
            if op == -1:  # in new file
                diff += self.mark_removed(word)
                self.is_diff = True
        if diff:
            return diff
        else:
            return ''

    @staticmethod
    def is_in_tag_definition(original_text) -> bool:
        """
        Pretty naive implementation!
        Tests if the char on the current index in a text, is inside a html tag definition
        I.E between < and >

        Args:
            original_text:
        Returns (bool):
            True if the it hits < when iterating backwards from current index in the text.
             False otherwise.
        """
        for c in reversed(original_text):
            if c == '<':
                return True
            elif c == '>':
                return False
        return False
