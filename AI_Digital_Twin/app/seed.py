from app.database import (
    initialize_database,
    get_db,
    fetch_one
)

from app.security import hash_password


def seed_database():

    initialize_database()

    with get_db() as db:

        # ---------------------------------------------------------
        # DEMO USERS
        # ---------------------------------------------------------

        users = [
            (
                "Ruhi Khan",
                "ruhi",
                hash_password("ruhi123"),
                "Owner",
                980
            ),
            (
                "Rutuja",
                "rutuja",
                hash_password("rutuja123"),
                "Data Analyst",
                840
            ),
            (
                "Piyusha",
                "piyusha",
                hash_password("piyusha123"),
                "Researcher",
                790
            ),
            (
                "Rimzim",
                "rimzim",
                hash_password("rimzim123"),
                "Explorer",
                720
            ),
            (
                "Ananya Joshi",
                "ananya",
                hash_password("demo123"),
                "AI Engineer",
                680
            )
        ]

        for user in users:

            existing = db.execute(
                "SELECT id FROM users WHERE username = ?",
                (user[1],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO users
                    (name, username, password_hash, role, points)
                    VALUES (?, ?, ?, ?, ?)
                """, user)

        # ---------------------------------------------------------
        # TECHNOLOGIES
        # ---------------------------------------------------------

        technologies = [
            ("Python", "Programming", 94, 18.6, 95),
            ("TypeScript", "Programming", 89, 21.4, 88),
            ("Rust", "Programming", 78, 29.8, 76),
            ("Go", "Programming", 76, 16.9, 74),
            ("SQL", "Data", 91, 12.8, 92),
            ("PyTorch", "AI / ML", 87, 24.2, 86),
            ("FastAPI", "Backend", 82, 31.1, 80),
            ("Kubernetes", "Cloud", 80, 14.7, 79),
            ("Docker", "Cloud", 88, 17.2, 90),
            ("Power BI", "Analytics", 79, 11.9, 77)
        ]

        for technology in technologies:

            existing = db.execute(
                "SELECT id FROM technologies WHERE name = ?",
                (technology[0],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO technologies
                    (name, category, score, growth, popularity)
                    VALUES (?, ?, ?, ?, ?)
                """, technology)

        # ---------------------------------------------------------
        # HIRING SIGNALS
        # ---------------------------------------------------------

        hiring = [
            ("Microsoft", "Cloud / AI", 1280, 22.4, "Very High"),
            ("Google", "AI / Cloud", 1150, 19.7, "Very High"),
            ("Amazon", "Cloud / Data", 1080, 18.2, "High"),
            ("NVIDIA", "AI / Hardware", 720, 36.5, "Very High"),
            ("Oracle", "Cloud / Data", 560, 15.4, "High"),
            ("TCS", "IT Services", 2450, 9.8, "High"),
            ("Infosys", "IT Services", 1920, 11.2, "High"),
            ("Accenture", "Technology", 2100, 14.8, "High")
        ]

        for item in hiring:

            existing = db.execute(
                "SELECT id FROM hiring_signals WHERE company = ?",
                (item[0],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO hiring_signals
                    (company, sector, openings, growth, signal)
                    VALUES (?, ?, ?, ?, ?)
                """, item)

        # ---------------------------------------------------------
        # AI TOOLS
        # ---------------------------------------------------------

        ai_tools = [
            ("ChatGPT", "Generative AI", 96, 8.4),
            ("Gemini", "Generative AI", 91, 11.7),
            ("Claude", "AI Assistant", 88, 15.2),
            ("GitHub Copilot", "Coding AI", 89, 12.4),
            ("Perplexity", "AI Search", 82, 18.9),
            ("Midjourney", "Generative Art", 76, 6.8),
            ("Hugging Face", "AI Platform", 84, 16.5),
            ("Cursor", "AI Coding", 87, 22.1)
        ]

        for tool in ai_tools:

            existing = db.execute(
                "SELECT id FROM ai_tools WHERE name = ?",
                (tool[0],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO ai_tools
                    (name, category, popularity, weekly_change)
                    VALUES (?, ?, ?, ?)
                """, tool)

        # ---------------------------------------------------------
        # CYBER THREATS
        # ---------------------------------------------------------

        threats = [
            (
                "Credential phishing campaign",
                "Critical",
                "Identity",
                "High activity"
            ),
            (
                "AI-generated malware samples",
                "High",
                "Malware",
                "Increasing"
            ),
            (
                "API abuse spike",
                "High",
                "API Security",
                "Detected"
            ),
            (
                "Supply-chain package risk",
                "Medium",
                "Software",
                "Monitoring"
            ),
            (
                "Bot traffic anomaly",
                "Medium",
                "Network",
                "Increasing"
            ),
            (
                "Cloud account scanning",
                "Low",
                "Cloud Security",
                "Stable"
            )
        ]

        for threat in threats:

            existing = db.execute(
                "SELECT id FROM threats WHERE title = ?",
                (threat[0],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO threats
                    (title, severity, category, activity)
                    VALUES (?, ?, ?, ?)
                """, threat)

        # ---------------------------------------------------------
        # STARTUPS
        # ---------------------------------------------------------

        startups = [
            (
                "Sarvam AI",
                "Artificial Intelligence",
                "Bengaluru",
                "$41M",
                94
            ),
            (
                "Krutrim",
                "Artificial Intelligence",
                "Bengaluru",
                "$75M",
                91
            ),
            (
                "E2E Networks",
                "Cloud Computing",
                "New Delhi",
                "$15M",
                82
            ),
            (
                "Qure.ai",
                "Healthcare AI",
                "Mumbai",
                "$110M",
                88
            ),
            (
                "Pixxel",
                "Space Technology",
                "Bengaluru",
                "$95M",
                86
            ),
            (
                "Yellow.ai",
                "Conversational AI",
                "Bengaluru",
                "$102M",
                84
            )
        ]

        for startup in startups:

            existing = db.execute(
                "SELECT id FROM startups WHERE name = ?",
                (startup[0],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO startups
                    (name, sector, location, funding, momentum)
                    VALUES (?, ?, ?, ?, ?)
                """, startup)

        # ---------------------------------------------------------
        # ACTIVITY FEED
        # ---------------------------------------------------------

        activities = [
            (
                "Python popularity increased",
                "Python crossed a new popularity threshold in the technology signal model.",
                "technology",
                "2026-10-08 18:45"
            ),
            (
                "AI hiring signal detected",
                "AI-related hiring activity increased across major technology companies.",
                "hiring",
                "2026-10-08 18:20"
            ),
            (
                "New cyber signal",
                "An increase in credential phishing activity was detected.",
                "security",
                "2026-10-08 17:55"
            ),
            (
                "Startup momentum changed",
                "Indian AI startup activity increased in the simulation.",
                "startup",
                "2026-10-08 17:25"
            ),
            (
                "AI tool trend updated",
                "AI coding assistants showed increasing activity this week.",
                "ai",
                "2026-10-08 16:50"
            )
        ]

        for activity in activities:

            existing = db.execute(
                "SELECT id FROM activities WHERE title = ?",
                (activity[0],)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO activities
                    (title, description, activity_type, created_at)
                    VALUES (?, ?, ?, ?)
                """, activity)

    print("Database created successfully.")
    print("Demo users added successfully.")
    print("Demo Digital Twin data added successfully.")


if __name__ == "__main__":
    seed_database()