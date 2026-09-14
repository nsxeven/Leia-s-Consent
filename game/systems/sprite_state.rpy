# Leia sprite state and wardrobe integration.
# Story code changes pose/expression through helpers; outfit comes from equipped_outfit.

init python:

    LEIA_POSES = (
        ("p01", "P01 — Neutral standing"),
        ("p02", "P02 — Confident / hand-on-hip"),
        ("p03", "P03 — Shy / closed posture"),
    )

    LEIA_EXPRESSIONS = (
        ("neutral", "Neutral"),
        ("smile", "Soft smile"),
        ("teasing", "Teasing"),
        ("embarrassed", "Embarrassed"),
        ("annoyed", "Annoyed"),
    )

    LEIA_OUTFIT_ATTRIBUTES = {
        "casual_default": "outfit_casual",
        # Distinct placeholder attributes keep Chapter 1 outfit branches visually testable.
        "pool_conservative": "outfit_pool_conservative",
        "pool_bolder": "outfit_pool_bolder",
        # The Chapter 1 restaurant outfit reuses the current date-dress placeholder layer.
        "resort_dinner_dress": "outfit_date",
        "date_night_dress": "outfit_date",
        "after_hours_dress": "outfit_after_hours",
    }

    LEIA_CONTROLLED_ATTRIBUTES = set(
        ["pose_{}".format(pose_id) for pose_id, _label in LEIA_POSES]
        + ["expr_{}".format(expression_id) for expression_id, _label in LEIA_EXPRESSIONS]
        + list(LEIA_OUTFIT_ATTRIBUTES.values())
    )


    def leia_pose_label():
        labels = dict(LEIA_POSES)
        return labels.get(renpy.store.leia_pose, renpy.store.leia_pose)


    def leia_expression_label():
        labels = dict(LEIA_EXPRESSIONS)
        return labels.get(renpy.store.leia_expression, renpy.store.leia_expression)


    def leia_outfit_attribute():
        return LEIA_OUTFIT_ATTRIBUTES.get(
            renpy.store.equipped_outfit,
            "outfit_casual",
        )


    def leia_adjust_attributes(names):
        """Make save-state pose/expression/outfit the source of truth for image attributes."""
        attributes = set(names[1:])
        attributes.difference_update(LEIA_CONTROLLED_ATTRIBUTES)

        pose_id = renpy.store.leia_pose
        valid_poses = set(pose for pose, _label in LEIA_POSES)
        if pose_id not in valid_poses:
            pose_id = "p01"

        expression_id = renpy.store.leia_expression
        valid_expressions = set(expression for expression, _label in LEIA_EXPRESSIONS)
        if expression_id not in valid_expressions:
            expression_id = "neutral"

        attributes.add("pose_{}".format(pose_id))
        attributes.add("expr_{}".format(expression_id))
        attributes.add(leia_outfit_attribute())

        return (names[0],) + tuple(sorted(attributes))


    def refresh_leia_sprite_if_visible():
        """Re-show Leia so the layered image re-evaluates the canonical sprite state."""
        if renpy.showing("leia"):
            renpy.show("leia")


    def set_leia_pose(pose_id):
        valid_poses = set(pose for pose, _label in LEIA_POSES)
        if pose_id not in valid_poses:
            raise ValueError("Unknown Leia pose: {}".format(pose_id))

        renpy.store.leia_pose = pose_id
        refresh_leia_sprite_if_visible()
        renpy.restart_interaction()
        return pose_id


    def set_leia_expression(expression_id):
        valid_expressions = set(expression for expression, _label in LEIA_EXPRESSIONS)
        if expression_id not in valid_expressions:
            raise ValueError("Unknown Leia expression: {}".format(expression_id))

        renpy.store.leia_expression = expression_id
        refresh_leia_sprite_if_visible()
        renpy.restart_interaction()
        return expression_id


    def set_leia_sprite(pose_id=None, expression_id=None):
        """Convenience helper for future chapter scripts."""
        if pose_id is not None:
            valid_poses = set(pose for pose, _label in LEIA_POSES)
            if pose_id not in valid_poses:
                raise ValueError("Unknown Leia pose: {}".format(pose_id))
            renpy.store.leia_pose = pose_id

        if expression_id is not None:
            valid_expressions = set(expression for expression, _label in LEIA_EXPRESSIONS)
            if expression_id not in valid_expressions:
                raise ValueError("Unknown Leia expression: {}".format(expression_id))
            renpy.store.leia_expression = expression_id

        refresh_leia_sprite_if_visible()
        return (renpy.store.leia_pose, renpy.store.leia_expression)


    def debug_reset_leia_sprite():
        renpy.store.leia_pose = "p01"
        renpy.store.leia_expression = "neutral"
        renpy.store.modified_save = True
        refresh_leia_sprite_if_visible()
        renpy.restart_interaction()


    # Every `show leia` call is normalized to the save-state pose, expression,
    # and currently equipped wardrobe outfit.
    config.adjust_attributes["leia"] = leia_adjust_attributes
