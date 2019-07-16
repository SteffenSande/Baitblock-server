import diff_match_patch as dmp_module


class Differ(object):
    def __init__(self, old_content: str, new_content: str):
        """
            Module to find the diff between two strings
        Args:
            old_content (str): Text representation of the old html node
            new_content (str): Text representation of the new html node

        Example:
            input:  Old text: You are beautiful
                    New text: You are not ugly

            output: Comparison: [(0, 'You are '), (-1, 'beautiful'), (1, 'not ugly')]
        """
        self.old_content = old_content
        self.new_content = new_content
        self.is_diff = False
        self.diff = self.create_diff_of_text()

    def create_diff_of_text(self) -> str:
        """
        Merges diff between two strings with the most recent one.
        I.E "You are beautiful" And "You are not ugly." renders to
        You are |new|not|new| |old|beautiful|old||new|ugly|new|

        Returns (str):
            String representation of off the diff between two files, merged with the diff.
        """

        dmp = dmp_module.diff_match_patch()
        changes = dmp.diff_main(self.old_content, self.new_content)
        dmp.diff_cleanupSemantic(changes)
        return changes
