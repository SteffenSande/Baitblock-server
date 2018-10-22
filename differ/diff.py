from bs4 import BeautifulSoup
import diff_match_patch


class Differ(object):
    def __init__(self, content_selector: str, old_content: str, new_content: str, css_prefix: str="news-enhancer-diff"):
        """
            Module to find the diff between two html nodes
        Args:
            content_selector (str): Css selector of the content node
            old_content (str): Text representation of the old html node
            new_content (str): Text representation of the new html node
            css_prefix (str): Css class prefix for marking added and removed text
        """
        self.content_selector = content_selector
        self.old_content = old_content
        self.new_content = new_content
        self.is_diff = False
        self.style = """<style>
            .news-enhancer-diff-old {
            background: #FF7676;
            }
            .news-enhancer-diff-new {
            background: #90ff90;
            }
        </style>"""

        self.css_prefix_class = css_prefix

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

    def mark(self, text: str, css: str) -> str:
        """
            Encapsulates text with a span tag with a specified css class.
        Args:
            text (str): The text to be marked .
            css (str): The css class to mark the text

        Returns (str):
            Text representation of a span tag encapsulating the text with the css class
        """
        return '<span class=\"{0}-{1}\">{2}</span>'.format(self.css_prefix_class, css, text)

    def get_content(self, html: str) -> str:
        """
            Retrieves the specified content of a html node
        Args:
            html (str): Text representation of html

        Returns (str):
            Text representation of a specific html node

        """
        soup = BeautifulSoup(html, 'html.parser')
        selected_content = soup.select_one(self.content_selector)
        return str(selected_content)

    def create_diff_of_text(self) -> str:
        """
        Merges diff between two strings with the most recent one.
        I.E "You are beautiful" And "You are not ugly." renders to
        You are <span class="added">not</span> <span class="removed">beautiful</span><span class="added">ugly</span>

        Returns (str):
            String representation of off the diff between two files, merged with the diff.
        """

        changes = diff_match_patch.diff(self.old_content, self.new_content, timelimit=5, checklines=False)

        diff = ""
        old_length = 0
        new_length = 0
        for op, length in changes:
            if op == "-":  # in old file
                removed_text = self.old_content[old_length:old_length + length]
                old_text = self.mark_removed(removed_text)
                if old_text:
                    diff += old_text
                    self.is_diff = True
                old_length += length
            if op == "=":  # in both files
                equal_text = self.new_content[new_length:new_length + length]
                if equal_text:
                    diff += equal_text
                old_length += length
                new_length += length
            if op == "+":  # in new file
                added_text = self.new_content[new_length:new_length + length]
                new_text = self.mark_added(added_text)
                if new_text:
                    diff += new_text
                    self.is_diff = True
                new_length += length
        if diff:
            return '{}{}'.format(self.style, diff)
        else:
            return ''

    def create_diff_of_html(self) -> str:
        """
        Merges diff between two strings with the most recent one.
        I.E "You are beautiful" And "You are not ugly." renders to
        You are <span class="added">not</span> <span class="removed">beautiful</span><span class="added">ugly</span>

        Returns (str):
            String representation of off the diff between two files, merged with the diff.
        """
        old_content = self.get_content(self.old_content)
        new_content = self.get_content(self.new_content)

        if not old_content and not new_content:
            return ''

        changes = diff_match_patch.diff(old_content, new_content, timelimit=5, checklines=False)
        diff = ""
        old_length = 0
        new_length = 0
        for op, length in changes:
            if op == "-":  # in old file
                if not self.is_in_tag_definition(old_content[0:old_length]):
                    removed_text = old_content[old_length:old_length + length]
                    diff += self.mark_removed(removed_text)
                    self.is_diff = True
                old_length += length

            elif op == "=":  # in both files
                diff += new_content[new_length:new_length + length]
                old_length += length
                new_length += length
            elif op == "+":  # in new file
                if not self.is_in_tag_definition(new_content[0:new_length]):
                    added_text = new_content[new_length:new_length + length]
                    diff += self.mark_added(added_text)
                    self.is_diff = True
                new_length += length
        if diff:
            return '{}{}'.format(self.style, diff)
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
