# RELEASE SWITCH — the only file a release branch changes (darryn, 2026-11-08).
#
# Rule: every feature, fix and asset is built on main. A public release is
# EXTRACTED from main: branch release/<name>-v<version> off main and change only
# the two lines below (see docs/BRANCH_AND_RELEASE_POLICY.md). Everything that
# differs between the full developer build and a release (demo gate, title,
# version, build name, save folder, About text, hidden developer options,
# chapter select, dev/QA files left out of the zips) keys off these values.
#
#   LC_RELEASE = None          main: the full, unrestricted developer build
#   LC_RELEASE = "day1-demo"   public Prologue + Day One demo (gate ON)
#
# Add a new profile name to LC_RELEASE_PROFILES when a later public build
# needs different settings, e.g. "day2" for v0.2.x.
#
# This is `python early` in a file named 00_... so it runs before options.rpy,
# whose config.name / config.version / config.save_directory are evaluated
# while the scripts load (a normal `define` would be too late).

python early:
    LC_RELEASE = "day1-demo"
    LC_RELEASE_VERSION = "0.1.1"

    LC_RELEASE_PROFILES = {
        None: {
            "title": "Leia's Consent",
            "build_name": "LeiasConsentDev",
            "save_directory": "LeiasConsent-1789068362",
            "about_title": "Leia's Consent — full developer build ({}).",
        },
        "day1-demo": {
            "title": "Leia's Consent — Day One Demo",
            "build_name": "LeiasConsent-Day1Demo",
            "save_directory": "LeiasConsent-DayOneDemo-1789068362",
            "about_title": "Leia's Consent — Day One Demo, version {}.",
        },
    }

    LC_RELEASE_INFO = LC_RELEASE_PROFILES[LC_RELEASE]
    LC_IS_RELEASE = LC_RELEASE is not None
