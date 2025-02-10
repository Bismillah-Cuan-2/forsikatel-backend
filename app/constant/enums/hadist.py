from enum import Enum

class HadistEnums(Enum):
    HADIST = "hadist"
    KULTUM = "kultum"

    @classmethod
    def get_all_hadist(cls):
        return [hadist.value for hadist in cls]