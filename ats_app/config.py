from pathlib import Path
import yaml

DEFAULT_CONFIG = {
    "logging": {
        "level": "INFO",
        "file": "logs/app.log",
        "rotate_mb": 5
    },
    "ats": {
        "uk_spellings": [["optimize","optimise"], ["optimization","optimisation"], ["program","programme"]],
        "hard_keywords": [
            "aws","ec2","ecs","eks","lambda","rds","vpc","iam","cloudwatch","s3",
            "kubernetes","container","microservices","cluster management",
            "terraform","cloudformation","jenkins","gitlab ci","azure devops","xl release",
            "python","bash","powershell","groovy",
            "monitoring","logging","alerting","prometheus","grafana","loki","datadog","observability",
            "security","iam policies","security groups","vpc configurations","pci","gdpr","iso 27001",
            "automation","cost optimisation","budgets","mentoring","documentation"
        ],
        "soft_keywords": ["collaboration","troubleshooting","communication","stakeholder","leadership","mentoring","documentation","teamwork","problem-solving"],
        "red_flags": [
            {"pattern": "\\bexpert\\b.*\\bpython\\b", "message": "Avoid overstating coding proficiency; use 'basic scripting in Python'."},
            {"pattern": "\\bexpert\\b.*\\bansible\\b", "message": "Use 'basic exposure to Ansible' if true."},
            {"pattern": "\\bowned\\b.*\\beks\\b", "message": "If EKS is limited, phrase as 'working knowledge; labs and limited production‑adjacent use'."}
        ],
        "weights": {"hard": 0.7, "soft": 0.3}
    }
}

def load_config(path: str | None):
    if not path:
        return DEFAULT_CONFIG
    p = Path(path)
    if not p.exists():
        return DEFAULT_CONFIG
    with p.open("r", encoding="utf-8") as f:
        user_cfg = yaml.safe_load(f) or {}
    # merge shallow
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(user_cfg)
    return cfg