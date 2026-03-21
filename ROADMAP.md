# Witch Doctor — Roadmap

## Current Status

Witch Doctor is in active early development. The repository structure is in place — folders for the bot, RAG pipeline, scrapers, data, cleaner, tracker, and vision system have all been set up. No functional code has been written yet. The next step is building out the databases.

If you want to get involved from the ground floor this is the time.

---

## v1 — First Usable Release

v1 is the milestone where Witch Doctor becomes something anyone can pick up and use — no technical knowledge required. It's broken down into five steps that build on each other:

**Step 1 — The Databases** *(in progress)*
Building out the three core datasets: drugs & interactions, DIY HRT, and overdose response. This is where it all starts.

**Step 2 — The RAG Pipeline**
Setting up the system that lets the AI actually use the data — connecting the databases to the model so it can pull the right information and give accurate answers.

**Step 3 — Visual Identification**
Adding image recognition so users can send a photo of an unknown pill, capsule, or substance and get back an identification along with relevant harm reduction information. This is handled by a dedicated vision pipeline separate from the main chat system.

**Step 4 — OpenWebUI**
Plugging everything into OpenWebUI so there's a clean interface people can actually talk to.

**Step 5 — Discord Bot**
Bringing Witch Doctor to Discord with a public invite link so anyone can access it without any setup at all.

**Step 6 — Polish**
Testing, fixing, and making sure everything works the way it should. When this step is done v1 is live.

---

## v2 — Withdrawal Management

v2 adds withdrawal management to the knowledge base. Every version from here follows the same process:

**Step 1 — Sources**
Finding and vetting reliable sources for the topic before anything gets written or scraped.

**Step 2 — Database**
Building out the dataset from those sources in the same format as v1.

**Step 3 — RAG Integration**
Adding the new data into the RAG pipeline so the AI can actually use it.

**Step 4 — Review & Test**
Checking the data for accuracy, testing responses, making sure nothing is wrong or missing.

**Step 5 — Publish**
Tagging the new version and pushing it live.

---

## v3 — Body Modifications

v3 adds body modification information to the knowledge base covering DIY procedures, aftercare, and safer practices.

**Step 1 — Sources**
Finding and vetting reliable sources for the topic before anything gets written or scraped.

**Step 2 — Database**
Building out the dataset from those sources in the same format as v1.

**Step 3 — RAG Integration**
Adding the new data into the RAG pipeline so the AI can actually use it.

**Step 4 — Review & Test**
Checking the data for accuracy, testing responses, making sure nothing is wrong or missing.

**Step 5 — Publish**
Tagging the new version and pushing it live.

---

## v4 — Sexual Health

v4 adds sexual health information covering PrEP, PEP, STIs, and safer practices.

**Step 1 — Sources**
Finding and vetting reliable sources for the topic before anything gets written or scraped.

**Step 2 — Database**
Building out the dataset from those sources in the same format as v1.

**Step 3 — RAG Integration**
Adding the new data into the RAG pipeline so the AI can actually use it.

**Step 4 — Review & Test**
Checking the data for accuracy, testing responses, making sure nothing is wrong or missing.

**Step 5 — Publish**
Tagging the new version and pushing it live.

---

## v5 — Mental Health & Substances

v5 adds information covering the intersection of mental health and substance use — the final planned topic and the milestone that completes the core knowledge base.

**Step 1 — Sources**
Finding and vetting reliable sources for the topic before anything gets written or scraped.

**Step 2 — Database**
Building out the dataset from those sources in the same format as v1.

**Step 3 — RAG Integration**
Adding the new data into the RAG pipeline so the AI can actually use it.

**Step 4 — Review & Test**
Checking the data for accuracy, testing responses, making sure nothing is wrong or missing.

**Step 5 — Publish**
Tagging the new version and pushing it live.

---

## Post v5 — Website Integration

Once the core knowledge base is complete the goal is to bring Witch Doctor to my personal website as a full chat interface. To do this safely without exposing my home network I'll be renting a VPS to act as a middleman between the website and the server running Witch Doctor — keeping everything secure while still making it publicly accessible.

Donations aren't being collected right now but if there's enough interest that may change down the line. Either way this is happening — just a matter of when.

---

## Long Term — SHAMAN

Once the core knowledge base is complete the long term goal is to take everything Witch Doctor has built and use it to train a dedicated model — codename SHAMAN.

SHAMAN will be fine tuned on all of Witch Doctor's data making it faster, more accurate, and purpose built for harm reduction rather than a general purpose AI running on top of a database. It will still use the same knowledge base but the responses will feel more natural and more in tune with what this project is actually for.

**Fine tuning data**

To fine tune SHAMAN we need real conversational data. Here's how you can help if you want to:

* **Donate your chat logs** — if you've used Witch Doctor and are willing to share your conversation logs for training purposes you can submit them as an issue or pull request. This is entirely voluntary, no pressure whatsoever.
* **Help prep the data** — if you know how to prepare and format chat logs for fine tuning your help would be hugely valuable. Jump in on the fine tuning issue when it opens.
* **Don't worry if you can't help** — if no logs are donated or there aren't enough we'll generate synthetic ones. Real logs help but they're not required.

SHAMAN is a long way off — Witch Doctor needs to be mature and well tested before fine tuning begins. But it's where all of this is heading.

---

## Long Term — Field Medic

After SHAMAN, if this project still has the interest and community behind it, the next step is Field Medic — a fully open source cyberdeck built to run SHAMAN locally without needing an internet connection.

The goal is simple: bring harm reduction directly to the people who need it most. Field Medic is a mobile terminal that can be carried anywhere and set up in minutes. Me and any volunteers willing to help their local communities will be running stands where people can walk up, ask questions, and use the terminal themselves — no internet, no accounts, no barriers. And for anyone who doesn't feel comfortable talking to a person face to face, the terminal is right there.

Everything about it — the hardware design, the software, the setup guide — will be open source so anyone anywhere can build one and do the same.
