from ovos_workshop.frameworks.playback import CPSMatchType, CPSPlayback, \
    CPSMatchConfidence
from ovos_workshop.skills.video_collection import VideoCollectionSkill
from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename


class ClassicScifiHorrorSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("ClassicScifiHorror")
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.MOVIE,
                                CPSMatchType.VIDEO]
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        # load video catalog
        path = join(dirname(__file__), "res", "scifi_horror.jsondb")
        logo = join(dirname(__file__), "res", "scifihorror.png")
        self.media_collection = Collection("SciFi_Horror", logo=logo, db_path=path)
        self.default_image = join(dirname(__file__), "ui", "scifihorror.png")
        self.skill_logo = join(dirname(__file__), "ui", "scifihorror.png")
        self.skill_icon = join(dirname(__file__), "ui", "scifihorror.png")
        self.default_bg = logo
        self.media_type = CPSMatchType.MOVIE
        self.playback_type = CPSPlayback.GUI

    # voice interaction
    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # better common play
    def normalize_title(self, title):
        title = title.lower().strip()
        title = self.remove_voc(title, "movie")
        title = self.remove_voc(title, "play")
        title = self.remove_voc(title, "video")
        title = self.remove_voc(title, "scifi")
        title = self.remove_voc(title, "horror")
        title = title.replace("|", "").replace('"', "") \
            .replace(':', "").replace('”', "").replace('“', "") \
            .strip()
        return " ".join([w for w in title.split(" ") if w])  # remove extra spaces

    def match_media_type(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "video") or media_type == CPSMatchType.VIDEO:
            score += 5

        if self.voc_match(phrase, "movie") or media_type == CPSMatchType.MOVIE:
            score += 10

        if self.voc_match(phrase, "old"):
            score += 30

        if self.voc_match(phrase, "public_domain"):
            score += 15

        if self.voc_match(phrase, "scifi"):
            score += 30

        if self.voc_match(phrase, "horror"):
            score += 30

        return score


def create_skill():
    return ClassicScifiHorrorSkill()

