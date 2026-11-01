# SDD App Builder

Describe the tool you need in plain words. Get a working app you can try right away.

SDD App Builder is for people who have a problem to solve but don't write code: an operations lead who needs a leave tracker, a finance analyst who wants to clean up a spreadsheet, a team that needs a simple feedback form. They type what they need, answer a few simple questions, and test the finished app inside the builder. The app is built behind the scenes using Spec-Driven Development (SDD), so the people using it never have to see a spec.

## The idea

Most "AI app builders" go straight from a prompt to code, and the result is hard to predict, hard to change and hard to fix. This project puts a written specification in the middle:

```
What you ask for  ->  Specification  ->  Plan and tasks  ->  Working app
   (plain words)       (hidden)            (hidden)           (you test it)
```

The specification is the source of truth. The app is built from it, checked against it, and changed by updating it. That makes builds more consistent, and it means a change request ("add a due date column") becomes a small, traceable edit rather than a rewrite.

Users never see any of this. They see a conversation, a progress indicator in everyday language, and their app.

## What a user can do

- **Describe what they need.** Free text, no templates or technical fields.
- **Answer a few simple questions.** The builder asks three to five multiple-choice questions, such as "Who will use this?" or "Do people need to log in?", so it builds what was meant instead of guessing.
- **Bring their own data.** Upload a CSV or Excel file. The builder reads it, shows what it found in plain language, and builds the app around those columns. The app starts pre-loaded with the data, so "show me totals by department" works on the first try.
- **Review a plain-language summary.** Before building, the user sees what will be made, in everyday terms, and can confirm or change it.
- **Try the app straight away.** The finished app runs live inside the builder. Users can add and edit records, run the feature they asked for, reset the test data, and restart the app if it misbehaves.
- **Ask for changes in plain words.** "Also group by region." The builder updates the specification and produces a new version.
- **Go back if a change goes wrong.** Every build is kept as a version, and any earlier version can be restored.

## What it builds

Internal tools: forms, trackers, dashboards and small data utilities. Every generated app uses the same fixed, simple stack with a local database. The narrow scope is deliberate: a consistent foundation is what makes the results reliable, so the focus is on getting common internal tools right rather than promising anything.

## How a build works

1. **Understand.** The builder reads the request and any uploaded data, and asks clarifying questions if the request is vague.
2. **Specify.** It writes the specification, plan and task list. These are stored with the version but never shown to the user.
3. **Build.** A coding agent works through the tasks, starting from a proven app template.
4. **Check itself.** The builder starts the app, tries each page the specification calls for, and confirms that the uploaded rows were loaded. If something fails, it fixes and retries, and if it still can't, it tells the user plainly and offers to try again or simplify.
5. **Hand over.** The user tests the live app, then asks for changes or keeps it.

## Design principles

- **Specs are the source of truth, and invisible.** Non-technical users should never need to learn the vocabulary.
- **Reliability over open-ended generation.** A fixed template and a self-checking step matter more than clever code generation.
- **Swappable infrastructure.** The agent framework, LLM, prompt store, tracing, file storage and sandbox each sit behind a small interface in `backend/core/`. Which one is used is a configuration choice, and adding a new one means extending a base class and registering it. Feature code never depends on a specific provider.
- **Data stays under control.** Uploaded files stay on the server and are deleted with the project. Only the structure of the data and a few sample rows are sent to the language model, never the full dataset.
- **Generated code is untrusted.** Apps run in a restricted workspace, bound to the local machine, with no access to the builder's secrets.

## Project layout

```
backend/
  core/          Swappable infrastructure behind interfaces: agent, llm, prompts,
                 tracing, object store, sandbox, plus config and a factory
  app/           Features: projects, chat, data upload, specs, builds, preview
  prompts/       Prompt files for each pipeline step, editable without code changes
  app_template/  The base app that every generated app starts from
frontend/        The builder interface: chat, questions, progress, live preview, versions
docs/            Product documentation, including the user stories
```

## Status

Early development. The backend foundation (configuration and the provider registry) is in place. The pipeline, builder interface and sandbox are next. The full list of what is planned, with priorities, is in [`docs/user-stories.md`](docs/user-stories.md).

## Not in scope yet

- Sharing a finished app with colleagues (needs sign-in and hosting)
- Multiple technology stacks for generated apps
- Strong container-level isolation for generated code (the first version uses a local sandbox and is meant for a trusted internal network)
