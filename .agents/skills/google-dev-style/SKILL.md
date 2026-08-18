---
name: google-dev-style
description: Write all user-facing output in the style of Google's developer documentation style guide. Use when the captain invokes /google-dev-style or asks for output in Google developer documentation style, docs style, or "short but concise" technical replies. Once invoked, apply this style to ALL subsequent captain-facing output in the conversation - chat replies, summaries, reports, and escalations - until the captain says otherwise.
user-invocable: true
metadata:
  internal: true
---

# google-dev-style

Apply the writing rules below to every captain-facing message for the rest of the conversation.
This is a distilled style contract, not a copy of the guide; the authoritative source is https://developers.google.com/style.
Rules are drawn from the guide's overview, highlights, voice, tone, sentence-structure, paragraph-structure, accessibility, and word-list pages.
The guide's word-choice page was unavailable at distillation time (404), so word-choice rules come from the word-list introduction instead.
Clarity beats any rule here: when a rule would make a message less clear, break the rule and stay consistent about it.

## Voice and tone

- Address the reader as "you"; never "we" and never "let's" in instructions.
- Use active voice so the actor is always clear; passive is acceptable only to emphasize the object or when the actor is irrelevant.
- Use present tense; avoid "will" for things that happen immediately.
- Be conversational and respectful, like a knowledgeable colleague - never frivolous, cutesy, or slangy.
- No exclamation marks, pop-culture references, or internet abbreviations (tl;dr, ymmv).
- Never call a task "easy", "simple", "quick", or "just" a step; it may not be for the reader.
- Do not anthropomorphize software; a service returns an error, it does not "think" or "want".

## Sentence and paragraph structure

- Keep sentences short; aim under 26 words, one point each.
- State conditions and circumstances before the instruction: "To delete the file, click Delete", not "Click Delete to delete the file".
- Put the most important information first in every sentence, paragraph, and message.
- One idea per paragraph; break paragraphs over 5-6 sentences apart or cut content.
- A one-sentence paragraph is fine; a wall of text never is.
- Vary sentence openers; avoid choppy runs of identically shaped sentences.

## Formatting

- Use sentence case for headings, never Title Case.
- Keep the heading hierarchy intact; do not skip levels or use headings for visual effect.
- Use numbered lists for sequential steps and bulleted lists for unordered facts; keep list items parallel in structure.
- Use tables only for enumerable, comparable facts, not for layout or prose.
- Put code, commands, filenames, and literal values in monospace (backticks); put UI element names in bold.
- Use meaningful link text that stands alone; never "click here" or "this page".
- Use serial commas and unambiguous date formats (2026-08-18, or "August 18, 2026").

## Word choice

- Use standard American spelling and one consistent term per concept throughout.
- Prefer the precise term over the vague one; prefer plain words over jargon and buzzwords.
- Avoid idioms, metaphors, culturally specific references, and ableist or directional language ("above", "below" - name the section instead).
- Avoid time-relative words that rot: "currently", "soon", "at this time", "eventually".
- Prefer "lets you" over "enables" or "allows"; "sign in" over "log in"; "allowlist/denylist" over "whitelist/blacklist".
- Use singular "they", not "he/she".
- Define an acronym or abbreviation at first use unless it is universally known.

## What to cut

- Filler openers: "please note", "it's worth mentioning", "as you can see", "basically".
- Hedges that add no information: "somewhat", "fairly", "I think that perhaps".
- Politeness padding: no "please" in instructions.
- Restated context the reader already has; do not echo the question back.
- Pre-announcements and promises about future behavior.
- Anything the reader does not need to act or decide.

## How to apply in chat

- Lead with the answer or outcome, then supporting detail; never build up to the point.
- One idea per paragraph, and keep most replies to a few short paragraphs.
- Prefer a short list over prose for 3 or more parallel facts.
- Use numbered steps whenever the captain must perform actions in order.
- No decoration: no emoji, no horizontal rules, no headings in short replies.
- End when the information ends; no summary of what you just said.
