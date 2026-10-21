# Compatibility getter paired with set_story_flag().
# Existing story code historically used has_story_flag(); newer route code may
# use get_story_flag() when assigning a boolean value to a local variable.

init 998 python:
    def get_story_flag(flag_id):
        return has_story_flag(flag_id)
