from rest_framework import serializers
from articleScraper.models import Article
from articleScraper.serializers.revision import RevisionSerializer
from differ.diff import Differ


class ArticleSerializer(serializers.ModelSerializer):
    revisions = RevisionSerializer(many=True)
    diffs = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = (
            'created',
            'modified',
        )

    def get_diffs(self, obj):
        revisions = obj.revisions
        last_revision = None
        # Initialize the final diff list
        diffs = []
        # First entry is none so we compare the first with the second etc
        for revision in revisions:
            if last_revision is None:
                last_revision = revision
            else:
                same = True
                if len(last_revision.contents) != len(revision.contents):
                    same = False
                for index in range(len(last_revision.contents)):
                    if last_revision.contents[index] != revision.contents[index]:
                        same = False

                if not same:
                    for index in range(len(last_revision.contents)):
                        if last_revision.contents[index].content != revision.contents[index].content:
                            diff = Differ(last_revision.contents[index].content, revision.contents[index].content).diff
                            diffs.append(diff)

            # Update the last revision so we can check if there are more changes!
            # Might add a breakpoint to color it differently
            last_revision = revision

        return None
