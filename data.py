"""News content for Tuesday 24 November 2026.

Every story below was checked against live reporting on 24 November 2026
(One Turn daily briefing, Spyglass, Reuters, France 24, BBC, CNBC, The
Guardian, Al Jazeera, CBS, SCMP, Japan Times, Tagesschau, UPI). Facts are
baked in as constants: the program never touches the network.
"""

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "TUESDAY 24 NOVEMBER 2026"
TICKER = "Huang returns to Nvidia  •  Iran vows all means  •  Ukraine sinks warship off Libya"

LEAD = {
    "kicker": "TECHNOLOGY  ·  SANTA CLARA",
    "headline": "HUANG IS BACK AT NVIDIA",
    "body": (
        "Nvidia's board unanimously reinstated Jensen Huang as chief "
        "executive and chair on Monday, 11 days after he resigned over "
        "an affair with a woman US intelligence suspects of spying for "
        "China. Shares jumped about 31% and the Nasdaq gained 6.5%. "
        "Trump said he brokered the return."
    ),
}

MARKETS = [
    ("S&P 500", "+4.73%"),
    ("NASDAQ", "+6.5%"),
    ("NIKKEI", "-5.06%"),
    ("SENSEX", "-1.77%"),
    ("SK HYNIX", "+20%"),
    ("BRENT", "~$87"),
]

CARDS = [
    {
        "icon": "tanker",
        "kicker": "GULF  ·  STRAIT OF HORMUZ",
        "headline": "Iran vows 'all means' against US blockade",
        "body": (
            "Iran vowed to end the US blockade by all available means; "
            "Iranian media reported three tankers exploded after hitting "
            "mines in the strait."
        ),
    },
    {
        "icon": "ship",
        "kicker": "WAR  ·  BENGHAZI, LIBYA",
        "headline": "Ukraine sinks Russian warship off Libya",
        "body": (
            "Kyiv said seven naval drones sank the corvette Merkury at "
            "Benghazi and hit a cargo ship — the first admitted "
            "Ukrainian strike in the Mediterranean."
        ),
    },
    {
        "icon": "shield",
        "kicker": "SECURITY  ·  BERLIN",
        "headline": "NATO warns Russia, pledges space defense",
        "body": (
            "NATO ended its Berlin meeting vowing to defend every inch "
            "of its territory, and pledged defense in space amid reports "
            "of a Russian nuclear-armed satellite."
        ),
    },
    {
        "icon": "chip",
        "kicker": "CHIPS  ·  SINGAPORE",
        "headline": "US to blacklist Megaspeed in Nvidia scandal",
        "body": (
            "The US Commerce Department moved to place Megaspeed, the "
            "Singapore chip firm at the centre of the Nvidia espionage "
            "scandal, on its trade blacklist."
        ),
    },
]

STRIP = [
    {
        "kicker": "LAW  ·  THE HAGUE",
        "headline": "14 nations back ICJ genocide ruling",
        "body": (
            "Fourteen countries acknowledged the court's ruling that "
            "Myanmar committed genocide against the Rohingya."
        ),
    },
    {
        "kicker": "GAZA",
        "headline": "Oxfam: Gaza a 'toxic wasteland'",
        "body": (
            "Oxfam said signs of contamination appear across almost all "
            "of Gaza; Israeli strikes continued on Monday."
        ),
    },
]

WIRE = [
    "Zelensky: intelligence shows Russia planning new strikes",
    "Moscow accuses Estonia of acts 'on verge of open war'",
]

FOOTER = "The World Today  ·  Tuesday 24 November 2026  ·  Stories as reported on 24 November 2026"
SOURCES = "Sources: BBC, France 24, CNBC, Reuters, Al Jazeera, The Guardian, CBS, SCMP, UPI"
