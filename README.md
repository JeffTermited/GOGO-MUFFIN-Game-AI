# GOGO Muffin AI Support Platform

An extensible conversational AI framework that helps users with reminders, web lookups, image annotation, and more—backed by a suite of custom tools and automations. Ideal as a demonstration of end-to-end solution design, data orchestration, and process automation.

---

## 📦 Repository Structure

```text
gogo-muffin/
├── click_data/
│   ├── click_recorder.py       # Interactive click annotation & YOLO labeling tool
│   ├── images/                 # Captured screenshots by class
│   ├── labels/                 # Generated YOLO .txt label files
│   ├── log/                    # Interaction logs & archives
│   └── previews/               # Full-screen previews with drawn boxes
├── automations/                # iCal-based task definitions for reminders & searches
├── tools/                      # Other custom modules (web, user_info, etc.)
├── config.json                 # Global settings (e.g. default box dimensions)
├── README.md                   # ← You are here
└── requirements.txt            # Python dependencies

🚀 Project Overview

GOGO Muffin is more than “just another chatbot”—it’s a toolbox you can extend:
	1.	Conversational Core
Built on Python, our engine routes user intents to:
	•	Reminder Automations (calendar tasks)
	•	Web & News Searches
	•	Image Capture & Annotation
	2.	Custom Tools
	•	Click Recorder: Interactive module to label UI elements via screenshots and generate YOLO-format labels.
	•	Scheduler: Converts natural-language reminders into iCal VEVENT automations.
	•	Web Browser & News: Real-time search and citation retrieval.
	•	User Info & Memories: Personalization based on preferences & location.
	3.	Business Analyst Lens
Every component follows BA best practices:
	•	Requirements Elicitation: Clean API for adding new tools.
	•	Process Modeling: Modular pipelines for capture → label → log → preview.
	•	Metrics & Dashboards: Logs, previews, and config feed into usage analytics.
	•	Documentation: This README + per-module READMEs ensure clarity for stakeholders.

🛠 Click Recorder Module

See click_data/click_recorder.py for a self-contained annotation tool:
	•	Test Mode: Visually tune capture‐box size
	•	Normal Mode:
	•	Full‐screen screenshot → images/<class>/...
	•	YOLO label → labels/<class>/...
	•	Operation log → log/click_log.txt
	•	Preview image → previews/<class>_normal_preview_...png

Config persists last box size in config.json.

## 📄 License
MIT © Jeff Hsieh
