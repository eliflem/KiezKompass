# Kiez Compass

Find the right Berlin neighborhood for you through a conversation, not a filter form.

Try the live app: https://kiezkompass-ejaxj6wdkaxpbboknnkzls.streamlit.app/

## The problem

Berlin is a large, diverse city made up of dozens of neighborhoods (Kieze), each with its own character: quiet or lively, family friendly or nightlife heavy, well connected or tucked away. For newcomers, especially migrants navigating an unfamiliar city, figuring out which area actually fits their life usually means asking friends, digging through forums, or guessing from listing photos.

Kiez Compass turns that search into a short conversation. You describe what matters to you, and the app asks a couple of smart follow up questions before recommending specific postal code areas, with real reasons, not generic praise.

## How it works

1. You describe what you're looking for in free text (for example, "I want somewhere quiet with parks nearby")
2. The app asks up to 3 clarifying questions if your preferences could point to different areas
3. It recommends 1 to 3 postal code areas, each with a specific explanation grounded in that area's actual transportation, demographics, green space, and housing character

The recommendation logic runs on Google's Gemini API, given a small hand curated dataset of Berlin postal code areas as context on every turn. There is no separate database or scoring engine; the model reasons directly over the structured data and decides for itself when it has enough information to answer confidently.

## Tech stack

* Frontend: Streamlit (https://streamlit.io)
* LLM: Google Gemini API (https://ai.google.dev), model gemini 3.1 flash lite, free tier
* Data: hand curated JSON dataset of Berlin postal code areas (transportation, vibe, family and nature amenities, housing type)
* Hosting: Streamlit Community Cloud

## Project status

This is an early MVP covering a limited set of Berlin neighborhoods, built to validate the core idea: that a conversational, reasoning based approach beats static filters for this kind of subjective, multi factor decision. Not yet included: apartment pricing data, full city coverage, or saved or shareable results.

## About this project

Kiez Compass was designed and built by Elif (https://www.linkedin.com/in/elif-sema-sanal/), a product manager, not an engineer, using AI assisted "vibe coding" (Claude for product and architecture decisions, OpenAI's Codex for implementation) to go from idea to a deployed, working app. It is as much a case study in scoping and directing AI built software as it is a neighborhood finder.

