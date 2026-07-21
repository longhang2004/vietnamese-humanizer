def test_get_patterns(client):
    response = client.get("/api/patterns")
    assert response.status_code == 200
    data = response.json()
    assert "patterns" in data
    patterns = data["patterns"]
    assert len(patterns) > 0

    first = patterns[0]
    required_keys = [
        "id",
        "name",
        "skill",
        "category",
        "finding_type",
        "severity",
        "summary",
        "why_it_matters",
        "rewrite_strategy",
    ]
    for key in required_keys:
        assert key in first


def test_get_skills(client):
    response = client.get("/api/skills")
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    skills = data["skills"]
    assert len(skills) == 4
    skill_ids = [s["id"] for s in skills]
    assert "humanizer-vi" in skill_ids
    assert "style-guide-vi" in skill_ids
